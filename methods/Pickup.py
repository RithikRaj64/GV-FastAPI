from mongo import client

from schemas import Schedule

async def bookPickup(info : Schedule):
    db = client["Database"]
    collection = db["Pickup"]

    collection.insert_one({"name": info.name, "date": info.date, "latitude": info.latitude, "longitude": info.longitude, "comments": info.comments, "status": "Booked", "address": info.address, "employeeId": info.employeeId})
    return 200

async def getBookingsSuper():
    db = client["Database"]
    collection = db["Pickup"]

    res = list(collection.find({"status" : "Booked"}))

    ret = []

    for i in res:
        ret.append(Schedule(**i))
    print(res)
    return ret

async def assignBooking(info):
    db = client["Database"]
    collection = db["Pickup"]
    collection.find_one_and_update({"_id": info.id}, {"$set": {"status": "Assigned", "employeeId": info.employeeId}})

async def getBookingsCollector(employeeId : str):
    db = client["Database"]
    collection = db["Pickup"]
    return collection.find({"status" : "Assigned", "employeeId" : employeeId})