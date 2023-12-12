from pydantic import BaseModel
# from datetime import date,time

class BookPickupDetails(BaseModel):
    username: str
    datetime: str
    address: str