from sqlalchemy import Column, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..db.session import Base

def generate_case_id():
    return f"CIQ-{uuid.uuid4().hex[:8].upper()}"

class Entity(Base):
    __tablename__ = "entities"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    case_id = Column(String, unique=True, index=True, default=generate_case_id)
    
    # Identity
    company_name = Column(String, nullable=False)
    cin = Column(String, unique=True, index=True)
    pan = Column(String, index=True)
    sector = Column(String)
    
    # Loan Parameters (Placeholders for now)
    loan_type = Column(String)
    loan_amount = Column(Float)
    tenure_months = Column(Float)
    
    # Financial Snapshots (from Onboarding UI)
    annual_turnover = Column(Float)
    net_worth = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Metadata for downstream modules
    analysis_status = Column(String, default="Pillar_1_Complete")
    metadata_json = Column(JSON, default={})

    documents = relationship("Document", back_populates="entity")
    analysis = relationship("Analysis", back_populates="entity", uselist=False)
