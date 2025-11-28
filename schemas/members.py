from pydantic import BaseModel

class Members(BaseModel):
    member_id: int
    member_name: str
    member_email: str
    member_phone: str
    member_address: str