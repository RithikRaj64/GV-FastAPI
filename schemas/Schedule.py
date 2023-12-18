from pydantic import BaseModel
from typing import Optional

class Schedule(BaseModel):
    name: str
    date: str
    latitude: str
    longitude: str
    comments: Optional[str] = None
    status: str
    address: Optional[str] = None
    employeeId: Optional[str] = None