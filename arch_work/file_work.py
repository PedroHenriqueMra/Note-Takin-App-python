import os
import json
from pydantic import BaseModel
from datetime import datetime
from typing import Dict
from typing import List

from arch_work.file_manager import File_Manager
from arch_work.folder_manager import Folder_Manager

# json format
class File_Tasks(File_Manager, Folder_Manager):
    def __init__(self, **args):
        super().__init__(**args)
        
        