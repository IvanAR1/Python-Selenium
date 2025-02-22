from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from .main import set_name_project
from libs.path.utils.file import FileContainsExtension

def env(index:str, default:str|float=""):
    return getenv(index) or default

def charge_env(file:str = "", **kwargs) -> None:
    file = set_name_project(file)
    if FileContainsExtension(file, ".env") or file != ".env":
        load_dotenv(dotenv_path=Path(file), **kwargs)
    elif file == ".env":
        load_dotenv()