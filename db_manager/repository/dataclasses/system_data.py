from dataclasses import dataclass

@dataclass
class Text:
    title:str
    content:str | None
    create_date:str = None
    edit_date:str = None
    type:str = "text"

    def response_error(msg=None) -> str|None:
        return msg if msg != None else ""

@dataclass
class Note:
    reference:str
    content:str | None
    create_date:str | None
    edit_date:str | None
    type:str = "note"