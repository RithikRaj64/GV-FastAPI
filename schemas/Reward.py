from pydantic import BaseModel

class Reward(BaseModel):
    rewardId: str
    businessName: str
    name: str
    description: str
    points: int
    image: str
    redeemedBy: dict[str, int]