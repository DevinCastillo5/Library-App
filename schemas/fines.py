from pydantic import BaseModel
from typing import Optional

class Fines(BaseModel):
    FineID: int
    AmountFined: Optional[int] = None
    DaysOverdue: Optional[int] = None
    LoanID: Optional[int] = None