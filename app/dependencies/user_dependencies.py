from fastapi import HTTPException
from app.data.users_db import users_db


def get_user_or_404(user_id: int):

    for user in users_db:
        if user["id"] == user_id:
            return user

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )