import re
from .main import set_name_project, JSON
from libs.path.utils.file import BaseName

env_json={}

def env(index:str|list|tuple, default:str|float="") -> str|float:
    """
    Retrieve the value from the JSON environment configuration using the provided index.
    
    *If the index is not found, return the default value.

    Args:
        index (str | list | tuple): The key or keys to look up in the JSON environment configuration.
        default (str | float, optional): The default value to return if the key is not found.. Defaults to "".

    Returns:
        str|float: The value from the JSON environment configuration or the default value.
    """
    return _manage_case_json(index) or default

def charge_env(file:str = ""):
    """Load environment variables from a .env.json file.

    Args:
        file (str, optional): The path to the .env.json file. If not provided, defaults to an empty string. Defaults to "".

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If there is an error loading the file.
    """
    try:
        file = set_name_project(file)
        global env_json
        if BaseName(file) == ".env.json":
            env_json.update(JSON(file))
    except FileNotFoundError as e:
        raise FileNotFoundError("File %s not found: %s" % (file, e))
    except ValueError as e:
        raise ValueError("An error ocurred when charge file: %s" % e)

def _manage_case_json(keys:str|list|tuple):
    """
    Retrieve the value from the JSON environment configuration using the provided keys.

    *Not use this functions, is private.

    Args:
        keys (str | list | tuple): The key or keys to look up in the JSON environment configuration.

    Raises:
        IndexError: If a key does not exist in the JSON environment configuration.

    Returns:
        Any: The value from the JSON environment configuration.
    """
    if isinstance(keys, str):
        pattern = re.compile(r'(\w+)(\[\d+\])?')
        new_keys = []
        for part in keys.split('.'):
            matched = pattern.match(part)
            if matched:
                new_keys.append(matched.group(1))
                if matched.group(2):
                    new_keys.append(int(matched.group(2)[1:-1]))
        keys = new_keys
    result = env_json
    for key in keys:
        try:
            if isinstance(key, int):
                result = result[key]
            elif isinstance(key, str):
                result = result.get(key)
        except (IndexError, AttributeError):
            raise IndexError(f"Not exist key {key} in json {env_json}")
    return result