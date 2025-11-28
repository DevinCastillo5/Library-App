from pydantic import BaseModel, Field
from typing import Optional



class Books(BaseModel):
    ISBN: str = Field(..., min_length=13, max_length=13)
    Title: str
    Categories: Optional[str] = None
    PublishYear: Optional[int] = None   # YEAR is int in Python
    PublishName: Optional[str] = None

# the optional is because it can be null

class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    pass
