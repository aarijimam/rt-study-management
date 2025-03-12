# filepath: /Users/aarijimam/Work/Risetech/demo-project/app/api/routes/allergy.py
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security.api_key import APIKey
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict
from sqlalchemy import tuple_
from app.core import models, schemas
from app.core.database import get_db
from sqlalchemy.dialects.postgresql import insert
from app.core.security import get_api_key
import logging

router = APIRouter(
    prefix="/allergies",
    tags=["Allergies"]
)

@router.post("/")
def create_or_update_allergies(
    allergies: List[schemas.AllergyUpdate],  # Schema uses allergyid
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    if not allergies:
        return {"message": "No allergies provided"}

    # Extract provided IDs (only for existing records)
    provided_ids = {a.allergyid for a in allergies if a.allergyid}

    # Fetch existing records in one query
    existing_allergies = db.query(models.Allergy).filter(models.Allergy.allergyid.in_(provided_ids)).all()
    existing_allergy_dict = {a.allergyid: a for a in existing_allergies}

    # Process each allergy in one loop
    for allergy in allergies:
        if allergy.allergyid and allergy.allergyid in existing_allergy_dict:
            # Update existing record
            existing_allergy = existing_allergy_dict[allergy.allergyid]
            existing_allergy.allergyname = allergy.allergyname
            existing_allergy.type = allergy.type
        else:
            # Insert new record
            db.add(models.Allergy(**allergy.model_dump(exclude={"allergyid"})))  # Exclude allergyid for new records

    # Delete records that are NOT in the received list
    db.query(models.Allergy).filter(~models.Allergy.allergyid.in_(provided_ids)).delete(synchronize_session=False)

    # Commit all changes at once
    db.commit()

    return {"message": "Allergy list updated successfully"}



# Get all Allergies
@router.get("/", response_model=List[schemas.AllergyResponse])
def get_all_allergies(db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    return db.query(models.Allergy).all()

# Get Allergy by ID
@router.get("/{allergy_id}", response_model=schemas.AllergyResponse)
def get_allergy_by_id(allergy_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    allergy = db.query(models.Allergy).filter(models.Allergy.allergyid == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")
    return allergy

# Delete an Allergy
@router.delete("/{allergy_id}")
def delete_allergy(allergy_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(get_api_key)):
    allergy = db.query(models.Allergy).filter(models.Allergy.allergyid == allergy_id).first()
    if not allergy:
        raise HTTPException(status_code=404, detail="Allergy not found")

    db.delete(allergy)
    db.commit()
    return {"message": "Allergy deleted successfully"}