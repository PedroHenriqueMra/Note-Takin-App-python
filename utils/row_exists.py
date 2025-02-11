from sqlite3 import OperationalError
from db_manager.connections.sqlite_connection import SqliteDB
from uuid import UUID
from typing import List, Any

# Show info
import logging
logging.basicConfig(level=logging.INFO)

# Sqlite instance
sqlite = SqliteDB()

def row_exists(table_name:str, primary_key:Any) -> bool:
    with sqlite.db_connection() as cur:
        query = "SELECT * FROM {} WHERE id = ?".format(table_name)
        exist = cur.execute(query, (primary_key,)).fetchone()
        if exist == None:
            return False
        
        return True
