class IGetterService:
    def get_link_data(self, link_id:str) -> dict | None:
        raise NotImplementedError()
    
    def get_text_data(self, text_id:int) -> dict | None:
        raise NotImplementedError()
    
    def get_notes_data(self, note_ids:list) -> list | None:
        raise NotImplementedError()
