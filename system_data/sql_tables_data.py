from dataclasses import dataclass
from uuid import UUID
from uuid import uuid4

@dataclass
class Text:
    title:str
    content:str | None
    create_date:str = None
    edit_date:str = None
    type:str = "text"

@dataclass
class Note:
    linked_text_id:int
    reference:str
    content:str | None
    create_date:str = None
    edit_date:str = None
    type:str = "note"

@dataclass
class Link:
    text_id:int
    note_ids:list
    id:UUID = uuid4()
