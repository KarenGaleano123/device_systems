from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException, status
from datetime import datetime, timezone
from typing import Optional

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate, LoanDetailResponse
from app.schemas.user_schema import UserBasicResponse
from app.schemas.device_schema import DeviceBasicResponse


def _build_loan_detail(loan: Loan) -> LoanDetailResponse:
    return LoanDetailResponse(
        loan_id=loan.id,
        status=loan.status,
        loan_date=loan.loan_date,
        return_date=loan.return_date,
        user=UserBasicResponse(
            id=loan.user.id,
            name=loan.user.name,
            email=loan.user.email
        ),
        device=DeviceBasicResponse(
            id=loan.device.id,
            name=loan.device.name,
            serial_number=loan.device.serial_number,
            device_type=loan.device.device_type
        )
    )


def get_all_loans(
    db: Session,
    loan_status: Optional[str] = None,
    user_email: Optional[str] = None,
    device_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
        .options(joinedload(Loan.user), joinedload(Loan.device))
    )

    conditions = []
    if loan_status:
        conditions.append(Loan.status == loan_status)
    if user_email:
        conditions.append(User.email.ilike(f"%{user_email}%"))
    if device_type:
        conditions.append(Device.device_type.ilike(f"%{device_type}%"))
    if conditions:
        query = query.where(and_(*conditions))

    loans = query.offset(skip).limit(limit).all()
    return [_build_loan_detail(loan) for loan in loans]


def get_loan_by_id(db: Session, loan_id: int):
    loan = (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.id == loan_id)
        .first()
    )
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Préstamo con id {loan_id} no encontrado"
        )
    return loan


def get_loans_by_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {user_id} no encontrado"
        )
    loans = (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.user_id == user_id)
        .all()
    )
    return [_build_loan_detail(loan) for loan in loans]


def get_loans_by_device(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con id {device_id} no encontrado"
        )
    loans = (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.device_id == device_id)
        .all()
    )
    return [_build_loan_detail(loan) for loan in loans]


def create_loan(db: Session, loan_data: LoanCreate):
    user = db.query(User).filter(User.id == loan_data.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con id {loan_data.user_id} no encontrado"
        )

    device = db.query(Device).filter(Device.id == loan_data.device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con id {loan_data.device_id} no encontrado"
        )

    if not device.is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El dispositivo '{device.name}' no está disponible para préstamo"
        )

    new_loan = Loan(
        user_id=loan_data.user_id,
        device_id=loan_data.device_id,
        status="active"
    )
    db.add(new_loan)
    device.is_available = False
    db.commit()
    db.refresh(new_loan)
    return get_loan_by_id(db, new_loan.id)


def return_loan(db: Session, loan_id: int):
    loan = get_loan_by_id(db, loan_id)

    if loan.status == "returned":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este préstamo ya fue devuelto anteriormente"
        )

    loan.status = "returned"
    loan.return_date = datetime.now(timezone.utc)

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)
    return _build_loan_detail(loan)