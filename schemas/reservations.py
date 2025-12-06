from pydantic import BaseModel
from typing import Optional
from datetime import date


class ReservationRequest(BaseModel):
    ISBN: str
    MemberID: int

class ReservationCreate(BaseModel):
    ISBN: str
    MemberID: int
    CopyID: int
    ReserveDate: date

class Reservations(BaseModel):
    ReservationID: int
    ISBN: str
    MemberID: int
    CopyID: int
    ReserveDate: Optional[date] = None
