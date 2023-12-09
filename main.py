from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Functions
from methods import signin, signup, passwordChecker

# Schemas for data
from schemas import Login

app = FastAPI()

origins = ["http://localhost:3000", "localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/auth/public/signup")
def SU(login: Login) -> dict[str, str]:
    if passwordChecker(login.password) is False:
        return {"status": "Password does not meet requirements"}

    res: dict[str, int] = signup(login)

    if res["status"] == 200:
        return {"status": "Signup Successful"}

    return {"status": "Username already exists"}


@app.post("/auth/public/signin")
def SI(login: Login) -> dict[str, str]:
    res: dict[str, int] = signin(login)

    if res["status"] == 200:
        return {"status": "Login Successful"}

    if res["status"] == 401:
        return {"status": "Incorrect Password"}

    return {"status": "User not found"}


# name, address, phone, email(op), pic(op), familysize
