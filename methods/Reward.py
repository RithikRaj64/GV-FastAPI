from typing import Literal
from mongo import client
import hashlib

from schemas import Reward

def addReward(info: Reward) -> Literal[200]:
    db = client["Database"]
    collection = db["Rewards"]

    id = hashlib.sha256(str(info.model_dump()).encode()).hexdigest()

    collection.insert_one({"rewardId": id, "businessName": info.businessName, "name": info.name, "description": info.description, "points": info.points, "image": info.image, "redeemedBy": {}})
    return 200

def getRewards() -> list[Reward]:
    db = client["Database"]
    collection = db["Rewards"]

    rewards = list(collection.find({}))

    return rewards

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