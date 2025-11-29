from pydantic import BaseModel
from typing import Required

class Fines(BaseModel):
    FineID: int
    AmountFined: int
    DaysOverdue: int
    LoanID: int