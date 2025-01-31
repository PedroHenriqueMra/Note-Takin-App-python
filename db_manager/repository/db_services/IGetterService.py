class IGetterService:
    def get_link_data(self, link_id:str) -> dict:
        raise NotImplementedError()
    
    def get_text_data(self, text_id:int) -> dict:
        raise NotImplementedError()
    
    def get_notes_data(self, note_ids:list) -> list:
        raise NotImplementedError()
    
    def get_all_notes(self, note_ids:list) -> dict:
        raise NotImplementedError()
