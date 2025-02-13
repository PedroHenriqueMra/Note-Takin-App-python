from bson.objectid import ObjectId


class TableNotExistsException(Exception):
    """
        Exception raised when a table not exists
         
        Attributes:
            table_id => table id
            message => exception message (optional)
    """
    
    def __init__(self, table_id:ObjectId|str, message:str="") -> None:
        self.table_id:ObjectId|str = table_id
        self.message:str = message

        super().__init__(self.table_id, self.message)

    def __str__(self):
        return "{} - in table id: {}".format(self.message, self.table_id)
    