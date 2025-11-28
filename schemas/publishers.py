from pydantic import BaseModel
from typing import Optional

class Publishers(BaseModel):
    PublishName: str
    ContactInfo: Optional[str] = None