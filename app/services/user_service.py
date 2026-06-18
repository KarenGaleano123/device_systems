from sqlalchemy.orm import Session
from app.models.user_model import User


# Crear usuario
def create_user(db: Session, user_data):

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        role=user_data.role,
        is_active=user_data.is_active
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Obtener todos los usuarios
def get_users(db: Session):

    return db.query(User).all()


# Obtener usuario por ID
def get_user_by_id(db: Session, user_id: int):

    return db.query(User).filter(
        User.id == user_id
    ).first()


# Obtener usuario por email
def get_user_by_email(
    db: Session,
    email: str
):

    return db.query(User).filter(
        User.email == email
    ).first()


# Actualización completa (PUT)
def update_user(
    db: Session,
    user_id: int,
    user_data
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        return None

    user.name = user_data.name
    user.email = user_data.email
    user.role = user_data.role
    user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return user


# Actualización parcial (PATCH)
def patch_user(
    db: Session,
    user_id: int,
    update_data: dict
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        return None

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user


# Eliminar usuario
def delete_user(
    db: Session,
    user_id: int
):

    user = get_user_by_id(
        db,
        user_id
    )

    if not user:
        return False

    db.delete(user)
    db.commit()

    return True


# Filtrar por rol
def get_users_by_role(
    db: Session,
    role: str
):

    return db.query(User).filter(
        User.role == role
    ).all()


# Filtrar por estado
def get_users_by_status(
    db: Session,
    is_active: bool
):

    return db.query(User).filter(
        User.is_active == is_active
    ).all()


# Ordenar por nombre
def order_users_by_name(
    db: Session
):

    return db.query(User).order_by(
        User.name
    ).all()


# Ordenar por fecha
def order_users_by_date(
    db: Session
):

    return db.query(User).order_by(
        User.created_at
    ).all()