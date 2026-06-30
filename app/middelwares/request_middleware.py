import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityAndLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Generar o propagar X-Request-ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Guardar en el estado de la petición por si se necesita leer después
        request.state.request_id = request_id
        
        # Continuar la ejecución de la petición
        response = await call_next(request)
        
        # Calcular el tiempo de procesamiento
        process_time = time.time() - start_time
        
        # Inyectar cabeceras requeridas
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        response.headers["X-Request-ID"] = request_id
        
        # Registro básico en consola para auditoría
        print(f"[{request.method}] {request.url.path} - Status: {response.status_code} - ID: {request_id} - Time: {process_time:.4f}s")
        
        return response