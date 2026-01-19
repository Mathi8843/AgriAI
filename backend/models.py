from sqlalchemy import Column, String, Float
from database import Base
import uuid
from pydantic import BaseModel

# SQLAlchemy Models
class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, unique=True, index=True) # New
    password_hash = Column(String) # New
    name = Column(String)
    language = Column(String)
    location = Column(String)
    farm_size = Column(Float)
    soil_type = Column(String)
    irrigation_type = Column(String)
    primary_crop = Column(String)

# Pydantic Schemas

# Base Schema
class FarmerBase(BaseModel):
    name: str
    language: str
    location: str
    farm_size: float
    soil_type: str
    irrigation_type: str
    primary_crop: str

class FarmerCreate(FarmerBase):
    username: str # New
    password: str # New

class FarmerResponse(FarmerBase):
    id: str
    username: str

    class Config:
        orm_mode = True

class FarmerLogin(BaseModel):
    username: str
    password: str
