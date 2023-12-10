from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Functions
from methods import passwordChecker
from methods import publicSignup, publicSignin, completePublicProfile
from methods import workerSignup, workerSignin, completeWorkerProfile

# Schemas for data
from schemas import PublicLogin, WorkerLogin
from schemas import Public, Worker

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
def signup1(info: PublicLogin) -> dict[str, str]:
    if passwordChecker(info.password) is False:
        return {"status": "Password does not meet requirements"}

    res: dict[str, int] = publicSignup(info)

    if res == 200:
        return {"status": "Signup Successful"}

    return {"status": "Username already exists"}


@app.post("/auth/public/completeProfile")
def complete1(info: Public) -> dict[str, str]:
    res: dict[str, int] = completePublicProfile(info)

    if res == 200:
        return {"status": "Profile Completed"}

    return {"status": "User not found"}


@app.post("/auth/public/signin")
def signin1(info: PublicLogin) -> dict[str, str]:
    res: dict[str, int] = publicSignin(info)

    if res == 200:
        return {"status": "Login Successful"}

    if res == 401:
        return {"status": "Incorrect Password"}

    return {"status": "User not found"}


@app.post("/auth/worker/signup")
def signup2(info: WorkerLogin) -> dict[str, str]:
    if passwordChecker(info.password) is False:
        return {"status": "Password does not meet requirements"}

    res: dict[str, int] = workerSignup(info)

    if res == 200:
        return {"status": "Signup Successful"}

    return {"status": "Username already exists"}


@app.post("/auth/worker/completeProfile")
def complete2(info: Worker) -> dict[str, str]:
    res: dict[str, int] = completeWorkerProfile(info)

    if res == 200:
        return {"status": "Profile Completed"}

    return {"status": "User not found"}


@app.post("/auth/worker/signin")
def signin2(info: WorkerLogin) -> dict[str, str]:
    res: dict[str, int] = workerSignin(info)

    if res == 200:
        return {"status": "Login Successful"}

    if res == 401:
        return {"status": "Incorrect Password"}

    return {"status": "User not found"}


# name, address, phone, email(op), pic(op), familysize
