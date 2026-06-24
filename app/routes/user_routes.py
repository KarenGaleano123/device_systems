from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.dependencies.database_dependency import get_db
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserResponse], summary="Listar todos los usuarios")
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_all_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID")
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Crear usuario")
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_data)


@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar usuario completo")
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, user_data)


@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar usuario parcialmente")
def patch_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user(db, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar usuario")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_service.delete_user(db, user_id)