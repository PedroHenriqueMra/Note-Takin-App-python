from pymongo import MongoClient
from bson.objectid import ObjectId
from contextlib import contextmanager
from utils.singleton import Singleton
from pymongo.database import Database


class MongoDBConnection:
    def __init__(self):
        self.connection_string = "mongodb://127.0.0.1:27017"
        self.collection_name = "note_takin_database"
        self.client_connection = None

    @contextmanager
    def context_database(self):
        try:
            print("-> connecting NoSQL database...")
            connection = self.get_connection()
            yield connection
        finally:
            print("-> closing NoSQL database...")
            self.close_connection()

    def get_connection(self) -> Database:
        client = MongoClient(self.connection_string)
        self.client_connection = client

        database = client[self.collection_name]
        return database
    
    def close_connection(self) -> None:
        self.client_connection.close()
        self.client_connection = None

mongo_database = MongoDBConnection()
# pool conection
mongo_connection = mongo_database.get_connection()
