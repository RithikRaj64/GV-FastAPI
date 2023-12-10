from pydantic import BaseModel


class PublicLogin(BaseModel):
    username: str
    password: str


class CollectorLogin(BaseModel):
    employeeId: str
    password: str
