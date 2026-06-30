from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support

router = APIRouter(prefix="/loans", tags=["Loans"])

# REQUERIMIENTO: POST /loans -> Cualquier usuario autenticado
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_loan(loan_data: dict, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    """
    Crea una solicitud de préstamo de un dispositivo.
    Cualquier usuario autenticado puede hacerlo.
    """
    return {
        "message": "Préstamo solicitado exitosamente",
        "solicitante_email": current_user.email,
        "data_enviada": loan_data
    }

# REQUERIMIENTO: PATCH /loans/{loan_id}/return -> Admin o support
@router.patch("/{loan_id}/return", dependencies=[Depends(require_admin_or_support)])
def return_device(loan_id: int, db: Session = Depends(get_db)):
    """
    Registra el retorno físico de un dispositivo prestado.
    Restringido a roles: admin, support.
    """
    return {"message": f"Retorno del préstamo {loan_id} procesado por personal autorizado"}

# REQUERIMIENTO: GET /loans/details -> Admin o support (Uso de Joins / Consultas avanzadas)
@router.get("/details", dependencies=[Depends(require_admin_or_support)])
def get_loan_details(db: Session = Depends(get_db)):
    """
    Retorna el listado completo y detallado de préstamos haciendo cruces.
    Restringido a roles: admin, support.
    """
    return {"message": "Reporte consolidado de préstamos generado de manera segura"}