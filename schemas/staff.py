from pydantic import BaseModel

class Staff(BaseModel):
    staff_id: int
    staff_name: str
    staff_role: str
    staff_email: str
    staff_phone: str
    staff_schedule: str
    staff_salary: float