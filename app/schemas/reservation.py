from pydantic import BaseModel
from datetime import datetime

class ReservationCreate(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int

class Reservation(ReservationCreate):
    id: int

    class Config:
        orm_mode = True
