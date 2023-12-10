# General Imports
import re

# Database
from mongo import client

# Schemas
from schemas import PublicLogin, CollectorLogin
from schemas import Public, Collector


def publicSignup(info: PublicLogin):
    db = client["Database"]
    collection = db["Public"]

    user = collection.find_one({"username": info.username})

    if user is not None:
        return {"status": 409}

    collection.insert_one({"username": info.username, "password": info.password})
    return {"status": 200}


def publicSignin(info: PublicLogin):
    db = client["Database"]
    collection = db["Public"]
    user = collection.find_one({"username": info.username})

    if user is None:
        return {"status": 404}

    if user["password"] != info.password:
        return {"status": 401}

    return {"status": 200}


def collectorSignup(info: CollectorLogin):
    db = client["Database"]
    collection = db["Collector"]

    user = collection.find_one({"employeeId": info.employeeId})

    if user is not None:
        return {"status": 409}

    collection.insert_one({"employeeId": info.employeeId, "password": info.password})
    return {"status": 200}


def collectorSignin(info: CollectorLogin):
    db = client["Database"]
    collection = db["Collector"]
    user = collection.find_one({"employeeId": info.employeeId})

    if user is None:
        return {"status": 404}

    if user["password"] != info.password:
        return {"status": 401}

    return {"status": 200}


def passwordChecker(pw: str) -> bool:
    regex = re.compile("^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$")
    return bool(regex.match(pw))


def completePublicProfile(info: Public):
    db = client["Database"]
    collection = db["Public"]

    user = collection.find_one({"username": info.username})

    if user is None:
        return {"status": 404}

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

    return {"status": 200}


def completeCollectorProfile(info: Collector):
    db = client["Database"]
    collection = db["Collector"]

    user = collection.find_one({"employeeId": info.employeeId})

    if user is None:
        return {"status": 404}

    collection.update_one(
        {"employeeId": info.employeeId},
        {
            "$set": {
                "mobile": info.mobile,
                "email": info.email,
                "full_name": info.full_name,
            }
        },
    )

    return {"status": 200}
