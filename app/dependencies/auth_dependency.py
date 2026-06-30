from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Importaciones del proyecto - Asegúrate de que las rutas de tus archivos coincidan
from app.auth.security import decode_access_token
from app.database.connection import get_db
from app.models.user_model import User
from app.schemas.auth_schema import TokenData

# Este objeto le dice a Swagger que busque el token en el endpoint 'auth/login'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Valida el token JWT enviado en la cabecera, extrae el usuario de la 
    base de datos y verifica su existencia.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales o el token expiró",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Desencriptar el token JWT
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    email: str = payload.get("sub")
    role: str = payload.get("role")
    if email is None:
        raise credentials_exception
        
    token_data = TokenData(email=email, role=role)
    
    # Buscar el usuario dueño del token en la base de datos
    user = db.query(User).filter(User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
        
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Verifica que el usuario autenticado no esté marcado como inactivo.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El usuario se encuentra inactivo en el sistema"
        )
    return current_user

# --- Clase Controladora de Roles Jerárquicos ---

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes los permisos necesarios (rol insuficiente) para realizar esta acción"
            )
        return current_user

# Instancias listas para importar y usar como dependencias en las rutas
require_admin = RoleChecker(["admin"])
require_admin_or_support = RoleChecker(["admin", "support"])