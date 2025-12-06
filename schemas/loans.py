from pydantic import BaseModel
from typing import Optional
from datetime import date


class LoanRequest(BaseModel):
    ISBN: str
    MemberID: int


class LoanCreate(BaseModel):
    ISBN: str
    MemberID: int
    StaffID: int
    CopyID: int
    ReturnDate: Optional[date] = None

class Loans(BaseModel):
    LoanID: int
    ISBN: str
    MemberID: int
    StaffID: int
    CopyID: int
    ReturnDate: Optional[date] = None
