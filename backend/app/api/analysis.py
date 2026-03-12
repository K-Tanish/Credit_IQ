from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.session import get_db
from ..services.analysis_service import analysis_engine
from ..models.entity import Entity
from ..schemas.analysis import AnalysisResponse
from ..services.report_service import report_service
from fastapi.responses import Response

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.get("/{case_id}", response_model=AnalysisResponse)
async def get_case_analysis(case_id: str, db: Session = Depends(get_db)):
    """
    Trigger Pillar 3 Triangulation and return the credit risk profile.
    """
    # Verify entity exists
    entity = db.query(Entity).filter(Entity.case_id == case_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Case ID not found")
        
    # Run the engine
    try:
        analysis = await analysis_engine.run_analysis(db, case_id)
        return analysis
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Triangulation failed: {str(e)}")

@router.get("/{case_id}/report")
async def get_case_report(case_id: str, db: Session = Depends(get_db)):
    """
    Generate and download the professional PDF Credit Memo.
    """
    entity = db.query(Entity).filter(Entity.case_id == case_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Case ID not found")
        
    analysis = await analysis_engine.run_analysis(db, case_id)
    
    from ..models.document import Document
    docs = db.query(Document).filter(Document.case_id == case_id, Document.status == "approved").all()

    # Map models to dicts for the service
    analysis_dict = {
        "credit_score": analysis.credit_score,
        "swot": analysis.swot,
        "findings": analysis.findings,
        "external_intelligence": analysis.external_intelligence,
        "docs": docs
    }
    entity_dict = {
        "company_name": entity.company_name,
        "case_id": entity.case_id,
        "sector": entity.sector,
        "cin": entity.cin,
        "pan": entity.pan,
        "loan_amount": entity.loan_amount,
        "loan_type": entity.loan_type,
        "turnover": entity.annual_turnover,
        "net_worth": entity.net_worth
    }
    
    try:
        pdf_content = report_service.generate_credit_memo(analysis_dict, entity_dict)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"PDF Generation failed: {str(e)}")
    
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Credit_IQ_Memo_{case_id}.pdf"}
    )
