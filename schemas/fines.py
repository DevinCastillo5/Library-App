from pydantic import BaseModel

class Fines(BaseModel):
    fine_id: int
    loan_id: int
    amount: float
    daysOverdue: int