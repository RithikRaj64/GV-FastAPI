from pymongo.mongo_client import MongoClient
from decouple import config

# Get the MongoDB Atlas connection URI
uri = config("MONGO_URI")

# Create a new client and connect to the server
client = MongoClient(uri)

