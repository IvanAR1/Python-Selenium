
from pathlib import Path
from itertools import chain
from shutil import rmtree, move
from config.framework import PATH_STRICT
from typing import Callable, List, Union, overload, TypeAlias, Any, Literal

FormatName: TypeAlias = Literal["only_name", "full_path"]

def ExistFolder(*folders_path: str) -> bool:
    """Whether this path is a directory.

    Args:
        folders_path (str): Folders path.

    Returns:
        bool: If all folders are exists.
    """
    for folder in folders_path:
        if not Path(folder).is_dir():
            return False
    return True

@overload
def FindFiles(folder_path:str, patterns: Union[str, List[str]]) -> List[Path|str]:...
def GlobFiles(folder_path:str, patterns: Union[str, List[str]]) -> List[Path|str]:
    """Helper function to get files matching patterns in a folder.

    Args:
        folder_path (str): Folder path.
        patterns (Union[str, List[str]]): Patterns to filter files. Defaults to "*". If string, separate with "|"

    Returns:
        List[Path|str]: List of files (usually Path)
    """
    if isinstance(patterns, str):
        patterns =  patterns.split("|")
    return list(chain.from_iterable(Path(folder_path).glob(pattern) for pattern in patterns))

@overload
def GetFilesInFolder(folder_path: str, patterns: Union[str, list] = "*") -> List[Path]: ...
@overload
def GetFilesInFolder(folder_path: str, format: FormatName|Callable[[Path], Path], patterns: Union[str, list] = "*") -> List[str]: ...
def GetFilesInFolder(folder_path: str, patterns:Union[str|list] = "*", format:Union[None, FormatName, Callable[[Path], Path]] = None ) -> List[Path|str]:
    """Get a list of files in specific directory.
    Args:
        folder_path (str): Folder path.
        patterns (Union[str | list], optional): Patterns to filter files. Defaults to "*". If string, separate with "|"
        format (Union[None, FormatName, Callable[[Path], Path]], optional): Choose between [None, "full_path", "only_name"] or manage arch. Defaults to None.

    Returns:
        List[Path|str]: List of files (usually Path)
    """
    files = GlobFiles(folder_path, patterns)
    match format:
        case "only_name":
            return [file.name for file in files] 
        case "full_path":
            return [str(file.resolve(PATH_STRICT)) for file in files]
        case format if callable(format):
            archs = []
            for arch in files:
                if arch.is_file():
                    archs.append(format(arch))
            return archs
        case _:
            return files

def CreateFolder(folder_path: str, mode:int=511) -> str:
    """Create a new directory at this given path.

    Args:
        folder_path (str): Folder path.

    Returns:
        str: Folder path.
    """
    Path(folder_path).mkdir(parents=not PATH_STRICT, exist_ok=not PATH_STRICT, mode=mode)
    return folder_path

def MoveFolder(folder_src_path:str, folder_dst_path:str, overwrite:bool = False):
    """Move and folder to other ubication.

    Args:
        folder_src_path (str): Folder src path.
        folder_dst_path (str): Folder to path.
        overwrite (bool, optional): If destiny folder already exists, deleted if overwrite is True. Defaults to False.

    Raises:
        FileNotFoundError: If folder source not exists.
        FileExistsError: If overwrite is False and destiny folder already exists, or PATH_STRICT is enabled.
        ValueError: If PATH_STRICT is enabled and source folder is subdirectory of destiny folder. 

    Returns:
        _PathReturn: Path destiny
    """
    folder_src_path:Path = Path(folder_src_path)
    folder_dst_path:Path = Path(folder_dst_path)
    if not ExistFolder(folder_src_path):
        raise FileNotFoundError(f"Source folder {folder_src_path} not exist.")
    if ExistFolder(folder_dst_path):
        if overwrite:
            DeleteFolder(folder_dst_path)
        else:
            raise FileExistsError(f"Destination folder {folder_dst_path} already exists.")
    if PATH_STRICT and folder_src_path in folder_dst_path.parents:
        raise ValueError(f"Strict mode enabled: Cannot move {folder_src_path} into its own subdirectory {folder_dst_path}.")
    return move(str(folder_src_path), str(folder_dst_path))

def DeleteFolder(folder_path:str):
    """Delete a folder

    Args:
        folder_path (str): _description_

    Raises:
        FileExistsError: If PATH_STRICT is enabled.

    Returns:
        str: folder_path if deleted.
        None: if folder not exist.
    """
    if ExistFolder(folder_path):
        if PATH_STRICT:
            raise FileExistsError(f"Strict mode enabled: Cannot overwrite {folder_path} and others folders.")
        rmtree(folder_path, ignore_errors=PATH_STRICT)
        return folder_path

def RecursiveFiles(folder_path: str, callback: Callable[[Path], Any] = None, patterns: Union[str, List] = "*") -> List[str]:
    """Find recursive in folder and applied a callback.

    Args:
        folder_path (str): Folder path.
        callback (Callable[[Path], Any], optional): Applied an callback to get file. Defaults to None.
        patterns (Union[str, List], optional): Patterns to filter files. Defaults to "*". If string, separate with "|"

    Returns:
        List[str]: List of files, or values returned in callback.
    """
    values_returned = []
    if ExistFolder(folder_path):
        for file in GetFilesInFolder(folder_path, patterns):
            if isinstance(callback, Callable):
                value_returned = callback(file)
                if value_returned:
                    values_returned.append(value_returned)
                continue
            values_returned.append(file)
    return values_returned

def CurrentWorkingDirectory(file_path:str = __file__):
    """Returned current working directory.
    Args:
        file_path (str, None): Specific file working directory. Defaults to __file__.
    Returns:
        str: Actual working directory.
    """
    return Path(file_path).cwd()