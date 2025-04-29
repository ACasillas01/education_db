from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

def get_mongo_db():
    client = MongoClient(MONGO_URI)
    return client["online_edu"]  # your database name
