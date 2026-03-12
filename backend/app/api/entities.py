from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.session import get_db
from ..models.entity import Entity
from ..schemas.entity import EntityCreate, EntityResponse

router = APIRouter(prefix="/entities", tags=["Entities"])

@router.post("/", response_model=EntityResponse, status_code=status.HTTP_201_CREATED)
def create_entity(entity_in: EntityCreate, db: Session = Depends(get_db)):
    # Check if CIN already exists
    existing = db.query(Entity).filter(Entity.cin == entity_in.cin).first()
    if existing:
        return existing # Return existing if already onboarded for this flow

    db_entity = Entity(**entity_in.model_dump())
    db.add(db_entity)
    db.commit()
    db.refresh(db_entity)
    return db_entity

@router.get("/{case_id}", response_model=EntityResponse)
def get_entity(case_id: str, db: Session = Depends(get_db)):
    entity = db.query(Entity).filter(Entity.case_id == case_id).first()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity

@router.get("/", response_model=List[EntityResponse])
def list_entities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Entity).offset(skip).limit(limit).all()
