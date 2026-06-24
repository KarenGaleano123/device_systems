from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user_model import User
from app.schemas.auth_schema import UserResponse
from app.dependencies.auth_dependency import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])

# REQUERIMIENTO: GET /users -> Solo usuarios autenticados
@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Retorna la lista de todos los usuarios del sistema.
    Requiere un token JWT válido. El campo 'hashed_password' queda automáticamente oculto.
    """
    users = db.query(User).all()
    return users

# REQUERIMIENTO: GET /users/{user_id} -> Solo usuarios autenticados
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Busca y retorna un usuario por su ID.
    Requiere un token JWT válido.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user