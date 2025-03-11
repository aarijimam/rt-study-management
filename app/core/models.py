from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base


class Allergy(Base):
    __tablename__ = "allergy"

    allergyid = Column(Integer, primary_key=True, index=True)
    allergyname = Column(String(255), nullable=False)
    type = Column(String(255), nullable=False)

    __table_args__ = ({"sqlite_autoincrement": True},)  # Ensure unique (AllergyName, Type)


