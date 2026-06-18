from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.dependencies.database_dependency import get_db

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserPatch
)

from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    get_user_by_email,
    update_user,
    patch_user,
    delete_user,
    get_users_by_role,
    get_users_by_status
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# GET TODOS LOS USUARIOS
@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios o permite filtrar por rol y estado."
)
def list_users(
    role: str | None = Query(None),
    is_active: bool | None = Query(None),
    db: Session = Depends(get_db)
):

    if role:
        return get_users_by_role(db, role)

    if is_active is not None:
        return get_users_by_status(db, is_active)

    return get_users(db)


# GET USUARIO POR ID
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Consultar usuario",
    description="Obtiene un usuario por ID."
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return user


# POST CREAR USUARIO
@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Crea un nuevo usuario."
)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El correo ya existe"
        )

    return create_user(
        db,
        user
    )


# PUT ACTUALIZAR COMPLETO
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Actualiza completamente un usuario."
)
def replace_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):

    existing_user = get_user_by_id(
        db,
        user_id
    )

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    email_owner = get_user_by_email(
        db,
        user_data.email
    )

    if (
        email_owner and
        email_owner.id != user_id
    ):
        raise HTTPException(
            status_code=400,
            detail="El correo ya existe"
        )

    return update_user(
        db,
        user_id,
        user_data
    )


# PATCH ACTUALIZAR PARCIAL
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar parcialmente usuario",
    description="Actualiza parcialmente un usuario."
)
def partial_update_user(
    user_id: int,
    user_data: UserPatch,
    db: Session = Depends(get_db)
):

    update_data = user_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar"
        )

    existing_user = get_user_by_id(
        db,
        user_id
    )

    if not existing_user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    if "email" in update_data:

        email_owner = get_user_by_email(
            db,
            update_data["email"]
        )

        if (
            email_owner and
            email_owner.id != user_id
        ):
            raise HTTPException(
                status_code=400,
                detail="El correo ya existe"
            )

    return patch_user(
        db,
        user_id,
        update_data
    )


# DELETE ELIMINAR USUARIO
@router.delete(
    "/{user_id}",
    status_code=200,
    summary="Eliminar usuario",
    description="Elimina un usuario."
)
def remove_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_user(
        db,
        user_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "message": "Usuario eliminado correctamente"
    }