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
    return collection.find({"status" : "Booked"})

# async def assignBooking()

async def getBookingsCollector(employeeId : str):
    db = client["Database"]
    collection = db["Pickup"]
    return collection.find({"status" : "Assigned", "employeeId" : employeeId})