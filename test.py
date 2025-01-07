from db_manager.repository.dataclasses.system_data import *
from db_manager.repository.text_adm import ADMText

# directory = "C:\\Users\\pedro\\OneDrive\\Documentos\\note-takin-app\\file-test"

text = ADMText()
txt = Text("title", "cpntent")
# text.add(txt)
# text.add(txt)
text.remove_by_id(6)
# text.get_by_id(1)
