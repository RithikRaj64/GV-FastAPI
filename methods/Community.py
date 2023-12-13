from mongo import client
from typing import Literal

# Schemas
from schemas import Schedule
from schemas import Post


def addSchedule(info: Schedule) -> Literal[200]:
    db = client["Database"]
    collection = db["Schedule"]

    createSchedulePost(info)

    collection.insert_one({"date": info.date, "location": info.location})
    return 200


def createSchedulePost(info: Schedule) -> Literal[200]:
    db = client["Database"]
    collection = db["Posts"]

    collection.insert_one(
        {"type": "schedule", "date": info.date, "location": info.location}
    )

    return 200


def getAllPosts() -> list[Post]:
    db = client["Database"]
    collection = db["Posts"]

    posts = collection.find({})

    return list(posts)
