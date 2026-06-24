import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict

class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico institucional o personal")
    password: str = Field(..., description="Contraseña de acceso segura")
    role: str = Field(default="user", description="Rol asignado: admin, support, user")

    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres.')
        if not re.search(r'[A-Z]', v):
            raise ValueError('La contraseña debe incluir al menos una letra mayúscula.')
        if not re.search(r'[a-z]', v):
            raise ValueError('La contraseña debe incluir al menos una letra minúscula.')
        if not re.search(r'[0-9]', v):
            raise ValueError('La contraseña debe incluir al menos un número.')
        if ' ' in v:
            raise ValueError('La contraseña no debe contener espacios en blanco.')
        return v

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        allowed_roles = ['admin', 'support', 'user']
        if v not in allowed_roles:
            raise ValueError(f'Rol no permitido. Debe ser uno de: {", ".join(allowed_roles)}')
        return v

class UserLogin(BaseModel):
    username: str = Field(..., description="Corresponde al email del usuario")
    password: str = Field(..., description="Contraseña en texto plano")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None

# Schema para responder los datos de usuario de forma segura sin exponer la contraseña
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)