"""
Pillar 2 – BERT-based Document Classifier (Sentence-Transformers)
Strategy:
  - Primary: cosine-similarity against a labelled reference dataset (CAMS_BERT_Classifier_Dataset.xlsx)
  - Fallback: zero-shot via canonical label descriptions when no dataset is found
"""

import os
import logging
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer, util

logger = logging.getLogger(__name__)

# Canonical CAMS document types with rich semantic descriptions
CANONICAL_LABELS: dict[str, str] = {
    "ALM Report": (
        "Asset Liability Management report showing maturity profile, liquidity gaps, "
        "interest rate risk, bucket-wise cash flows"
    ),
    "Balance Sheet": (
        "Annual balance sheet showing assets, liabilities, equity, fixed assets, "
        "current assets, long-term debt, net worth"
    ),
    "Bank Statement": (
        "Bank account statement showing transaction history, credits, debits, "
        "account balance, cash inflows and outflows"
    ),
    "GST Return": (
        "Goods and Services Tax return GSTR-1 GSTR-3B showing sales, purchases, "
        "input tax credit ITC, tax liability"
    ),
    "ITR Filing": (
        "Income Tax Return filing showing gross total income, taxable income, "
        "deductions, tax paid, refund due"
    ),
    "Profit & Loss Statement": (
        "Profit and Loss statement income statement showing revenue, expenses, "
        "EBITDA, depreciation, net profit or loss"
    ),
    "Shareholding Pattern": (
        "Shareholding pattern showing promoter holding, FII, DII, public float, "
        "percentage ownership, equity structure"
    ),
    "Credit Report": (
        "Credit information report CIBIL bureau report showing credit score, "
        "loan accounts, repayment history, NPA classification"
    ),
    "Audit Report": (
        "Statutory audit report showing auditors opinion, qualifications, "
        "key audit matters, internal control assessment"
    ),
    "KYC Document": (
        "Know Your Customer document identity proof PAN Aadhaar passport "
        "address proof director identification"
    ),
    "Borrowing Profile": (
        "Borrowing profile showing existing loans, term loans, working capital limits, "
        "OD utilization, lender details, repayment schedule"
    ),
    "MCA Filing": (
        "MCA21 Ministry of Corporate Affairs filing annual return ROC forms "
        "director details company registration"
    ),
}


class DocumentClassifier:
    def __init__(self, dataset_path: str | None = None):
        logger.info("Loading SentenceTransformer model (all-MiniLM-L6-v2)…")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.reference_texts: list[str] = []
        self.reference_labels: list[str] = []
        self.label_embeddings = None
        self._mode = "zero_shot"         # 'dataset' or 'zero_shot'

        dataset_loaded = False
        if dataset_path and os.path.exists(dataset_path):
            dataset_loaded = self._load_dataset(dataset_path)

        if not dataset_loaded:
            logger.warning(
                "Reference dataset not found or empty. "
                "Falling back to zero-shot mode with canonical label descriptions."
            )
            self._load_zero_shot_labels()

    # ------------------------------------------------------------------
    def _load_dataset(self, path: str) -> bool:
        """Load labelled reference dataset and pre-compute embeddings."""
        try:
            df = pd.read_excel(path)
            # Accept first two columns as (text, label), drop NaN rows
            df = df.iloc[:, :2].dropna()
            df.columns = ["text", "label"]
            if df.empty:
                return False

            self.reference_texts = df["text"].tolist()
            self.reference_labels = df["label"].tolist()
            self.label_embeddings = self.model.encode(
                self.reference_texts, convert_to_tensor=True, show_progress_bar=False
            )
            self._mode = "dataset"
            logger.info(f"Loaded {len(self.reference_texts)} reference samples from dataset.")
            return True
        except Exception as e:
            logger.error(f"Failed to load dataset: {e}")
            return False

    def _load_zero_shot_labels(self):
        """Use canonical label descriptions as the reference corpus."""
        for label, description in CANONICAL_LABELS.items():
            self.reference_texts.append(description)
            self.reference_labels.append(label)

        self.label_embeddings = self.model.encode(
            self.reference_texts, convert_to_tensor=True, show_progress_bar=False
        )
        self._mode = "zero_shot"
        logger.info(f"Zero-shot mode: {len(self.reference_labels)} canonical label descriptions loaded.")

    # ------------------------------------------------------------------
    def classify_text(self, text: str, top_k: int = 1) -> tuple[str, float]:
        """
        Classify a text snippet.
        Returns (label, confidence_score) where confidence ∈ [0, 1].
        """
        if self.label_embeddings is None or not text.strip():
            return "Unknown", 0.0

        query_embedding = self.model.encode(text, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.label_embeddings)[0]

        top_result = torch.topk(cos_scores, k=1)
        best_idx = top_result.indices[0].item()
        best_score = top_result.values[0].item()

        label = self.reference_labels[best_idx]
        # Normalise: cosine similarity is [-1,1] → clip to [0,1]
        confidence = max(0.0, min(1.0, float(best_score)))

        return str(label), confidence

    @property
    def mode(self) -> str:
        return self._mode


# ---- Global singleton ----
_DATASET_PATH = os.environ.get(
    "CLASSIFIER_DATASET_PATH",
    "app/data/CAMS_BERT_Classifier_Dataset.xlsx"
)
classifier = DocumentClassifier(dataset_path=_DATASET_PATH)
