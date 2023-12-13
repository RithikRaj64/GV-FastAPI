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


def getTodaySchedule(date: str) -> Schedule:
    db = client["Database"]
    collection = db["Schedule"]

    schedule = collection.find_one({"date": date})

    return schedule


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


def createPost(info: Post) -> Literal[200]:
    db = client["Database"]
    collection = db["Posts"]

    collection.insert_one(
        {
            "type": "titbit",
            "title": info.title,
            "description": info.description,
            "image": info.image,
            "link": info.link,
        }
    )

    return 200
