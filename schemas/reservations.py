from pydantic import BaseModel

class Reservations(BaseModel):
    reservation_id: int
    member_id: int
    copy_id: int
    reservation_date: str