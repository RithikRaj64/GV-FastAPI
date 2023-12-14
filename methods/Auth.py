# General Imports
import re
from typing import List, Literal
from io import BytesIO

# Image handling
from fastapi import UploadFile, File, Form
from PIL import Image

# Database
from mongo import client

# Schemas
from schemas import PublicLogin, WorkerLogin, BusinessLogin
from schemas import Public, Worker, Business
from schemas import BookPickupDetails
from schemas import logs

async def publicSignup(info: PublicLogin) -> Literal[409, 200]:
    db = client["Database"]
    collection = db["Public"]

    user = collection.find_one({"username": info.username})

    if user is not None:
        return 409

    collection.insert_one({"username": info.username, "password": info.password})
    return 200


def publicSignin(info: PublicLogin) -> Literal[404, 401, 200]:
    db = client["Database"]
    collection = db["Public"]
    user = collection.find_one({"username": info.username})

    if user is None:
        return 404

    if user["password"] != info.password:
        return 401

    return 200


def workerSignup(info: WorkerLogin) -> Literal[409, 200]:
    db = client["Database"]
    collection = db["Worker"]

    user = collection.find_one({"employeeId": info.employeeId})

    if user is not None:
        return 409

    collection.insert_one({"employeeId": info.employeeId, "password": info.password})
    return 200


def workerSignin(info: WorkerLogin) -> Literal[404, 401, 200]:
    db = client["Database"]
    collection = db["Worker"]
    user = collection.find_one({"employeeId": info.employeeId})

    if user is None:
        return 404

    if user["password"] != info.password:
        return 401

    return 200


def businessSignup(info: BusinessLogin) -> Literal[409, 200]:
    db = client["Database"]
    collection = db["Business"]

    user = collection.find_one({"username": info.username})

    if user is not None:
        return 409

    collection.insert_one({"username": info.username, "password": info.password})
    return 200


def businessSignin(info: BusinessLogin) -> Literal[404, 401, 200]:
    db = client["Database"]
    collection = db["Business"]
    user = collection.find_one({"username": info.username})

    if user is None:
        return 404

    if user["password"] != info.password:
        return 401

    return 200


def passwordChecker(pw: str) -> bool:
    regex = re.compile("^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$")
    return bool(regex.match(pw))


def completePublicProfile(info: Public) -> Literal[404, 200]:
    db = client["Database"]
    collection = db["Public"]

    user = collection.find_one({"username": info.username})

    if user is None:
        return 404

    collection.update_one(
        {"username": info.username},
        {
            "$set": {
                "mobile": info.mobile,
                "email": info.email,
                "full_name": info.full_name,
            }
        },
    )

    return 200


def completeWorkerProfile(info: Worker) -> Literal[404, 200]:
    db = client["Database"]
    collection = db["Worker"]

    user = collection.find_one({"employeeId": info.employeeId})

    if user is None:
        return 404

    collection.update_one(
        {"employeeId": info.employeeId},
        {
            "$set": {
                "mobile": info.mobile,
                "email": info.email,
                "full_name": info.full_name,
                "type": info.type,
            }
        },
    )

    return 200


def completeBusinessProfile(info: Business) -> Literal[404, 200]:
    db = client["Database"]
    collection = db["Business"]

    user = collection.find_one({"username": info.username})

    if user is None:
        return 404

    collection.update_one(
        {"username": info.username},
        {
            "$set": {
                "businessName": info.businessName,
                "businessType": info.businessType,
                "address": info.address,
                "email": info.email,
                "mobile": info.mobile,
                "businessDescription": info.businessDescription,
            }
        },
    )

    return 200


async def uploadImages(file: UploadFile = File(...), username: str = Form(...)):
    db = client["Database"]
    collection = db["Business"]

    business = collection.find_one({"username": username})

    if business is None:
        return 404
    
    collection.update_one(
        {"username": username},
        {
            "$set": {
                "image": file.file.read()
            }
        }
    )
    
    return 200


async def getImages():
    db = client["Database"]
    collection = db["Business"]

    business = collection.find_one({"username": "hello"})

    if business is None:
        return 404
    
    image = Image.open(BytesIO(business["image"])).show()
    # return business["image"]

async def bookPickup(info : BookPickupDetails):
    db = client["Database"]
    collection = db["Public"]
    collection2 = db["BookPickupDetails"]
    user = collection.find_one({"username": info.username})
    if user is None:
        return 404
    collection2.insert_one({"username": info.username, "datetime": info.datetime, "address": info.address})
    return 200

def viewDailyLogs() -> list[logs]:
    db = client["Database"]
    collection = db["DailyLogs"]
    
    user = list(collection.find({}))
    return user


async def addDailyLogs(info : logs):
    db = client["Database"]
    collection = db["DailyLogs"]
    user = collection.find_one({"name":info.name})
    if user is not None:
        return 409

    collection.insert_one({"name": info.name, "datetime": info.datetime, "amount": info.amount})
    return 200
