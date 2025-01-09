from data.system_data import *
from db_manager.repository.note import ADMNote
from db_manager.repository.text import ADMText
from db_manager.repository.link_handler import ADMLink

# Test ADMText

text = ADMText()
txt = Text("titleTest", "COntentslda")
# text.add_row(txt)

# Test ADMNote

note = ADMNote()
# nt = Note(reference="lalal", content="lalla")
# note.delete_by_id(1)
# note.add_row(nt)

# Test link
link = ADMLink()
