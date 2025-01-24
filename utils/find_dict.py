# Logic to found the first key found in a dictionary and return its key path
import ast

def get_dict_path_by_key(d_base:dict, find_key:str):
    """
    This function returns the full path of your dict structure where the first key name passed as argument is found.

    Args:
        d_base (dict): The dictionary
        find_key (str): The name of the key you want to get path
    """
    for k, v in d_base.items():
        # Variable to keep route path
        route_path = list()
        route_path.append(k)
        if k == find_key:
            yield generate_nested_dict(route_path)
            continue

        if isinstance(v, dict):
            res = yield from iter_in_nested_dict(v, find_key, route_path)
            if type(res) is type(dict):
                yield res


def iter_in_nested_dict(d_nested:dict, found_key:str, cur_path:list):
    for k, v in d_nested.items():
        if k == found_key:
            cur_path.append(k)
            yield generate_nested_dict(cur_path)
            continue

        if isinstance(v, dict):
            # Save current path and get in the next nested dict
            cur_path.append(k)
            yield from iter_in_nested_dict(v, found_key, cur_path)
            
            # If the last dict iterated was wrong:
            cur_path.pop()


# Parse a list to a nested dict as string format
def generate_nested_dict(path:list) -> dict | str:
    dict_string = str()
    if len(path) == 1:
        return path[0]

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
