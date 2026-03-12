from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class EntityBase(BaseModel):
    company_name: str
    # Accept CIN/PAN with lenient validation — uppercase, strip spaces
    cin: str
    pan: str
    sector: Optional[str] = None
    annual_turnover: Optional[float] = 0.0
    net_worth: Optional[float] = 0.0
    loan_type: Optional[str] = "term_loan"
    loan_amount: Optional[float] = 0.0
    tenure_months: Optional[int] = 12

    @field_validator('cin')
    @classmethod
    def normalise_cin(cls, v: str) -> str:
        v = v.strip().upper().replace(' ', '')
        if not v:
            raise ValueError('CIN cannot be empty')
        return v

    @field_validator('pan')
    @classmethod
    def normalise_pan(cls, v: str) -> str:
        v = v.strip().upper().replace(' ', '')
        if not v:
            raise ValueError('PAN cannot be empty')
        return v

    @field_validator('company_name')
    @classmethod
    def company_name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Company name cannot be empty')
        return v.strip()


class EntityCreate(EntityBase):
    pass


class EntityUpdate(BaseModel):
    company_name: Optional[str] = None
    sector: Optional[str] = None
    loan_amount: Optional[float] = None
    analysis_status: Optional[str] = None


class EntityResponse(EntityBase):
    id: str
    case_id: str
    created_at: datetime
    analysis_status: str

    class Config:
        from_attributes = True
