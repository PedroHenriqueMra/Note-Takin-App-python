import threading
from db_manager.db_services.change_service.change_service import ChangeService


class AutoSaveService(ChangeService):
    def __init__(self, delay:float=4.0):
        self.delay = delay

    
    
    
    def save(self):
        pass
