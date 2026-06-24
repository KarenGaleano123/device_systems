from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.dependencies.database_dependency import get_db
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse
from app.services import loan_service

router = APIRouter(tags=["Loans"])


@router.get("/loans", response_model=List[LoanDetailResponse], summary="Listar préstamos con filtros y JOIN")
def list_loans(
    status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Consulta préstamos con JOIN entre loans, users y devices.
    - **status**: active, returned, overdue
    - **user_email**: filtrar por correo del usuario
    - **device_type**: filtrar por tipo de dispositivo
    """
    return loan_service.get_all_loans(db, status, user_email, device_type, skip, limit)


@router.get("/loans/details", response_model=List[LoanDetailResponse], summary="Ver préstamos con información completa")
def list_loan_details(db: Session = Depends(get_db)):
    return loan_service.get_all_loans(db)


@router.get("/loans/{loan_id}", response_model=LoanDetailResponse, summary="Obtener préstamo por ID")
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = loan_service.get_loan_by_id(db, loan_id)
    return loan_service._build_loan_detail(loan)


@router.post("/loans", response_model=LoanDetailResponse, status_code=status.HTTP_201_CREATED, summary="Crear préstamo")
def create_loan(loan_data: LoanCreate, db: Session = Depends(get_db)):
    """
    - Valida que el usuario exista
    - Valida que el dispositivo exista
    - Valida que el dispositivo esté disponible
    - Marca el dispositivo como no disponible al prestarlo
    """
    return loan_service.create_loan(db, loan_data)


@router.patch("/loans/{loan_id}/return", response_model=LoanDetailResponse, summary="Devolver dispositivo")
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    """
    - Cambia el estado a 'returned'
    - Registra la fecha de devolución
    - Vuelve a marcar el dispositivo como disponible
    """
    return loan_service.return_loan(db, loan_id)


@router.get("/users/{user_id}/loans", response_model=List[LoanDetailResponse], tags=["Users"], summary="Préstamos de un usuario")
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loans_by_user(db, user_id)


@router.get("/devices/{device_id}/loans", response_model=List[LoanDetailResponse], tags=["Devices"], summary="Historial de préstamos de un dispositivo")
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loans_by_device(db, device_id)