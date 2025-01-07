import os
import json
from pathlib import Path
from dotenv import load_dotenv

def env(index:str) -> str|float:
    return os.getenv(index)

def JSON(file:str) -> dict:
    try:
        with open(file) as file:
            data = json.load(file)
            return data
    except FileNotFoundError as e:
        raise FileNotFoundError("El archivo %s no existe: %s" % (file, e))
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError("Error al decodificar JSON: %s" % e)

def chargeEnv(file:str = "") -> dict:
    try:
        if file != "":
            load_dotenv(dotenv_path=Path(file))
        else:
            load_dotenv();
    except FileNotFoundError as e:
        raise FileNotFoundError("El archivo %s no existe: %s" % (file, e))
    except ValueError as e:
        raise ValueError("Error al cargar el archivo: %s" % e)