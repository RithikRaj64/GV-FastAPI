from typing import Optional
from pydantic import BaseModel


class Public(BaseModel):
    username: str
    password: str
    mobile: str
    email: Optional[str] = None
    full_name: str


class Collector(BaseModel):
    employeeId: str
    password: str
    mobile: str
    email: Optional[str] = None
    full_name: str
    address: str
