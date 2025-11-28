from pydantic import BaseModel

class Books(BaseModel):
    ISBN: str
    book_title: str
    book_category: str
    publish_year: int
    publisher_name: str