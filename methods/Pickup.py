from mongo import client
import hashlib

from schemas import Schedule

async def bookPickup(info : Schedule):
    db = client["Database"]
    collection = db["Pickup"]

    id = hashlib.sha256(str(info).encode()).hexdigest()

    collection.insert_one({"bookingId" : id,"name": info.name, "date": info.date, "latitude": info.latitude, "longitude": info.longitude, "comments": info.comments, "status": "Booked", "address": info.address, "employeeId": info.employeeId})
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

async def assignBooking(bookingId : str, employeeId : str):
    db = client["Database"]
    collection = db["Pickup"]
    collection.update_one({"bookingId" : bookingId}, {"$set" : {"status" : "Assigned", "employeeId" : employeeId}})
    return 200

async def getBookingsCollector(employeeId : str):
    db = client["Database"]
    collection = db["Pickup"]

    res = list(collection.find({"employeeId" : employeeId, "status" : "Assigned"}))

    ret = []

    for i in res:
        ret.append(Schedule(**i))

    return ret
