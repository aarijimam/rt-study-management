from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from app.core import models, schemas
from app.core.database import get_db


router = APIRouter(
    prefix="/allergies",
    tags=["Allergies"]
)

# Create new Allergies
@router.post("/", response_model=Dict[str, List[schemas.AllergyResponse]])
def create_allergies(allergies: List[schemas.AllergyCreate], db: Session = Depends(get_db)):
    added_allergies = []
    existing_allergies = []
    for allergy in allergies:
        # Check if the Allergy already exists (Unique Constraint on Name & Type)
        existing_allergy = db.query(models.Allergy).filter(
            models.Allergy.allergyname == allergy.allergyname,
            models.Allergy.type == allergy.type
        ).first()
        if existing_allergy:
            existing_allergies.append(existing_allergy)
        else:
            new_allergy = models.Allergy(**allergy.dict())
            db.add(new_allergy)
            db.commit()
            db.refresh(new_allergy)
            added_allergies.append(new_allergy)
    
    return {"added": added_allergies, "existing": existing_allergies}

# Get all Allergies
@router.get("/", response_model=List[schemas.AllergyResponse])
def get_all_allergies(db: Session = Depends(get_db)):
    return db.query(models.Allergy).all()

# Get Allergy by ID
@router.get("/{allergy_id}", response_model=schemas.AllergyResponse)
def get_allergy_by_id(allergy_id: int, db: Session = Depends(get_db)):
    allergy = db.query(models.Allergy).filter(models.Allergy.AllergyID == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return allergy

# Delete an Allergy
@router.delete("/{allergy_id}")
def delete_allergy(allergy_id: int, db: Session = Depends(get_db)):
    allergy = db.query(models.Allergy).filter(models.Allergy.AllergyID == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")

    db.delete(allergy)
    db.commit()
    return {"message": "Allergy deleted successfully"}
