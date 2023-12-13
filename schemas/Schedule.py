from pydantic import BaseModel


class Schedule(BaseModel):
    date: str
    location: dict[str, str]
