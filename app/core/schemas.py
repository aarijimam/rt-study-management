from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

class AllergyBase(BaseModel):
    allergyname: str = Field(..., description="The name of the allergy", example="Peanuts")
    type: str = Field(..., description="The type of the allergy", example="Food")

class AllergyCreate(AllergyBase):
    pass

class AllergyResponse(AllergyBase):
    allergyid: int = Field(..., description="The unique identifier of the allergy", example=1)

    class ConfigDict:
        from_attributes = True

class AllergyUpdate(BaseModel):
    allergyid: Optional[int] = None  # Using allergyid instead of id
    allergyname: str
    type: str