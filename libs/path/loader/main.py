import json
from pathlib import Path

def set_name_project(file:str = ""):
    project = file
    split_project = Path(project).parts
    file = str(file or ".env").format(
        path_project = project, 
        name_project = split_project[-1] if len(split_project) > 1 else "",
        root_project = split_project[0] if len(split_project) > 1 else "",
    )
    return file

def JSON(file:str, **kwargs) -> dict:
    try:
        return json.load(open(file, 'r'), **kwargs)
    except FileNotFoundError as e:
        raise FileNotFoundError("El archivo %s no existe: %s" % (file, e))
    except json.JSONDecodeError as e:
        raise Exception("Error al decodificar JSON: %s" % e)