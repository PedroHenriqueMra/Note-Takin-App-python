import json
import uuid
from pathlib import Path

from pydantic import BaseModel
# from ..file_work import File_Tasks

# The folders will be in a default path (always)
class Link(BaseModel):
    default_dir_path: Path = Path.cwd() / "notations-folder"
    link_dir_path: Path = Path.cwd() / "link"
    link_file_path: Path

    def __init__(self, **args):
        super().__init__(**args)
        self._create_dedfault_directories()
        self._create_structure_link_file()
        self.link_file_path = Path.joinpath(self.link_dir_path, "link.json")

    def _create_dedfault_directories(self) -> None:
        self.link_dir_path.mkdir(parents=True, exist_ok=True)
        self.default_dir_path.mkdir(parents=True, exist_ok=True)

    def _create_structure_link_file(self) -> None:
        try:
            open(self.link_file_path, 'x')
        except FileExistsError as e:
            print(f"This file already exists. Message: {e}")

    def create_link(self, text_id: str, note_id: str) -> Path:
        object = {
            "link_id": str(uuid.uuid4),
            "text-file_id": text_id,
            "note-file_id": note_id
        }
        serialize = json.dumps(object)
        try:
            with open(self.link_file_path, 'a') as f:
                f.write(serialize)
        except Exception as e:
            print(f"An error unexpected ocurred. Message: {e}")
        
        return self.link_file_path
