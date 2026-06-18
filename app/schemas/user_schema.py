from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional


# Modelo base
class UserBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool


# Crear usuario (POST)
class UserCreate(UserBase):
    pass


# Actualización completa (PUT)
class UserUpdate(UserBase):
    pass


# Actualización parcial (PATCH)
class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[Literal["admin", "support", "user"]] = None
    is_active: Optional[bool] = None


# Respuesta de usuario
class UserResponse(UserBase):
    id: int

    model_config = {
        "from_attributes": True
    }