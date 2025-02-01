import os, re, json
from pathlib import Path
from dotenv import load_dotenv
from config.framework import EXTENSION_LOADER
from libs.cmd.CheckCmd import get_type_of_param
from .path_utils import ExistFile, AcceptFile, BaseName

env_json={}
extension_loader = (EXTENSION_LOADER or ".env").rsplit(".",1)[-1]
def env(index:str) -> str|float:
    match extension_loader:
        case "env":
            return os.getenv(index)
        case "json":
            return _manage_case_json(index)

def JSON(file:str) -> dict:
    try:
        return json.load(open(file, 'r'))
    except FileNotFoundError as e:
        raise FileNotFoundError("El archivo %s no existe: %s" % (file, e))
    except json.JSONDecodeError as e:
        raise Exception("Error al decodificar JSON: %s" % e)
    
def chargeEnv(file:str = "") -> dict:
    from warnings import warn
    warn("This method changed name to 'charge_env'.This function will be removed in a future.", DeprecationWarning)
    charge_env(file)

def charge_env(file:str = "") -> None:
    project = get_type_of_param(["--run-project", "-rp"])
    file = str.format(file or ".env", project_name = ("", project)[project != None] )
    if ExistFile(file):
        try:
            match extension_loader:
                case "env" | "":
                    if AcceptFile(file, f".{extension_loader}") or file != f".{extension_loader}":
                        load_dotenv(dotenv_path=Path(file))
                    elif file == f".{extension_loader}":
                        load_dotenv()
                case "json":
                    global env_json
                    if BaseName(file) == f".{extension_loader}":
                        env_json.update(JSON(file))
        except FileNotFoundError as e:
            raise FileNotFoundError("El archivo %s no existe: %s" % (file, e))
        except ValueError as e:
            raise ValueError("Error al cargar el archivo: %s" % e)
    
def _manage_case_json(index:str):
    pattern = re.compile(r'(\w+)(\[\d+\])?')
    keys = []
    for part in index.split('.'):
        matched = pattern.match(part)
        if matched:
            keys.append(matched.group(1))
            if matched.group(2):
                keys.append(int(matched.group(2)[1:-1]))
    result = env_json
    for key in keys:
        if isinstance(key, int):
            try:
                result = result[key]
            except IndexError as e:
                raise IndexError(f"Not exist key {key} in key {result}")
        elif isinstance(key, str):
            result = result.get(key)
    return result