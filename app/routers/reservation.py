from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models.reservations import Reservation
from app.schemas.reservation import ReservationCreate
from app.database import get_db

router = APIRouter()


@router.get("/reservations/")
def read_reservations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservations = db.query(Reservation).offset(skip).limit(limit).all()
    return reservations




@router.post("/reservations/")
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    # Получаем время начала и окончания резервирования
    start_time = reservation.reservation_time
    end_time = start_time + timedelta(minutes=reservation.duration_minutes)

    # Проверка на наличие конфликта по времени
    conflicting_reservation = db.query(Reservation).filter(
        Reservation.table_id == reservation.table_id,
        Reservation.reservation_time < end_time,
        (Reservation.reservation_time + timedelta(minutes=reservation.duration_minutes)) > start_time  # Используйте reservation.duration_minutes
    ).first()

    if conflicting_reservation:
        raise HTTPException(status_code=400, detail="Time slot is already booked for this table.")

    # Создаем новое резервирование
    db_reservation = Reservation(
        customer_name=reservation.customer_name,
        table_id=reservation.table_id,
        reservation_time=start_time,
        duration_minutes=reservation.duration_minutes
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation




@router.delete("/reservations/{id}")
def delete_reservation(id: int, db: Session = Depends(get_db)):
    db_reservation = db.query(Reservation).filter(Reservation.id == id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(db_reservation)
    db.commit()
    return {"detail": "Reservation deleted"}
