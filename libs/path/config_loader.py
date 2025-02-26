import os
import re
import json
import inspect
import warnings
import functools
from pathlib import Path
from dotenv import load_dotenv
from .path_utils import AcceptFile, BaseName
from config.framework import EXTENSION_LOADER
from libs.cmd.CheckCmd import get_type_of_param


def deprecated(func):
    warnings.simplefilter('always', DeprecationWarning)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        frame = inspect.stack()[1]
        message = (
            f"{func.__name__} and all methods in module 'libs.path.config_loader' are deprecated and deleted in other version. Please, use the module 'libs.path.loader'; version=1.0.0"
            f"\nCalled from {frame.filename}, file {frame.lineno}"
        )
        warnings.warn(message,
            category=DeprecationWarning, 
            stacklevel=2
        )
        warnings.simplefilter("default", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper

env_json={}
extension_loader = (EXTENSION_LOADER or ".env").rsplit(".",1)[-1]

@deprecated
def env(index:str|list|tuple, default:str|float="") -> str|float:
    match extension_loader:
        case "env":
            return os.getenv(index) or default
        case "json":
            return _manage_case_json(index) or default

@deprecated
def JSON(file:str) -> dict:
    try:
        return json.load(open(file, 'r'))
    except FileNotFoundError as e:
        raise FileNotFoundError("El archivo %s no existe: %s" % (file, e))
    except json.JSONDecodeError as e:
        raise Exception("Error al decodificar JSON: %s" % e)

@deprecated
def chargeEnv(file:str = "") -> dict:
    from warnings import warn
    warn("This method changed name to 'charge_env'.This function will be removed in a future.", DeprecationWarning)
    charge_env(file)

@deprecated
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

@deprecated
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