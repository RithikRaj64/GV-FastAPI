from pydantic import BaseModel
from typing import Optional

class Schedule(BaseModel):
    bookingId: Optional[str] = None
    name: str
    date: str
    latitude: str
    longitude: str
    comments: Optional[str] = None
    status: Optional[str] = None
    address: Optional[str] = None
    employeeId: Optional[str] = None