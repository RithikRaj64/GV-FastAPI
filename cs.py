from pymongo import MongoClient
import pandas as pd

# # Get the MongoDB Atlas connection URI
uri = "mongodb+srv://root:root@greenvoucher.wdhjtff.mongodb.net/?retryWrites=true&w=majority"

# # Create a new client and connect to the server
client = MongoClient(uri)

db = client["Database"]
collection = db["TS"]

cursor = collection.find({})
data_list = list(cursor)

# convert and save as csv

df = pd.DataFrame(data_list)
df.to_csv("data.csv", index=False)

df = pd.read_csv("data.csv")