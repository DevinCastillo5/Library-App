from pydantic import BaseModel
from typing import Optional

class Copies(BaseModel):
    CopyID: int
    ISBN: str
    ShelfLocation: Optional[str] = None
    ConditionDesc: Optional[str] = None