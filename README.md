# CREDIT_IQ: Cognitive Appraisal & Memory System

## Introduction

CREDIT_IQ is a professional credit intelligence platform designed to automate the credit appraisal lifecycle for corporate borrowers. The system leverages artificial intelligence to ingest, classify, and cross-validate financial data from multiple sources, providing an auditable and explainable risk score.


## Functional Pillars

### 1. Entity Onboarding
The system initiates the appraisal process by capturing core entity details (CIN, PAN, Sector) and specific loan requirements. This creates a centralized record for all downstream analysis.

### 2. Intelligent Document Ingestion
Automated classification of financial documents (GST returns, Bank Statements, ITRs, etc.) using semantic similarity models. A human-in-the-loop interface ensures classification accuracy before data extraction.

### 3. Triangulation and Contradiction Detection
A specialized engine cross-references data points across disparate sources to identify inconsistencies. It flags discrepancies such as revenue mismatches between GST filings and bank records to mitigate fraud risk.

### 4. Automated Extraction and Schema Mapping
High-precision extraction of semi-structured data from PDFs and spreadsheets. The system maps extracted fields to a standardized schema, allowing for consistent financial analysis across different document formats.

### 5. AI-Powered Analysis and Reporting
Synthesizes primary data and external intelligence into a comprehensive credit memo.
- **Risk Scoring**: Utilizes gradient boosting models with SHAP-based explainability.
- **SWOT Analysis**: An AI agent generates structured insights based on document content and financial findings.
- **Reporting**: Automated generation of a professional PDF Credit Intelliigence Report.

## User Interface 
<img width="1280" height="1687" alt="Executive SWOT   Final Report - Finalized" src="https://github.com/user-attachments/assets/df3eaf5a-ada5-453c-9452-3c40050951db" />
<img width="1280" height="1222" alt="Entity Onboarding (Beige)" src="https://github.com/user-attachments/assets/76c44e70-5c24-4f46-80fb-c7bc1de89265" />
<img width="1280" height="1024" alt="Data Ingestion (Beige)" src="https://github.com/user-attachments/assets/36fbced2-b3db-4a37-940e-ee8feb836b02" />
<img width="1280" height="1055" alt="Command Center" src="https://github.com/user-attachments/assets/55135811-24eb-46d8-bcb7-97d1b6e8c031" />
<img width="1280" height="1024" alt="Processing - Beige Theme" src="https://github.com/user-attachments/assets/e273b8ce-70c6-4c98-8099-75d062905187" />

## Technical Architecture

| Component | Technology |
|---|---|
| **Backend** | FastAPI, SQLAlchemy, Pydantic |
| **Frontend** | React, Vite, TailwindCSS |
| **NLP & AI** | LangChain, Anthropic Claude, OpenAI gpt-4o |
| **Data Processing** | Pandas, PyMuPDF, Tesseract OCR |
| **Scoring** | XGBoost, SHAP |
| **Reporting** | ReportLab |

## Installation and Setup

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- PostgreSQL

### Local Development

#### Backend Configuration
1. Navigate to the `backend` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables in a `.env` file based on `.env.example`.
4. Run the application:
   ```bash
   python -m app.main
   ```

#### Frontend Configuration
1. Navigate to the root directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

### Docker Deployment
The project includes a `docker-compose.yml` for containerized deployment:
```bash
docker-compose up --build
```

### Deploy to Vercel

Vercel hosts the Vite frontend. The FastAPI backend, PostgreSQL database, and durable upload storage are deployed separately using the included `render.yaml` Blueprint. The backend loads a SentenceTransformer model and requires Tesseract plus persistent storage, so it is not deployed as a Vercel serverless function. The Render API instance, persistent disk, and database are paid resources; review their current costs before applying the Blueprint.

1. Push this repository to GitHub, GitLab, or Bitbucket.
2. In [Vercel](https://vercel.com/), select **Add New** > **Project**, import the repository, and deploy it. Use the repository root as the project root and the Vite framework preset. `vercel.json` configures `npm run build`, publishes `dist`, and sends frontend routes to `index.html`.
3. Copy the deployed production URL, for example `https://credit-iq.vercel.app`.
4. In [Render](https://render.com/), select **New** > **Blueprint**, connect the same repository and branch, review the API and database resources, then apply the Blueprint. When prompted for `CORS_ORIGINS`, enter the Vercel production origin exactly, without a trailing slash. Render builds the API and database; wait for the API service to become healthy.
5. Copy the API service's public base URL from Render, such as `https://credit-iq-api.onrender.com`. Confirm that `<API_URL>/health` returns `{"status":"healthy"}`.
6. In Vercel, open the project **Settings** > **Environment Variables**. Add `VITE_API_URL` with the Render API base URL (no trailing slash), at least for **Production**, then save.
7. Open **Deployments**, redeploy the latest production deployment so Vite builds with `VITE_API_URL`, and test onboarding, document upload, and analysis.
8. To enable AI-generated SWOT analysis, add `ANTHROPIC_API_KEY` and/or `OPENAI_API_KEY` to the `credit-iq-api` service's **Environment** settings in Render, then redeploy the API. Without either key, the app uses its built-in fallback analysis.

For Vercel preview deployments, add each preview origin to Render's `CORS_ORIGINS` (comma-separated) and redeploy the API. Vite embeds `VITE_API_URL` at build time, so changing it also requires a new frontend deployment.

**Security note:** this prototype does not implement user authentication or authorization. CORS only restricts browser origins and does not protect the API from direct requests. Do not upload real customer or confidential credit documents until authentication, authorization, and an appropriate data-protection review are in place.

## Project Structure

- `backend/`: FastAPI application, database models, and AI services.
- `src/`: React frontend source code.
- `docs/`: Supplemental project documentation.
- `uploads/`: Local storage for ingested documents (git-ignored).

## Documentation

For more detailed information, please refer to the files in the `docs/` directory:
- [Project Overview](docs/Project_Overview.md)
- [Implementation Checklist](docs/Implementation_Checklist.md)
