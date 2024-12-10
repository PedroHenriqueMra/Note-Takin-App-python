import json
import os
from datetime import datetime
from pydantic import BaseModel
from typing import Dict
import uuid

class File_Manager(BaseModel):
    # file path selected
    file_path: str = None
    # json structure
    structure: Dict[str,str] = dict()

    def __init__(self, **args):
        super().__init__(**args)

    def _add_type_file(self, file:str) -> str:
        if not file.lower().endswith(".json"):
            return file + ".json"
        return file
    
    # add the necessary structure to file
    def _format_structure_file(self, file_path) -> str:
        self.structure["created_at"] = str(datetime.now().date())
        self.structure["updated_at"] = str(datetime.now().date())
        self.structure["id"] = str(uuid.uuid4())
        json_object = json.dumps(self.structure, indent=4)
        
        with open(file_path, "w") as json_file:
            json_file.write(json_object)

        return file_path
    
    def get_content(self) -> json:
        with open(self.file_path, "r") as f:
            return json.load(f)

    def create_file(self, p_directory:str, filename:str) -> str:
        # format file type
        filename = self._add_type_file(filename)

        if not os.path.exists(os.path.join(p_directory, filename)):
            # create file
            filename = os.path.join(p_directory, filename)
            f = open(filename, "x")
            f.close()
            
            filename = self._format_structure_file(filename)

        return self.file_path

    # overide file with new content
    def edit_field(self, field:str, content:str) -> str:
            if not os.path.exists(self.file_path):
                return ""

            with open(self.file_path, "r+") as f:
                data = json.load(f)
                if field in data:
                    data[field] = content
                    data["updated_at"] = str(datetime.now().date())
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                else:
                    return ""
    
    def delete_file(self, file_path:str):
        try:
            os.remove(file_path)
        except FileNotFoundError:
            print(f"There isn't any file with path {file_path}")
        except Exception as e:
            print(f"An unexpected error ocurred: {e}")
