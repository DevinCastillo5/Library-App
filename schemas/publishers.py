from pydantic import BaseModel

class Publishers(BaseModel):
    publisher_name: str
    publisher_phone: str
    publisher_address: str
    publisher_email: str

