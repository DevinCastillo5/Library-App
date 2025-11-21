from pydantic import BaseModel


class Course(BaseModel):
    course_code: int
    course_title: str
    department_code: int  # Foreign Key to department table
