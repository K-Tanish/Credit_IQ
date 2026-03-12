from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class AnalysisResponse(BaseModel):
    case_id: str
    credit_score: int
    score_breakdown: Dict[str, int]
    findings: List[Dict[str, Any]]
    swot: Dict[str, List[str]]
    external_intelligence: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
