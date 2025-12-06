from pydantic import BaseModel
from datetime import date
from typing import Optional

class Authors(BaseModel):
    AuthorName: str
    DOB: Optional[date]  # <-- change from str to date
    Nationality: Optional[str]
