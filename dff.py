from utils.get_change import Differ
from pprint import pprint

str1 = "olala lalsl oooo"
str2 = "olala oooo"
type = "text"
table_id = 1

service = Differ(str1, str2, type, table_id)
for obj in service.get_changeObjects():
    pprint(obj.gen_change_script())
