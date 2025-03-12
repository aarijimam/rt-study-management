from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class AllergyBase(BaseModel):
    allergyname: str
    type: str

class AllergyCreate(AllergyBase):
    pass

class AllergyResponse(AllergyBase):
    allergyid: int

    class ConfigDict:
        from_attributes = True
