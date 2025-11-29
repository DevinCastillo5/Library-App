from pydantic import BaseModel
from typing import Optional

class Staff(BaseModel):
    StaffID: int
    StaffName: str
    Position: Optional[str] = None
    WorkTime: Optional[int] = None
