from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware

# Functions
from methods import passwordChecker
from methods import publicSignup, publicSignin, completePublicProfile
from methods import workerSignup, workerSignin, completeWorkerProfile
from methods import (
    businessSignup,
    businessSignin,
    completeBusinessProfile,
    uploadImages,
    getImages,
)
from methods import bookPickup, getBookingsSuper
from methods import addReward, getRewards, getReward, deleteReward, claimRewards
from methods import viewDailyLogs, addDailyLogs, getEmployeeLogs
from methods import addSchedule, getAllPosts, createPost, getTodaySchedule


# Schemas for data
from schemas import PublicLogin, WorkerLogin, BusinessLogin
from schemas import Public, Worker, Business
from schemas import BookPickupDetails
from schemas import Schedule
from schemas import Reward
from schemas import logs
from schemas import Post

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Password and confirm password validate
@app.post("/auth/public/signup")
async def signup1(info: PublicLogin) -> dict[str, str]:
    if passwordChecker(info.password) is False:
        return {"status": "Password does not meet requirements"}

    res: dict[str, int] = await publicSignup(info)

    print(res)

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

    if res == 404:
        return {"status": "User not found"}

    if res == 401:
        return {"status": "Incorrect Password"}

    return res


@app.post("/auth/business/signup")
def signup3(info: BusinessLogin) -> dict[str, str]:
    if passwordChecker(info.password) is False:
        return {"status": "Password does not meet requirements"}

    res: dict[str, int] = businessSignup(info)

    if res == 200:
        return {"status": "Signup Successful"}

    return {"status": "Username already exists"}


@app.post("/auth/business/completeProfile")
def complete3(info: Business) -> dict[str, str]:
    res: dict[str, int] = completeBusinessProfile(info)

    if res == 200:
        return {"status": "Profile Completed"}

    return {"status": "User not found"}


@app.post("/auth/business/signin")
def signin3(info: BusinessLogin) -> dict[str, str]:
    res: dict[str, int] = businessSignin(info)

    if res == 200:
        return {"status": "Login Successful"}

    if res == 401:
        return {"status": "Incorrect Password"}

    return {"status": "User not found"}


# allow multiple files
@app.post("/auth/business/upload")
async def upload_file(file:UploadFile = File(...),  username: str = Form(...)):
    await uploadImages(file, username)
    return {"status": "Upload Successful"}


@app.get("/auth/business/getImages")
async def get_file():
    return await getImages()


@app.post("/rewards/add")
async def add_rewards(file: UploadFile = File(...), info: dict[str, str | int] = Form(...)):
    addReward(file, info)
    return {"status": "Reward added successfully"}


@app.get("/rewards/view/all")
async def view_all_rewards() -> list[Reward]:
    return getRewards()


@app.get("/rewards/view/{rewardId}")
async def view_rewards(rewardId: str):
    return {"reward": getReward(rewardId)}


@app.put("/rewards/update/{rewardId}")
async def update_rewards(rewardId):
    pass


@app.delete("/rewards/delete/{rewardId}")
async def delete_rewards(rewardId: str):
    res = deleteReward(rewardId)

    if res == 200:
        return {"status": "Reward deleted successfully"}

    return {"status": "Reward not deleted"}


@app.post("/rewards/claim/{username}/{rewardId}")
async def claim_rewards(username: str, rewardId: str):
    res = claimRewards(username, rewardId)

    if res == 200:
        return {"status": "Reward claimed successfully"}

    return {"status": "Reward not claimed"}


@app.post("/dailyLogs/add")
async def add_Logs(info: logs):
    res = await addDailyLogs(info)
    if res == 200:
        return {"status": "Added to Daily Logs"}



@app.get("/dailyLogs/viewAll")
def view_Logs():
    res = viewDailyLogs()
    return {"logs": res}

@app.get("/dailyLogs/view/{employeeId}")
def get_employee_logs(employeeId : str):
    res = getEmployeeLogs(employeeId)
    return {"logs" : res}

@app.post("/community/addSchedule")
def addPost(info: Schedule):
    res = addSchedule(info)

    if res == 200:
        return {"status": "Schedule added successfully"}

    return {"status": "Failed to add schedule"}


@app.get("/community/addPost")
def addPost(info: Post):
    res = createPost(info)

    if res == 200:
        return {"status": "Post added successfully"}

    return {"status": "Failed to add post"}


@app.get("/community/getAllPosts")
def getAllPosts() -> list[Post]:
    return getAllPosts()


@app.get("/worker/getSchedule/{date}")
def getSchedule(date: str) -> Schedule:
    return getTodaySchedule(date)


@app.post("/public/bookPickup")
async def book_A_Pickup(info: Schedule):
    res = await bookPickup(info)
    if res == 200:
        return {"status": "Booked a pickup successfully"}
    if res == 404:
        return {"status": "Booking Failed"}
    
@app.get("/supervisor/getBookings")
async def get_bookings_super():
    return {"bookings": getBookingsSuper()}

@app.get("/collector/getBookings/{employeeId}")
async def get_bookings_collector(employeeId: str):
    return {"bookings": getBookingsCollector(employeeId)}