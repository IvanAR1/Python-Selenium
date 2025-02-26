from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from .main import set_name_project
from libs.path.utils.file import FileContainsExtension

def env(index:str, default:str|float="") -> str|float:
    """
    Retrieve the value from the JSON environment configuration using the provided index.
    
    *If the index is not found, return the default value.

    Args:
        index (str): The key or keys to look up in the JSON environment configuration.
        default (str | float, optional): The default value to return if the key is not found.. Defaults to "".

    Returns:
        str|float: The value from the JSON environment configuration or the default value.
    """
    return getenv(index) or default

def charge_env(file:str = "", **kwargs) -> None:
    """Load environment variables from a .env file.

    Args:
        file (str, optional): The path to the .env file. If not provided, defaults to an empty string. Defaults to "".

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If there is an error loading the file.
    """
    file = set_name_project(file)
    if FileContainsExtension(file, ".env"):
        if file != ".env":
            load_dotenv(dotenv_path=Path(file), **kwargs)
        else:
            load_dotenv()