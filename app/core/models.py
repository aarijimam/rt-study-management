from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from .database import Base


class Allergy(Base):
    __tablename__ = "allergy"

    allergyid = Column(Integer, primary_key=True, index=True)
    allergyname = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)

    __table_args__ = (
        UniqueConstraint('allergyname', 'type', name='unique_allergy'),
    )  # Ensures no duplicate (allergyname, type) pairs

