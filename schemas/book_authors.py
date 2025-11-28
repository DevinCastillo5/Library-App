from pydantic import BaseModel, Field


class BookAuthorBase(BaseModel):
    ISBN: str = Field(..., min_length=13, max_length=13)
    AuthorName: str


class BookAuthorCreate(BookAuthorBase):
    pass


class BookAuthorRead(BookAuthorBase):
    pass
