from irepository import IRepository

from db_manager.repository.dataclasses.note_type import Note
from db_manager.connection.connection import db

class ADMNote(IRepository[Note]):
    def __init__(self):
        db.get_connection()
        table = """
        CREATE TABLE IF NOT EXISTS note (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        type VARCHAR(5) NOT NULL,
        reference TEXT NOT NULL,
        content MEDIUMTEXT,
        create_date DATETIME NOT NULL,
        edit_date DATETIME NOT NULL
        );"""
        db.cur.execute(table)
        db.conn.commit()
        db.close_connection()

    def add(self, ) -> str:
        pass

    # def remove_by_id(self, id) -> str:
    #     pass

    # def get_by_id(self, id) -> bool:
    #     pass
