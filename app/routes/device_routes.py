from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.device_model import Device  # Asegúrate de que el nombre coincida con tu modelo existente
from app.dependencies.auth_dependency import require_admin, require_admin_or_support

router = APIRouter(prefix="/devices", tags=["Devices"])

# Nota: El schema de entrada (ej: DeviceCreate) y salida (ej: DeviceResponse) 
# dependerá de cómo los llamaste en tu Fase 1. Ajústalos si es necesario.

# REQUERIMIENTO: POST /devices -> Admin o support
@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin_or_support)])
def create_device(device_data: dict, db: Session = Depends(get_db)):
    """
    Registra un nuevo dispositivo en el sistema.
    Restringido a roles: admin, support. Usuarios normales recibirán 403 Forbidden.
    """
    # Tu lógica original de la Fase 1 va aquí abajo:
    # new_device = Device(**device_data.model_dump())
    # db.add(new_device)
    # db.commit()
    return {"message": "Dispositivo creado con éxito (Validado por rol Admin/Support)", "data": device_data}

# REQUERIMIENTO: PUT /devices/{device_id} -> Admin o support
@router.put("/{device_id}", dependencies=[Depends(require_admin_or_support)])
def update_device(device_id: int, device_data: dict, db: Session = Depends(get_db)):
    """
    Modifica las propiedades de un dispositivo.
    Restringido a roles: admin, support.
    """
    # Tu lógica original de actualización va aquí abajo:
    return {"message": f"Dispositivo {device_id} actualizado con éxito"}

# REQUERIMIENTO: DELETE /devices/{device_id} -> Estrictamente Admin
@router.delete("/{device_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(require_admin)])
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """
    Elimina permanentemente un dispositivo del inventario.
    Restringido exclusivamente al rol: admin. Rol 'support' y 'user' recibirán 403 Forbidden.
    """
    # Tu lógica original de eliminación va aquí abajo:
    return {"message": f"Dispositivo {device_id} eliminado del sistema por el Administrador"}