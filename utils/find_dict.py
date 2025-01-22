# Logic to found the first key found in a dictionary and return its key path

from typing import Generator


def find_first_key(d_base:dict, find_key:str):
    """
    This function returns the full path of your dict structure where the first key name passed as argument is found.

    Args:
        d_base (dict): The dictionary
        find_key (str): The name of the key you want to get path
    """
    for k, v in d_base.items():
        # Variable to keep route path
        route_path = list([k])
        if k == find_key:
            yield from key_found(route_path)

        if isinstance(v, dict):
            yield from find_in_nested_dict(v, find_key, route_path)


def find_in_nested_dict(d_nested:dict, found_key:str, cur_path:list):
    for k, v in d_nested.items():
        if k == found_key:
            cur_path.append(k)
            yield from key_found(cur_path)

        if isinstance(v, dict):
            # Save current path and get in the next nested dict
            cur_path.append(k)
            yield from find_in_nested_dict(v, found_key, cur_path)
            
            # If the last dict iterated was wrong:
            cur_path.pop()

# Parse a list to a dict as string format
def key_found(cur_path:list) -> str:
    parsed_path = dict()
    for index, key in enumerate(cur_path):
        try:
            parsed_path[key] = dict().fromkeys(cur_path[index+1])
        except:
            pass


    print(str(parsed_path))
    return str(parsed_path)

