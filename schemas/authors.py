from pydantic import BaseModel

class Authors(BaseModel):
    AuthorName: str
    DOB: str
    Nationality: str