import json
from pathlib import Path
from libs.cmd.CheckCmd import get_type_of_param

def set_name_project(file:str) -> str:
    """Format the file name based on the project parameters.

    Args:
        file (str): The file name to format.

    Returns:
        str: The formatted file name.
    """
    project = get_type_of_param(["--run-project", "-rp"]) or ""
    split_project = Path(project).parts
    file_formated = str(file or ".env").format(
        path_project = project,
        name_project = split_project[-1] if len(split_project) > 1 else "",
        root_project = split_project[0] if len(split_project) > 1 else "",
    )
    return file_formated

def JSON(file:str, **kwargs) -> dict:
    """Load a JSON file and return its contents as a dictionary.

    Args:
        file (str): The path to the JSON file.
        **kwargs: Additional keyword arguments to pass to the json.load function.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If there is an error decoding the JSON file.

    Returns:
        dict: The contents of the JSON file.
    """
    try:
        return json.load(open(file, 'r'), **kwargs)
    except FileNotFoundError as e:
        raise FileNotFoundError("File %s not found: %s" % (file, e))
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError("An error ocurred when decoding JSON: %s" % e)