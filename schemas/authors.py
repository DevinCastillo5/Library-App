from pydantic import BaseModel

class Authors(BaseModel):
    author_name: str
    date_of_birth: str
    nationality: str