from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, example="Ana Pérez")
    email: EmailStr = Field(..., example="ana@sena.edu.co")
    phone: Optional[str] = Field(None, example="3001234567")

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}


class UserBasicResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}