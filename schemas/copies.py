from pydantic import BaseModel

class Copies(BaseModel):
    copy_id: int
    ISBN: str
    Shelf_location: str
    Condition: str