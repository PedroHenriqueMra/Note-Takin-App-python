import json
from pathlib import Path
import uuid

from pydantic import BaseModel
# from ..file_work import File_Tasks

# The folders will be in a default path (always)
class Notations(BaseModel):
    def __init__(self, **args):
        super().__init__(**args)
        
