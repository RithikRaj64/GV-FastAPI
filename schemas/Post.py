from pydantic import BaseModel
from typing import Literal


class Post(BaseModel):
    type: Literal["schedule", "titbit"]
    date: str
    location: dict[str, str]
    title: str
    description: str
    image: str
    link: str
