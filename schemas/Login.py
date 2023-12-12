from pydantic import BaseModel


class PublicLogin(BaseModel):
    username: str
    password: str


class WorkerLogin(BaseModel):
    employeeId: str
    password: str


class BusinessLogin(BaseModel):
    username: str
    password: str
