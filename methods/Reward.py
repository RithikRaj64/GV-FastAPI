from typing import Literal
from PIL import Image

from fastapi import UploadFile, File, Form
from sklearn.feature_extraction import img_to_graph
from mongo import client
import hashlib
from io import BytesIO
import base64

from schemas import Reward

def addReward(file: UploadFile = File(...), info: dict[str, str | int] = Form(...)) -> Literal[200]:
    db = client["Database"]
    collection = db["Rewards"]

    id = hashlib.sha256(str(info).encode()).hexdigest()

    buffer = BytesIO()

    img = Image.open(file.file)
    img.save(buffer, format="JPEG")
    img_str = base64.b64encode(buffer.getvalue())

    collection.insert_one({"rewardId": id, "businessName": info.businessName, "name": info.name, "description": info.description, "points": info.points, "image": img_str, "redeemedBy": {}})
    return 200

def getRewards() -> list[Reward]:
    db = client["Database"]
    collection = db["Rewards"]

    rewards = list(collection.find({}))
    Reward_list: list[Reward] = []

    for reward in rewards:
        Reward_list.append(Reward(**reward))

    return Reward_list

def getReward(rewardId:str) -> Reward:
    db = client["Database"]
    collection = db["Rewards"]

    reward = collection.find_one({"rewardId": rewardId})

    # convert to Reward object
    reward = Reward(**reward)
    return reward

def deleteReward(rewardId:str) -> Literal[200]:
    db = client["Database"]
    collection = db["Rewards"]

    collection.delete_one({"rewardId": rewardId})

    return 200

def claimRewards(username:str, rewardId:str) -> Literal[200]:
    db = client["Database"]
    collection = db["Rewards"]

    log = collection.find_one({"rewardId": rewardId})

    print(log)

    # inc count
    if username in log["redeemedBy"]:
        log["redeemedBy"][username] += 1
    else:
        log["redeemedBy"][username] = 1
     
    collection.update_one({"rewardId": rewardId}, {"$set": {"redeemedBy": log["redeemedBy"]}})  

    return 200