from sqlite3 import OperationalError
from db_manager.connection.sqlite_connection import sqlite
from uuid import UUID
from typing import List

# show info
import logging
logging.basicConfig(level=logging.INFO)

def row_exists(table_name:str, primary_key:UUID | int) -> bool:
    with sqlite.db_connection() as cur:
        try:
            query = f"SELECT * FROM {table_name} WHERE id=?"
            exist = cur.execute(query, (primary_key,)).fetchone()
            if exist != None:
                return True
        except OperationalError as err:
            print(f"An error ocurred while query was done. Probably the name typed doesn't exist. Table_name: {table_name}.\nError message: {err}")
        
        return False
    
def all_row_exists(table_name:List[str], primary_key:List[str|int]) -> bool:
    if len(table_name) != len(primary_key):
        return False
    
    with sqlite.db_connection() as cur:
        for t, p_key in zip(table_name, primary_key):
            try:
                query = f"SELECT * FROM {t} WHERE id=?"
                exist = cur.execute(query, (p_key,)).fetchone()
                if exist is None:
                    return False
            except OperationalError as err:
                logging.info(f"An error ocurred while query was done. Probably the name typed doesn't exist. Table_name: {t}.\nError message: {err}")
                return False
    
    return True
