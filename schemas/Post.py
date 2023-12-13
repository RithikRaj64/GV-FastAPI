from pydantic import BaseModel
from typing import Literal, Optional


class Post(BaseModel):
    type: Literal["schedule", "titbit"]
    date: str
    location: dict[str, str]
    title: str
    description: str
    image: Optional[str]
    link: Optional[str]
