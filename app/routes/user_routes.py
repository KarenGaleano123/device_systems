from fastapi import APIRouter, HTTPException, Query, Response
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter()

# Base de datos simulada
users_db = [
    {
        "id": 1,
        "name": "Karen",
        "email": "karen@gmail.com",
        "role": "admin",
        "is_active": True
    },
    {
        "id": 2,
        "name": "Carlos",
        "email": "carlos@gmail.com",
        "role": "support",
        "is_active": False
    }
]


# GET TODOS LOS USUARIOS
@router.get("/users", response_model=list[UserResponse])
def get_users(
    response: Response,
    role: str = Query(None),
    is_active: bool = Query(None)
):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    results = users_db

    # Filtrar por rol
    if role:
        results = [user for user in results if user["role"] == role]

    # Filtrar por estado
    if is_active is not None:
        results = [
            user for user in results
            if user["is_active"] == is_active
        ]

    return results


# GET USUARIO POR ID
@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, response: Response):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    for user in users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )


# POST CREAR USUARIO
@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, response: Response):

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

    # Validar correo duplicado
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="El correo ya existe"
            )

    new_user = {
        "id": len(users_db) + 1,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

    users_db.append(new_user)

    return new_user