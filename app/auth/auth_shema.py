from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional


# =========================
# REGISTRO DE USUARIOS
# =========================

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres."
            )
        return value


# =========================
# RESPUESTA DE USUARIO
# =========================

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True


# =========================
# TOKEN JWT
# =========================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


# =========================
# UPDATE COMPLETO (PUT)
# =========================

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    role: str
    is_active: bool


# =========================
# UPDATE PARCIAL (PATCH)
# =========================

class UserPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None