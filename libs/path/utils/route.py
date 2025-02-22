from os import path
from typing import AnyStr

def NormalizePath(route_path: str) -> AnyStr:
    """Normalize an route to actual SO
    Args:
        route_path (str): A path-like object representing a file system path. 

    Returns:
        str: route normalized 
    """
    return path.normpath(route_path)

def ExpandVars(route_path: str) -> AnyStr:
    """Expande las variables de entorno en la ruta.

    Args:
        route_path (str): A path-like object representing a file system path.

    Returns:
        str: route with vars expanded
    """
    return path.expandvars(route_path)

def NormalizePathExpandVars(route_path: str) -> AnyStr:
    """Normalize route y expand environment vars.

    Args:
        route_path (str): A path-like object representing a file system path. 

    Returns:
        str: route normalized and vars expended
    """
    return NormalizePath(ExpandVars(route_path))

def CheckAbsPath(route_path: str) -> AnyStr:
    """Get absolute route of directory

    Args:
        route_path (str): A path-like object representing a file system path.

    Returns:
        AnyStr: Route with path absolute.
    """
    return path.abspath(route_path)

def CheckDirnamePath(route_path: str) -> AnyStr:
    """Returns the directory component of a pathname

    Args:
        route_path (str): A path-like object representing a file system path. 

    Returns:
        str: This method returns a string value which represents the directory name from the specified path.
    """
    return path.dirname(route_path)

def ExistPath(*routes_path:str):
    """Check if file/folder exists.

    Args:
        routes_path (str): Files or folders path.

    Returns:
        bool: If all files / folders exists.
    """
    for route in routes_path:
        if not path.exists(route):
            return False
    return True

def JoinPath(*routes_path:str) -> str:
    """Join some directories. Recommended finished with a file_name.

    Returns:
        str: End route
    """
    end_route = ""
    for route in routes_path:
        end_route = path.join(route)
    return end_route

def FileContainStr(route_path: str, search: str) -> bool:
    """Search if str of file is contains in a route

    Args:
        route_path (str): File or directory path.
        search (str): Text to search.

    Returns:
        bool: If text is in route.
    """
    return search in route_path.lower()