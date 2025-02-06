from libs.path.config_loader import charge_env, env
import sys
import importlib
import re
from framework import WebDriver
from config.framework import EXTENSION_LOADER
from libs.cmd.CheckCmd import get_type_of_param
from libs.path.path_utils import (
    ExistFile,
    ExistPath,
    CreatePath,
    CreateFile,
    CheckAbsPath,
)


def initialize_driver(project_name: str | None):
    def check_initialize():
        option_ni = get_type_of_param(["--not-init", "-ni"])
        match option_ni:
            case "":
                pass
            case _:
                WebDriver.initialize_driver(env("BROWSER"), False)

    if isinstance(project_name, str) and ExistPath(project_name):
        if ExistFile(project_name + f"/{EXTENSION_LOADER}"):
            charge_env(project_name + f"/{EXTENSION_LOADER}")
        try:
            full_module = "%s.main" % (
                project_name.replace("/", ".").replace("\\", ".")
            )
            module = importlib.import_module(full_module)
            check_initialize()
            module.execute_from_command_line(get_type_of_param("--type"))
        except ImportError as e:
            raise ImportError(
                "In line %s from %s error ocurred: %s."
                % (
                    sys.exc_info()[-1].tb_lineno,
                    sys.exc_info()[-1].tb_frame.f_code.co_filename,
                    e,
                )
            )


def create_project(project_name: str | None):
    if isinstance(project_name, str) and not project_name == "":
        CreatePath(CheckAbsPath(project_name))
        contentPy = """def execute_from_command_line(action: str):
    pass
"""
        CreateFile(f"{project_name}\\main.py", contentPy)
        CreateFile(f"{project_name}\\{EXTENSION_LOADER or '.env'}")
        CreateFile(f"{project_name}\\{EXTENSION_LOADER or '.env'}.example")


def create_model(model: str):
    separatePath = re.split(r"[\\/]", re.sub(r"\s{2,}", "", model))
    nameModel = separatePath[-1]
    folder_path = "/".join(separatePath[:-1])
    if not folder_path:
        return
    table_name = get_type_of_param("--table")
    engine = get_type_of_param(["--engine", "--database"])
    table_name = (f'__tablename__ = "{table_name}"', "pass")[not table_name]
    engine = (f'__bind_key__ = "{engine}"', "")[not engine]
    if not ExistPath(folder_path):
        CreatePath(folder_path)
    contentModel = f"""from libs.databases import DBManager
from sqlalchemy import (
    Column, VARCHAR, Integer, DECIMAL
)
from sqlalchemy.orm import (
    Mapped, mapped_column
)

class {nameModel}(DBManager):
    {table_name}
    {engine}
"""
    CreateFile(f"{folder_path}/{nameModel}.py", contentModel)
