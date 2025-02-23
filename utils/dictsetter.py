from typing import Any


def dictGetter(obj:dict, path:str) -> dict | None:
    path = path.split("/")
    for p in path:
        try:
            if p == path[-1]:
                break
            obj = obj[p]
        except KeyError:
            return 
    
    return obj

def dictSetter(obj:dict, path:str, value:Any) -> dict | None :
    obj = dictGetter(obj, path)
    if obj == None:
        return
    
    path = path.split("/")
    key = path[-1]
    obj[key] = value
    return obj
