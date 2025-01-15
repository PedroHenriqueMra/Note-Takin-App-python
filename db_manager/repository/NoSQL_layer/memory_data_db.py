from ...connection.mgdb_connection import mongo_database
from pydantic import BaseModel

class MemoryDataDB(BaseModel):

    database_name:str = "memory_data"

    
