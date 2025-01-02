from db_manager.repository.irepository import IRepository

from db_manager.config.configdb import db

class ADMText(IRepository):
    def _IRepository__create_table(self):
        # create table
        exist = db.table_exists("text")
        if not exist:
            print("criado")
            db.cur.execute("CREATE TABLE text(id, type, title, content, date infos)")


    def add(self, content:dict) -> str:
        pass

    def remove(self, id) -> str:
        pass

    def get_by_id(self, id) -> str:
        pass
