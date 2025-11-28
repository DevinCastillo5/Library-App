from pydantic import BaseModel

class Book_Authors(BaseModel):
    book_id: int
    author_name: str