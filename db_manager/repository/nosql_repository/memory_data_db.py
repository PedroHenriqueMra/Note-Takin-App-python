from db_manager.connections.mgdb_connection import mongo_conn
from ...connections.mgdb_connection import MongoDBConnection

from pymongo.database import Database
from pymongo.collection import Collection


class MemoryDataDB():

    def __init__(self):
        self.collection_name:str = "memory_data_test"
        self.collection:Collection = mongo_conn[self.collection_name]
