from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Functions
from methods import publicSignup, publicSignin, completePublicProfile, passwordChecker

# Schemas for data
from schemas import PublicLogin
from schemas import Public

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
def SU(login: PublicLogin) -> dict[str, str]:
    if passwordChecker(login.password) is False:
        return {"status": "Password does not meet requirements"}

    res: dict[str, int] = publicSignup(login)

    if res["status"] == 200:
        return {"status": "Signup Successful"}

    return {"status": "Username already exists"}


@app.post("/auth/public/completeProfile")
def CP(info: Public) -> dict[str, str]:
    res: dict[str, int] = completePublicProfile(info)

    if res["status"] == 200:
        return {"status": "Profile Completed"}

    return {"status": "User not found"}


@app.post("/auth/public/signin")
def SI(login: PublicLogin) -> dict[str, str]:
    res: dict[str, int] = publicSignin(login)

    if res["status"] == 200:
        return {"status": "Login Successful"}

    if res["status"] == 401:
        return {"status": "Incorrect Password"}

    return {"status": "User not found"}


@app.post("auth/collector/signup")
def CS():
    pass


# name, address, phone, email(op), pic(op), familysize
