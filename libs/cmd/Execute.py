import re
import sys
import importlib
from pathlib import Path
from framework import WebDriver
from libs.path.path_utils import ExistPath
from libs.path.utils.route import CheckAbsPath
from libs.cmd.CheckCmd import get_type_of_param
from libs.path.utils.file import ExistFile, CreateFile
from libs.path.utils.folder import CreateFolder, ExistFolder
from libs.path.loader import env, charge_env, extension_loader

folder_cmd:Path = Path(__file__).parent

def init(path_project:str|None):
    """Initialize the project/subproject

    Args:
        path_project (str | None): Where's the project
    """
    def check_initialize():
        option_ni = get_type_of_param(["--not-init", "-ni"])
        if option_ni is None:
            WebDriver.initialize_driver(env("BROWSER"))
    if isinstance(path_project, str) and ExistPath(path_project):
        if ExistFile(path_project + f"/{extension_loader}"):
            charge_env(path_project + f"/{extension_loader}")
        try:
            full_module = '%s.main' %(path_project.replace("/",".").replace("\\","."))
            module = importlib.import_module(full_module)
            check_initialize()
            module.execute_from_command_line(get_type_of_param("--action"))
        except ImportError as e:
            raise ImportError(
                "In line %s from %s error ocurred: %s." 
                %(sys.exc_info()[-1].tb_lineno, sys.exc_info()[-1].tb_frame.f_code.co_filename, e)
            )
    
def create_project(project_name:str|None):
    """Create an project

    Args:
        project_name (str | None): Where's the project
    """
    CreateFolder(CheckAbsPath(project_name))
    contentPy = folder_cmd.joinpath("templates/create_project").read_text()
    CreateFile(f"{project_name}\\main.py", contentPy)
    CreateFile(f"{project_name}\\{extension_loader or '.env'}")
    CreateFile(f"{project_name}\\{extension_loader or '.env'}.example")

def create_model(model:str):
    """Generate an model with SqlAlchemy

    Args:
        model (str): Where's alojed your model
    """
    separatePath = re.split(r"[\\/]", re.sub(r"\s{2,}","",model))
    nameModel = separatePath[-1]
    folder_path = "/".join(separatePath[:-1])
    if not folder_path:
        return
    table_name = get_type_of_param("--table")
    engine = get_type_of_param(["--engine", "--database"])
    table_name = f'__tablename__ = "{table_name}"' if table_name else ""
    engine = f'__bind_key__ = "{engine}"' if engine else ""
    if not ExistFolder(folder_path):
        CreateFolder(folder_path)
    contentModel = folder_cmd.joinpath("templates/model") \
        .read_text() \
        .format(
            nameModel=nameModel,
            table_name=table_name,
            engine=engine
        )
    CreateFile(f"{folder_path}/{nameModel}.py", contentModel)