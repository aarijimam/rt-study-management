from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security.api_key import APIKey
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Dict
from app.core import models, schemas
from app.core.database import get_db
from app.core.security import get_api_key

router = APIRouter(
    prefix="/allergies",
    tags=["Allergies"]
)

@router.post("/")
def create_or_update_allergies(
    allergies: List[schemas.AllergyUpdate],  # AllergyUpdate contains allergyid
    db: Session = Depends(get_db),
    api_key: APIKey = Depends(get_api_key),
):
    if not allergies:
        return {"message": "No allergies provided"}

    # Separate new and existing records
    existing_allergies = [a for a in allergies if a.allergyid]  # Records with ID (update)
    new_allergies = [a.model_dump(exclude={"allergyid"}) for a in allergies if not a.allergyid]  # No ID (create)

    # **Bulk INSERT for new allergies** (auto-increment handles `allergyid`)
    if new_allergies:
        new_allergy_objects = [models.Allergy(**a) for a in new_allergies]
        db.add_all(new_allergy_objects)


    # **Bulk UPDATE existing allergies** (Use `allergyid` as key)
    if existing_allergies:
        db.bulk_update_mappings(models.Allergy, [a.model_dump() for a in existing_allergies])

    # **Extract provided IDs for deletion**
    provided_ids = {a.allergyid for a in existing_allergies if a.allergyid}

    # **Bulk DELETE for removed allergies**
    if provided_ids:
        db.query(models.Allergy).filter(~models.Allergy.allergyid.in_(provided_ids)).delete(synchronize_session=False)

    # Commit all changes
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error")

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