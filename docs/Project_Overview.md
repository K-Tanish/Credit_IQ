# Credit_IQ — Project Overview

## Problem Statement

Credit appraisal in India's NBFC and banking sector is slow, labour-intensive, and dangerously dependent on manually prepared documents that are trivially easy to manipulate. A credit analyst today must:

- Compare GST returns against bank credits against ITR declarations — three separate data sources that are rarely cross-checked programmatically.
- Read through dense shareholding tables and ALM reports to detect promoter pledge concentrations or liquidity mismatches.
- Conduct manual web searches on MCA21, eCourts, CIBIL, and news outlets to flag litigation risk.
- Rely on subjective, individual judgment for a final recommendation that may carry crore-scale consequences.

This entire process takes **3–15 business days** per appraisal and is highly susceptible to both human error and document fraud.

---

## Solution: Credit_IQ (CAMS — Cognitive Appraisal & Memory System)

Credit_IQ is an **AI-native credit intelligence platform** that automates and augments the full credit appraisal pipeline for Indian corporate borrowers. It ingests raw financial documents, cross-validates data across all available sources, runs a structured risk-scoring engine, and produces an auditable, explainable credit recommendation — in minutes, not days.

---

## Core Functional Pillars

### Pillar 1 — Entity Onboarding
- Collects basic entity identity (CIN, PAN, Company Name, Sector) and loan request parameters (type, amount, tenure).
- Acts as the hard gate for the pipeline — creates a unique `Case ID` that all downstream modules reference.
- Enables sector tagging which drives benchmarking throughout the analysis (e.g. comparing EBITDA margins against sector medians).

### Pillar 2 — Intelligent Document Uploading
- Accepts raw, unstructured uploads: PDFs, scanned documents, Excel sheets, Word files.
- Uses a **BERT-based zero-shot classification model** (fine-tuned on 14 Indian financial document classes) to automatically identify and categorise each uploaded file — GSTR-3B, Bank Statement, ALM Report, ITR, Sanction Letter, Shareholding Pattern, etc. — without requiring manual labelling.
- Provides a **Human-in-the-Loop (HITL) classification review**: the user can approve, deny, or manually override any auto-classification before extraction proceeds.

### Pillar 3 — The Contradiction Engine
The core differentiator. This module performs **automated triangulation** across all collected data sources to detect financial inconsistencies that are red flags for fraud or misrepresentation.

Key checks performed:

| Check Name | Description |
|---|---|
| **Red Triangle Mismatch** | GST-declared revenue vs. Bank credits vs. ITR revenue — all three must align within a threshold. Any divergence of >25% without explanation is flagged. |
| **ITC Leakage Signal** | Claimed Input Tax Credit in GSTR-3B compared against ITC available in GSTR-2A. A ratio >1.2 signals a potential circular trading arrangement. |
| **OD Window Dressing** | Bank statement analysis for large, unexplained credits arriving within 3–5 days of the statement cut-off date, artificially inflating apparent liquidity. |
| **Promoter Pledge Concentration** | Detects >50% promoter holding pledged to lenders in the Shareholding Pattern. |
| **ALM Bucket Mismatch** | Asset-liability maturity mismatch beyond sector norms — signalling potential rollover or liquidity risk. |
| **Cross-Default Flag** | Detects simultaneous defaults or breach of covenants referenced in existing sanction letters. |

### Pillar 4 — Automated Extraction & Schema Mapping
The operational core of data structuring.

- **Auto-Classification**: Documents are automatically identified and categorised (from Pillar 2) before extraction begins.
- **Human-in-the-Loop Review**: Credit officers can approve, reject, or edit the auto-classification of each document prior to data extraction — ensuring human accountability before any data enters the system.
- **Dynamic Schema Configuration**: Users can define or configure the output schema for each document type. For example, a credit officer can specify that from a Bank Statement, they want `Date`, `Debit`, `Credit`, `Closing Balance`, and `OD Limit` as named columns — and the system will map extracted data to those exact field names.
- **High-Precision Extraction**: Using a two-pass OCR pipeline (Tesseract + PyMuPDF for native PDFs), the system ingests tabular and semi-structured data from raw documents and maps it precisely to the user-defined schema. Field-level confidence scores are surfaced for any value the model is uncertain about, triggering a manual review prompt.
- **User-Defined Adjustments**: For any extracted value, the user can directly correct it in the interface. Corrections feed back into the model as fine-tuning signals for future accuracy improvement.

