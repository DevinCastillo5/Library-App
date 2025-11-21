from pydantic import BaseModel


class Department(BaseModel):
    department_code: int
    department_name: str

