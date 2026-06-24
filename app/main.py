from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Importación corregida apuntando a tu carpeta 'middelwares'
from app.middelwares.request_middleware import SecurityAndLoggingMiddleware
from app.auth import auth_routes
from app.routes import user_routes, device_routes, loan_routes

# 1. Configurar Rate Limiting
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos",
    version="3.0.0"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. Agregar Middleware personalizado
app.add_middleware(SecurityAndLoggingMiddleware)

# 3. Configurar CORS (Fase 9)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Incluir los Routers
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)

@app.get("/", tags=["Root"])
def read_root():
    return {"status": "API device_systems activa y protegida"}