"""
Pillar 2 – Documents API Router
Endpoints:
  POST   /documents/upload/{case_id}    → Multi-format ingestion + BERT classification
  GET    /documents/{case_id}           → List all documents for an entity
  PATCH  /documents/{document_id}       → HITL: approve / override label, update status
  GET    /documents/{document_id}/status → Lightweight status polling
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List

from ..db.session import get_db
from ..models.document import Document
from ..schemas.document import DocumentResponse, DocumentUpdate, DocumentStatusResponse
from ..services.document_service import process_document_upload
from ..services.extractor import extractor

router = APIRouter(prefix="/documents", tags=["Pillar 2 – Documents"])

# Valid status transitions (enforced loosely to prevent nonsensical states)
VALID_STATUSES = {"uploaded", "classified", "pending_review", "approved", "rejected", "extraction_in_progress", "complete"}


@router.post("/upload/{case_id}", response_model=DocumentResponse, summary="Upload & auto-classify a document")
async def upload_document(
    case_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    from ..models.entity import Entity  # Avoid circular import

    entity = db.query(Entity).filter(Entity.case_id == case_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity with case_id '{case_id}' not found")

    return await process_document_upload(entity.id, case_id, file, db)


@router.get("/{case_id}", response_model=List[DocumentResponse], summary="List all documents for a case")
def list_documents(case_id: str, db: Session = Depends(get_db)):
    from ..models.entity import Entity

    entity = db.query(Entity).filter(Entity.case_id == case_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail=f"Entity with case_id '{case_id}' not found")

    docs = db.query(Document).filter(Document.entity_id == entity.id).order_by(Document.created_at.desc()).all()
    return docs


@router.patch("/{document_id}", response_model=DocumentResponse, summary="HITL: approve / override classification")
def review_document(document_id: str, doc_in: DocumentUpdate, db: Session = Depends(get_db)):
    """
    Human-in-the-Loop review endpoint.
    Credit officer can:
      - Set `user_label` to override the AI's `auto_label`
      - Set `status` to 'approved' or 'rejected' to close the review loop
    """
    db_doc = db.query(Document).filter(Document.id == document_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc_in.user_label is not None:
        db_doc.user_label = doc_in.user_label

    if doc_in.status is not None:
        if doc_in.status not in VALID_STATUSES:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid status '{doc_in.status}'. Valid: {sorted(VALID_STATUSES)}"
            )
        db_doc.status = doc_in.status
        
        # Pillar 4: Trigger extraction if approved
        if doc_in.status == "approved" and db_doc.extracted_text:
            label = db_doc.user_label or db_doc.auto_label
            if label:
                extraction_results = extractor.extract(label, db_doc.extracted_text)
                db_doc.extracted_data = extraction_results.get("raw_values", {})

    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc


@router.get("/{document_id}/status", response_model=DocumentStatusResponse, summary="Poll document processing status")
def get_document_status(document_id: str, db: Session = Depends(get_db)):
    db_doc = db.query(Document).filter(Document.id == document_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_doc
