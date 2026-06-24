from fastapi import FastAPI
from app.database.connection import Base, engine
from app.models import User, Device, Loan
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

app = FastAPI(
    
    title="device_systems API",
    description="""
## Sistema de Gestión de Usuarios, Dispositivos y Préstamos

API REST construida con **FastAPI** y **SQLAlchemy** que permite:

- Gestionar **usuarios** del sistema
- Registrar **dispositivos** tecnológicos
- Administrar **préstamos** de dispositivos a usuarios
- Consultar información relacionada mediante **JOINs**
- Filtrar por tipo, estado, usuario o dispositivo

### Recursos disponibles:
- `/users` — CRUD completo de usuarios
- `/devices` — CRUD completo de dispositivos con filtros
- `/loans` — Gestión de préstamos con consultas avanzadas
    """,
    version="2.0.0",
    contact={
        "name": "SENA - Tecnólogo en ADSO",
        "email": "aprendiz@sena.edu.co"
    }
)



from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)

@app.get("/", tags=["Root"], summary="Bienvenida a la API")
def root():
    return {
        "message": "Bienvenido a device_systems API v2.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "recursos": ["/users", "/devices", "/loans"]
    }