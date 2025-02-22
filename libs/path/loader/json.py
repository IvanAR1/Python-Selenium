import re
from .main import set_name_project, JSON
from libs.path.utils.file import BaseName

env_json={}

def env(index:str|list|tuple, default:str|float="") -> str|float:
    return _manage_case_json(index) or default

def charge_env(file:str = ""):
    try:
        file = set_name_project(file)
        global env_json
        if BaseName(file) == ".env.json":
            env_json.update(JSON(file))
    except FileNotFoundError as e:
        raise FileNotFoundError("El archivo %s no existe: %s" % (file, e))
    except ValueError as e:
        raise ValueError("Error al cargar el archivo: %s" % e)

def _manage_case_json(keys:str|list|tuple):
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