import re
from schemas import Login
from mongo import client


def signup(login: Login):
    db = client["Database"]
    collection = db["Public"]

    user = collection.find_one({"username": login.username})

    if user is not None:
        return {"status": 409}

    collection.insert_one({"username": login.username, "password": login.password})
    return {"status": 200}


def signin(login: Login):
    db = client["Database"]
    collection = db["Public"]
    user = collection.find_one({"username": login.username})

    if user is None:
        return {"status": 404}

    if user["password"] != login.password:
        return {"status": 401}

    return {"status": 200}


def passwordChecker(pw: str) -> bool:
    regex = re.compile("^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$")
    return bool(regex.match(pw))
