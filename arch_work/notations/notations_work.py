from pydantic import BaseModel
from ..file_work import File_Tasks

class Notations(File_Tasks, BaseModel):
    
    
    def __init__(self, **args):
        super().__init__(**args)
