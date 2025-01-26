# Logic to found the first key found in a dictionary and return its key path
from typing import Optional
import ast


def find_keypath(obj:dict, key:str) -> Optional[dict|str]:
    """
        This function returns the full path of your dict structure where the first key name passed as argument is found.

        Args:
            obj (dict): The dictionary
            key (str): The name of the key you want to get path
        """
    
    res = get_dict_path(base_dict=obj, find_key=key, cur_path=[])
    parsed_path = generate_nested_dict(res)

    return parsed_path

def get_dict_path(base_dict:dict, find_key:str, cur_path:list=[]) -> Optional[list]:
    for k, v in base_dict.items():
        cur_path.append(k)

        if k is find_key:
            return cur_path
        
        if isinstance(v, dict):
            res = get_dict_path(v, find_key, cur_path)
            if res is not None:
                return res

        cur_path.pop()

# Parse a list to a nested dict as string format
def generate_nested_dict(path:list) -> Optional[dict|str]:
    if path == None:
        return None
    
    if len(path) == 1:
        return path[0]

    dict_string = str()
    for iter, p in enumerate(path):
        iter+=1
        if len(path) != iter:
            dict_string += "{"+ "'" + p + "'" +":"
        else:
            dict_string += "'" + p + "'"

    for _ in range(1, len(path)):
        dict_string += "}"

    parsed_path = ast.literal_eval(dict_string)
    return parsed_path
