from pydantic import BaseModel

class Loans(BaseModel):
    loan_id: int
    member_id: int
    staff_id: int
    copy_id: int
    loan_date: str
    return_date: str