from libs.cmd.CheckCmd import get_type_of_param
from libs.cmd.Execute import create_model, create_project, initialize_driver
from libs.path.loader import charge_env

def main():
    """
    Main execution from console and initialize driver.
    
    Raises:
        ImportError: 
            If not found the folder of project/subproject , .main module or 
            execute_from_command_line function in .main module
    """
    model = get_type_of_param("--make-model")
    createProject = get_type_of_param(["--make-project", "-mp"])
    runProject = get_type_of_param(["--run-project", "-rp"])
    if model:
        create_model(model)
    elif createProject:        
        create_project(createProject)
    elif runProject:
        charge_env()
        initialize_driver(runProject)

if __name__ == "__main__":
    main()