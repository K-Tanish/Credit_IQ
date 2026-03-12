"""
Pillar 2 – Multi-Format Document Ingestion Service
Supports: PDF (text + OCR fallback), Excel/CSV, Images (Tesseract OCR)
"""

import os
import uuid
import shutil
import io
import pandas as pd
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from fastapi import UploadFile
from sqlalchemy.orm import Session
from ..models.document import Document
from ..services.classifier import classifier

UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# --- Supported MIME type groups ---
PDF_TYPES = {"application/pdf"}
EXCEL_TYPES = {
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/csv",
}
IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/tiff", "image/bmp"}


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using PyMuPDF; fall back to Tesseract OCR for scanned pages."""
    text_parts = []
    try:
        doc = fitz.open(file_path)
        for page_num in range(min(3, len(doc))):
            page = doc[page_num]
            page_text = page.get_text().strip()
            if not page_text:
                # Scanned page → rasterise and OCR
                pix = page.get_pixmap(dpi=200)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                page_text = pytesseract.image_to_string(img)
            text_parts.append(page_text)
        doc.close()
    except Exception as e:
        text_parts.append(f"[PDF extraction error: {e}]")
    return "\n".join(text_parts)


def extract_text_from_excel(file_path: str, content_type: str) -> str:
    """Stringify the first sheet / CSV into a text snippet for classification."""
    try:
        if content_type == "text/csv":
            df = pd.read_csv(file_path, nrows=50)
        else:
            df = pd.read_excel(file_path, nrows=50)
        # Combine column headers + first few rows into a readable string
        header = " | ".join(str(c) for c in df.columns.tolist())
        sample = df.head(10).to_string(index=False)
        return f"Columns: {header}\n\nSample rows:\n{sample}"
    except Exception as e:
        return f"[Excel extraction error: {e}]"


def extract_text_from_image(file_path: str) -> str:
    """OCR an image file."""
    try:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        return f"[Image OCR error: {e}]"


def derive_file_type_from_name(filename: str) -> str:
    """Fallback MIME guesser from extension."""
    ext = filename.rsplit(".", 1)[-1].lower()
    mapping = {
        "pdf": "application/pdf",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "csv": "text/csv",
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "tiff": "image/tiff",
        "bmp": "image/bmp",
    }
    return mapping.get(ext, "application/octet-stream")


async def process_document_upload(entity_id: str, case_id: str, file: UploadFile, db: Session) -> Document:
    """
    Core Pillar-2 ingestion pipeline:
      1. Save file to disk with a collision-safe name.
      2. Detect format and extract a representative text snippet.
      3. Run BERT-based zero-shot classifier.
      4. Persist a Document record with auto_label + confidence_score.
    """
    # --- 1. Save ---
    safe_id = str(uuid.uuid4())[:8]
    dest_filename = f"{entity_id}_{safe_id}_{file.filename}"
    file_path = os.path.join(UPLOADS_DIR, dest_filename)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    file_size = len(content)

    # --- 2. Resolve content type ---
    content_type = file.content_type or derive_file_type_from_name(file.filename)

    # --- 3. Extract text snippet ---
    if content_type in PDF_TYPES or file.filename.lower().endswith(".pdf"):
        snippet = extract_text_from_pdf(file_path)
    elif content_type in EXCEL_TYPES or file.filename.lower().endswith((".xls", ".xlsx", ".csv")):
        snippet = extract_text_from_excel(file_path, content_type)
    elif content_type in IMAGE_TYPES or file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
        snippet = extract_text_from_image(file_path)
    else:
        # Unknown binary; use filename as weak signal
        snippet = file.filename

    # --- 4. Classify ---
    label, confidence = classifier.classify_text(snippet[:1500])

    # --- 5. Persist ---
    db_doc = Document(
        entity_id=entity_id,
        case_id=case_id,
        filename=file.filename,
        file_path=file_path,
        file_type=content_type,
        file_size=float(file_size),
        auto_label=label,
        confidence_score=round(confidence, 4),
        extracted_text=snippet,
        status="pending_review" if confidence < 0.70 else "classified",
    )
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)

    return db_doc
