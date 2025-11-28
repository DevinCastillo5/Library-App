from pydantic import BaseModel
from typing import Optional

class Staff(BaseModel):
    StaffID: int
    StaffName: Optional[str] = None
    Position: Optional[str] = None
    WorkTime: Optional[int] = None
