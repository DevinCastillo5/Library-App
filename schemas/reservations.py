from pydantic import BaseModel
from typing import Optional
from datetime import date

class Reservations(BaseModel):
    ReservationID: int
    memberID: int
    DateFor: date
    BookReserved: int