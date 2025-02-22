import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv
from config.framework import EXTENSION_LOADER
from libs.cmd.CheckCmd import get_type_of_param
from .path_utils import AcceptFile, BaseName
from deprecated import deprecated

env_json={}
extension_loader = (EXTENSION_LOADER or ".env").rsplit(".",1)[-1]
execution = 0

Deprecation = deprecated(reason="All methods in module 'libs.path.config_loader' are deprecated and deleted in other version. Please, use the module 'libs.path.loader'"
                         ,version="1.0.0")
@Deprecation
def env(index:str|list|tuple, default:str|float="") -> str|float:
    match extension_loader:
        case "env":
            return os.getenv(index) or default
        case "json":
            return _manage_case_json(index) or default

@Deprecation
def JSON(file:str) -> dict:
    try:
        return json.load(open(file, 'r'))
    except FileNotFoundError as e:
        raise FileNotFoundError("El archivo %s no existe: %s" % (file, e))
    except json.JSONDecodeError as e:
        raise Exception("Error al decodificar JSON: %s" % e)

@Deprecation    
def chargeEnv(file:str = "") -> dict:
    from warnings import warn
    warn("This method changed name to 'charge_env'.This function will be removed in a future.", DeprecationWarning)
    charge_env(file)

@Deprecation
def charge_env(file:str = "") -> None:
    try:
        project = get_type_of_param(["--run-project", "-rp"]) or ""
        split_project = os.path.split(project)
        file = str(file or ".env").format(
            path_project = "/".join(split_project), 
            name_project = split_project[-1],
            root_project = split_project[0]
        )
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

@Deprecation    
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

if execution == 0:
    charge_env()
    execution = 1