from sqlalchemy import Column, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from ..db.session import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    entity_id = Column(String, ForeignKey("entities.id"), nullable=False)
    case_id = Column(String, index=True) # Redundant but useful for fast queries
    
    # File Metadata
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String) # MIME type
    file_size = Column(Float) # In bytes
    
    # Classification Info
    auto_label = Column(String) # Model predicted label
    user_label = Column(String) # Human approved/overridden label
    confidence_score = Column(Float)
    
    # Extract Info (Pillar 4)
    extracted_text = Column(String)
    extracted_data = Column(JSON, default={})
    
    status = Column(String, default="uploaded") # uploaded, classified, pending_review, approved, rejected
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship back to entity
    entity = relationship("Entity", back_populates="documents")

# Update Entity model to include relationship
# Note: In a real project we'd use a single models file or carefully handle imports.
# I will update entity.py next.
