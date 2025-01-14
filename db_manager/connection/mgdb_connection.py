from pymongo import MongoClient

uri = "mongodb://127.0.0.1:27017"
client = MongoClient(uri)

db = client["test-database"]

collection = db["teste-collection"]


print(collection)
