from pydantic import BaseModel
from typing import List


class logs(BaseModel):
    employeeId: str
    datetime: str
    location: str
    amount: float

