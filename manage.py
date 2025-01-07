import sys, importlib
from framework import WebDriver
from libs.path.config_loader import chargeEnv
from libs.cmd.CheckCmd import get_type_of_param
from libs.path.path_utils import ExistPath, ExistFile

def main():
    """
    Main execution from console and initialize driver.
    
    Raises:
        ImportError: 
            If not found the folder of project/subproject , .main module or 
            execute_from_command_line function in .main module
    """
    project_name = get_type_of_param("--project")
    if ExistPath(project_name):
        chargeEnv()
        if(ExistFile(project_name + "/.env")):
            chargeEnv(project_name + "/.env")
        try:
            full_module = "%s.main" %(project_name.replace("/",".").replace("\\","."))
            module = importlib.import_module(full_module)
            check_initialize()
            module.execute_from_command_line(get_type_of_param("--type"))
        except ImportError as e:
            raise ImportError(
                "In line %s from %s error ocurred: %s." 
                %(sys.exc_info()[-1].tb_lineno, sys.exc_info()[-1].tb_frame.f_code.co_filename, e)
            );

def check_initialize():
    option_ni = get_type_of_param("--not-init") or get_type_of_param("-ni")
    match option_ni:
        case "":
            pass
        case _:
            WebDriver.initialize_driver()

if __name__ == "__main__":
    main()