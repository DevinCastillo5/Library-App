from pydantic import BaseModel, Field


class BookAuthor(BaseModel):
    ISBN: str = Field(..., min_length=13, max_length=13)
    AuthorName: str