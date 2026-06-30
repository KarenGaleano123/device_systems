from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from typing import Optional
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate


def get_all_devices(
    db: Session,
    device_type: Optional[str] = None,
    is_available: Optional[bool] = None,
    brand: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(Device)

    if device_type:
        query = query.filter(Device.device_type.ilike(f"%{device_type}%"))
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
                Device.brand.ilike(f"%{search}%")
            )
        )

    return query.offset(skip).limit(limit).all()


def get_device_by_id(db: Session, device_id: int):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo con id {device_id} no encontrado"
        )
    return device


def create_device(db: Session, device_data: DeviceCreate):
    existing = db.query(Device).filter(
        Device.serial_number == device_data.serial_number
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un dispositivo con el número de serie {device_data.serial_number}"
        )
    new_device = Device(**device_data.model_dump())
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


def update_device(db: Session, device_id: int, device_data: DeviceUpdate):
    device = get_device_by_id(db, device_id)
    update_fields = device_data.model_dump(exclude_unset=True)
    if "serial_number" in update_fields:
        existing = db.query(Device).filter(
            Device.serial_number == update_fields["serial_number"]
        ).first()
        if existing and existing.id != device_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El número de serie ya está en uso"
            )
    for key, value in update_fields.items():
        setattr(device, key, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int):
    device = get_device_by_id(db, device_id)
    db.delete(device)
    db.commit()