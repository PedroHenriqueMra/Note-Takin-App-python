import os
import shutil
from pydantic import BaseModel
from typing import Dict
from typing import List


class Folder_Manager(BaseModel):
    current_directory: str = None
    directories: List[str] = list()

    def __init__(self, **args):
        super().__init__(**args)
        self._create_default_directory()

    def _create_default_directory(self):
        if self.current_directory == None:
            # Default path
            default_path = os.getcwd() + "\\Default-Folder"
            self.current_directory = default_path

        if not os.path.exists(self.current_directory):
            os.makedirs(self.current_directory)
        self.directories.append(self.current_directory)

    def add_directory(self, path_directory:str) -> str:
        if not os.path.exists(path_directory):
            os.mkdir(path_directory)
            self.directories.append(path_directory)
            self.current_directory = path_directory
            return path_directory
        return ""
    
    def delete_directory(self, directory:str):
        if directory in self.directories:
            os.remove(directory)
            self.directories.remove(directory)
        
        if self.current_directory == directory:
            if len(self.directories) == 0:
                self._create_default_directory()
            else:
                self.current_directory = self.directories[0]

    # def move_directory(self, directory:str, dest:str) -> str:        
    #     # if this dir is not on the system it will not be possible to move it
    #     if directory not in self.directories:
    #         return ""
    #     self.directories.remove(directory)
        
    #     if not os.path.isdir(dest):
    #         os.mkdir(dest)

    #     try:  
    #         path_returned = shutil.move(directory, dest)
    #         self.directories.append(path_returned)
            
    #         if self.current_directory == directory:
    #             self.current_directory = path_returned

    #         if os.path.exists(directory):
    #             os.remove(directory)
            
    #         return path_returned
    #     except Exception as e:
    #         print(f"Error: \n{e}")
    #         return ""
