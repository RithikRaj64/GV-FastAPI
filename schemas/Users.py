from typing import Optional
from pydantic import BaseModel


class Public(BaseModel):
    username: str
    password: str
    mobile: str
    email: Optional[str] = None
    full_name: str
    # address also


class Worker(BaseModel):
    employeeId: str
    password: str
    type: str
    mobile: str
    email: Optional[str] = None
    full_name: str


class Business(BaseModel):
    username: str
    password: str
    businessName: str
    businessType: str
    address: str
    email: Optional[str] = None
    mobile: str
    businessDescription: str
    image: Optional[bytes] = None

# Rewards : Reward title, description, image, points, expiry date
