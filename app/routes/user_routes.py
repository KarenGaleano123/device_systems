from fastapi import APIRouter, HTTPException, Query, Response

from app.schemas.user_schema import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserPatch
)

from app.services.user_service import (
    get_all_users,
    get_user_by_id,
    create_user_service,
    update_user,
    patch_user,
    delete_user
)

router = APIRouter()


# GET TODOS LOS USUARIOS
@router.get(
    "/users",
    response_model=list[UserResponse],
    tags=["Users"],
    summary="Listar usuarios",
    description="Obtiene todos los usuarios registrados"
)
def get_users(
    response: Response,
    role: str = Query(None),
    is_active: bool = Query(None)
):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"

    results = get_all_users()

    if role:
        results = [
            user for user in results
            if user["role"] == role
        ]

    if is_active is not None:
        results = [
            user for user in results
            if user["is_active"] == is_active
        ]

    return results


# GET USUARIO POR ID
@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Consultar usuario",
    description="Obtiene un usuario por su ID"
)
def get_user(user_id: int, response: Response):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"

    user = get_user_by_id(user_id)

    if user:
        return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# POST CREAR USUARIO
@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    tags=["Users"],
    summary="Crear usuario",
    description="Crea un nuevo usuario"
)
def create_user(user: UserCreate, response: Response):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"

    users = get_all_users()

    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya existe"
            )

    return create_user_service(user)


# PUT ACTUALIZAR COMPLETO
@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=200,
    tags=["Users"],
    summary="Actualizar usuario completo",
    description="Reemplaza completamente los datos de un usuario"
)
def replace_user(
    user_id: int,
    user: UserUpdate
):

    users = get_all_users()

    for existing_user in users:
        if (
            existing_user["email"] == user.email
            and existing_user["id"] != user_id
        ):
            raise HTTPException(
                status_code=400,
                detail="El correo ya existe"
            )

    updated_user = update_user(
        user_id,
        user
    )

    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return updated_user


# PATCH ACTUALIZAR PARCIAL
@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=200,
    tags=["Users"],
    summary="Actualizar parcialmente usuario",
    description="Modifica uno o varios campos de un usuario"
)
def partial_update_user(
    user_id: int,
    user_data: UserPatch
):

    if not user_data.model_dump(exclude_unset=True):
        raise HTTPException(
            status_code=400,
            detail="Debe enviar al menos un campo para actualizar"
        )

    updated_user = patch_user(
        user_id,
        user_data
    )

    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return updated_user


# DELETE ELIMINAR USUARIO
@router.delete(
    "/users/{user_id}",
    status_code=200,
    tags=["Users"],
    summary="Eliminar usuario",
    description="Elimina un usuario por ID"
)
def remove_user(user_id: int):

    deleted = delete_user(user_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return {
        "message": "Usuario eliminado correctamente"
    }