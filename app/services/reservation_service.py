from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.reservations import Reservation
from app.schemas.reservation import ReservationCreate
from datetime import timedelta

async def create_reservation(db: AsyncSession, reservation: ReservationCreate):
    # Проверка на пересечение временных слотов
    existing_reservation = await db.execute(
        select(Reservation).filter(
            Reservation.table_id == reservation.table_id,
            Reservation.reservation_time < reservation.reservation_time + timedelta(minutes=reservation.duration_minutes),
            Reservation.reservation_time + timedelta(minutes=reservation.duration_minutes) > reservation.reservation_time
        )
    )
    if existing_reservation.scalars().first() is not None:
        raise ValueError("Table is already booked for the selected time.")

    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)
    await db.commit()
    await db.refresh(db_reservation)
    return db_reservation

async def get_reservations(db: AsyncSession):
    result = await db.execute(select(Reservation))
    return result.scalars().all()

async def delete_reservation(db: AsyncSession, reservation_id: int):
    result = await db.execute(select(Reservation).filter(Reservation.id == reservation_id))
    reservation = result.scalars().first()
    if reservation:
        await db.delete(reservation)
        await db.commit()
    return reservation
