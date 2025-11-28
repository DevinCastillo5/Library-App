from pydantic import BaseModel
from typing import Optional
from datetime import date

class Loans(BaseModel):
    LoanID: int
    ReturnDate: Optional[date] = None
    ISBN: Optional[str] = None
    MemberID: Optional[int] = None
    StaffID: Optional[int] = None
    CopyID: Optional[int] = None