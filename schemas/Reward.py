from pydantic import BaseModel
from typing import Optional

class Reward(BaseModel):
    rewardId: Optional[str] = None
    businessName: str
    name: str
    description: str
    points: int
    image: bytes
    redeemedBy: Optional[dict[str, int]] = None