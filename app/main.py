from fastapi import FastAPI

from app.database.connection import Base, engine
from app.models.user_model import User
from app.routes.user_routes import router as user_router

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Device Systems API",
    description="""
API REST para la gestión de usuarios del sistema Device Systems.

Permite:

- Crear usuarios
- Listar usuarios
- Consultar usuarios por ID
- Filtrar usuarios
- Actualizar usuarios
- Eliminar usuarios

Desarrollada con FastAPI, SQLAlchemy y Pydantic v2.
""",
    version="3.0.0",
    contact={
        "name": "Karen Galeano",
        "email": "Karen@example.com"
    }
)


@app.middleware("http")
async def add_custom_headers(request, call_next):

    response = await call_next(request)

    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "3.0"

    return response


@app.get("/")
def home():

    return {
        "message": "Bienvenido a Device Systems API"
    }


app.include_router(user_router)