### Pillar 5 — Pre-Cognitive Secondary Analysis & Reporting
The intelligence synthesis layer. Once primary data is extracted and cross-validated, the platform conducts a wide-spectrum secondary analysis.

- **Secondary Research (360° Intelligence Gathering)**:
  - **News & Sentiment**: Programmatic scraping of financial news sources and search engines for the entity, its promoters, and associated sector/sub-sector.
  - **Legal & Litigation**: Automated queries against eCourts, NCLT, DRT, and SEBI enforcement databases.
  - **Market & Macro Trends**: Sector-level performance data, macro-economic indicators, and RBI/SEBI regulatory announcements relevant to the borrower's industry.
  - **MCA21 V3**: Director cross-holdings, related-party transactions, annual filing compliance status.

- **Triangulation with Primary Data**: All secondary research findings are programmatically cross-referenced against the extracted primary data. Divergences (e.g. news reports of a factory fire contradicting reported production capacity) are surfaced as additional contradiction flags.

- **Explainable Prediction / Recommendation Engine**:
  - A structured feature vector (DSCR, EBITDA margin, leverage ratio, ITC gap, litigation score, promoter pledge ratio, news sentiment score, etc.) is assembled and passed into a trained **XGBoost Gradient Boosting classifier**.
  - Outputs a **Probability of Default (PD)** percentage and a composite **CAMS Score (0–100)**.
  - **SHAP (SHapley Additive exPlanations)** values provide a fully auditable, factor-by-factor justification for every point of the score — meeting regulatory explainability standards.
  - A clear **Reasoning Engine narrative** is generated by an LLM, translating the SHAP outputs into plain-English explanations a credit officer can cite directly in their appraisal file.

- **SWOT Analysis & Final Investment Report**:
  - A structured **SWOT analysis** (Strengths, Weaknesses, Opportunities, Threats) is auto-generated from the combination of primary extracted data, contradiction flags, secondary research, and scoring outputs.
  - A **downloadable Final Investment Report (PDF)** is generated, presenting all findings in a clean, consumable format — including: entity summary, contradiction findings, SHAP waterfall, SWOT table, secondary research highlights, and the final recommendation with rationale.
  - The report is structured to be directly shareable with credit committees, investors, and regulators without requiring further manual editing.

---

## Technology Stack

| Layer | Technology |
|---|---|
| **Document Classification** | `sentence-transformers` (all-MiniLM-L6-v2), zero-shot cosine similarity |
| **OCR & Extraction** | Tesseract OCR, PyMuPDF |
| **Schema Mapping & Validation** | Custom field-mapping engine, Pydantic |
| **Contradiction Engine** | Rule-based cross-validation logic (Python) |
| **Risk Scoring** | XGBoost, SHAP |
| **Secondary Research** | DuckDuckGo Search API, BeautifulSoup, LangChain |
| **Reasoning & Report Generation** | Anthropic Claude / OpenAI GPT-4o, LangChain |
| **PDF Report Generation** | ReportLab / WeasyPrint |
| **Backend API** | FastAPI (Python), Uvicorn |
| **Data Processing** | Pandas, OpenPyXL |

---

## What Makes This Different

1. **Triangulation, not just extraction**: Most tools extract — Credit_IQ cross-validates across sources to identify what doesn't match, flagging fraud signals that would otherwise go undetected.
2. **User-controlled schema**: Credit officers define the exact structure of what gets extracted, making the system adaptable to any document format without retraining.
3. **360-degree intelligence**: Primary document data is enriched with live secondary research — news, legal, macro — giving the analyst a complete picture, not just what the borrower chose to submit.
4. **Explainable by default**: Every score point is attributed via SHAP and narrated in plain English, satisfying both internal governance and regulatory audit requirements.
5. **Human stays in control**: Classification, schema design, extraction corrections, and report approval all pass through the human operator. The system augments the analyst, it does not replace them.
