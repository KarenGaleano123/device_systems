from app.data.users_db import users_db


# Obtener todos los usuarios
def get_all_users():
    return users_db


# Obtener usuario por ID
def get_user_by_id(user_id: int):

    for user in users_db:
        if user["id"] == user_id:
            return user

    return None


# Crear usuario
def create_user_service(user):

    new_user = {
        "id": len(users_db) + 1,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

    users_db.append(new_user)

    return new_user


# Actualización completa (PUT)
def update_user(user_id: int, user_data):

    user = get_user_by_id(user_id)

    if not user:
        return None

    user["name"] = user_data.name
    user["email"] = user_data.email
    user["role"] = user_data.role
    user["is_active"] = user_data.is_active

    return user


# Actualización parcial (PATCH)
def patch_user(user_id: int, data):

    user = get_user_by_id(user_id)

    if not user:
        return None

    update_data = data.model_dump(exclude_unset=True)

    user.update(update_data)

    return user


# Eliminar usuario (DELETE)
def delete_user(user_id: int):

    user = get_user_by_id(user_id)

    if not user:
        return False

    users_db.remove(user)

    return True