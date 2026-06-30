from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
    name: str = Field(..., min_length=2, example="Laptop Lenovo ThinkPad")
    serial_number: str = Field(..., example="LEN-2024-001")
    device_type: str = Field(..., example="laptop")
    brand: Optional[str] = Field(None, example="Lenovo")
    is_available: bool = Field(True)

    model_config = {"from_attributes": True}


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    serial_number: Optional[str] = None
    device_type: Optional[str] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None

    model_config = {"from_attributes": True}


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str
    brand: Optional[str]
    is_available: bool
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}


class DeviceBasicResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    model_config = {"from_attributes": True}