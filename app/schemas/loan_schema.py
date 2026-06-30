from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.user_schema import UserBasicResponse
from app.schemas.device_schema import DeviceBasicResponse


class LoanCreate(BaseModel):
    user_id: int = Field(..., example=1)
    device_id: int = Field(..., example=1)

    model_config = {"from_attributes": True}


class LoanUpdate(BaseModel):
    status: Optional[str] = Field(None, example="overdue")
    return_date: Optional[datetime] = None

    model_config = {"from_attributes": True}


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: Optional[datetime]
    return_date: Optional[datetime]
    status: str

    model_config = {"from_attributes": True}


class LoanDetailResponse(BaseModel):
    loan_id: int
    status: str
    loan_date: Optional[datetime]
    return_date: Optional[datetime]
    user: UserBasicResponse
    device: DeviceBasicResponse

    model_config = {"from_attributes": True}