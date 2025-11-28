from pydantic import BaseModel

class Members(BaseModel):
    memberID: int
    memName: str
    Email: str
    Phone: str
    Address: str