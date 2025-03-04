from os import path
from pathlib import Path
from typing import AnyStr

def NormalizePath(route_path: str) -> AnyStr:
    """Return the string representation of the path with forward (/) slashes.
    Args:
        route_path (str): A path-like object representing a file system path. 
    Returns:
        str: route normalized
    """
    return str(Path(route_path).resolve())

def ExpandVars(route_path: str) -> AnyStr:
    """Expands vars in route.

    If route contains "~": Expand ~ and ~user constructions. If user or $HOME is unknown, do nothing.

    If not: Expand shell variables of form $var and ${var}. Unknown variables are left unchanged.
    
    Args:
        route_path (str): A path-like object representing a file system path.

    Returns:
        str: route with vars expanded
    """
    if "~" in route_path:
        return path.expanduser(route_path)
    return path.expandvars(route_path)

def NormalizePathExpandVars(route_path: str) -> AnyStr:
    """Normalize route y expand vars.

    Args:
        route_path (str): A path-like object representing a file system path. 

    Returns:
        str: route normalized and vars expanded.
    """
    return NormalizePath(ExpandVars(route_path))

def CheckAbsPath(route_path: str) -> AnyStr:
    """Get absolute route of directory

    Args:
        route_path (str): A path-like object representing a file system path.

    Returns:
        AnyStr: Route with absolute path.
    """
    return str( Path(route_path).absolute() )

def CheckDirnamePath(route_path: str) -> Path:
    """Returns the directory component of a pathname

    Args:
        route_path (str): A path-like object representing a file system path. 

    Returns:
        Path: The logical parent of the path.
    """
    return Path(route_path).parent

def ExistPath(*routes_path:str) -> bool:
    """Check if file/folder exists.

    Args:
        *routes_path (str): Files or folders path.

    Returns:
        bool: If all files / folders exists.
    """
    for route in routes_path:
        if not Path(route).exists():
            return False
    return True

def JoinPath(*routes_path:str) -> str:
    """Join some directories. Recommended finished with a file_name.

    Args:
        *routes_path (str): Some directories.
    Returns:
        str: End route
    """
    return str(Path(routes_path[0]).joinpath(*routes_path[1:]))

def FileContainStr(route_path: str, search: str) -> bool:
    """Search if str of file is contains in a route

    Args:
        route_path (str): File or directory path.
        search (str): Text to search.

    Returns:
        bool: If text is in route.
    """
    return search in route_path.lower()