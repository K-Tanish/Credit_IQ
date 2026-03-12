from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentBase(BaseModel):
    filename: str
    file_type: Optional[str] = None
    file_size: Optional[float] = None
    auto_label: Optional[str] = None
    user_label: Optional[str] = None
    confidence_score: Optional[float] = None
    status: str = "uploaded"
    case_id: Optional[str] = None
    extracted_text: Optional[str] = None
    extracted_data: Optional[dict] = None


class DocumentCreate(DocumentBase):
    entity_id: str
    file_path: str


class DocumentUpdate(BaseModel):
    """HITL review payload: override AI label and/or advance the status."""
    user_label: Optional[str] = None
    status: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: str
    entity_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DocumentStatusResponse(BaseModel):
    """Lightweight status-poll response."""
    id: str
    filename: str
    status: str
    auto_label: Optional[str] = None
    user_label: Optional[str] = None
    confidence_score: Optional[float] = None

    class Config:
        from_attributes = True
