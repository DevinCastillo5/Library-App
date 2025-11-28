from pydantic import BaseModel
from typing import Optional
from datetime import date

class Reservations(BaseModel):
    ReservationID: int
    DateFor: Optional[date] = None
    MemberID: Optional[int] = None
    BookReserved: Optional[str] = None