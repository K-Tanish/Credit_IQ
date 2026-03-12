from sqlalchemy import Column, String, Float, JSON, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.session import Base

class Analysis(Base):
    __tablename__ = "analysis"

    id = Column(String, primary_key=True, index=True)
    case_id = Column(String, ForeignKey("entities.case_id"), unique=True)
    
    # The final credit score (0-100)
    credit_score = Column(Integer)
    
    # Breakdown of scores (Financial, Operational, Compliance, etc.)
    score_breakdown = Column(JSON)
    
    # Detailed findings/contradictions
    findings = Column(JSON)
    
    # SWOT analysis generated based on findings
    swot = Column(JSON)
    
    # Pillar 5: External data (News, Sentiment, etc.)
    external_intelligence = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to entity
    entity = relationship("Entity", back_populates="analysis")
