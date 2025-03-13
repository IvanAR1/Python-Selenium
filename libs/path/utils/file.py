import errno
from pathlib import Path
from shutil import copyfile
from config.framework import PATH_STRICT
from typing import Union, TypeAlias, Literal

ActionCopyMove:TypeAlias = Literal["copy","move"]
ActionManageExtension:TypeAlias = Literal["only", "without"]
ActionReadFile:TypeAlias = Literal["text", "bytes"]

def BaseName(file_path: str) -> str:
    """Get basename of file

    Args:
        file_path (str): File path.

    Returns:
        str: Return filename with extension
    """
    return Path(file_path).name

def FileContainsExtension(file_path:str, extensions:Union[str, list[str]]) -> bool:
    """Check if file contains extension
    Args:
        file_path (str): File path.
        extensions (Union[str, List[str]]): Patterns to filter files. If string, separate with "|"

    Returns:
        List[Path|str]: List of files (usually Path)
    """
    if isinstance(extensions, str):
        extensions = extensions.split("|")
    return f".{file_path.rsplit('.', 1)[-1]}" in extensions

def ManageExtension(file_path: str, action:ActionManageExtension="without", conserved_route:bool = True) -> str:
    """Get filename without extension
    Args:
        file_path (str): File path.
        action (ActionManageExtension): Action between ('only', 'without')
        conserved_route (bool, optional): If file contains a route, its conserved if value is True. Defaults to True.

    Returns:
        str: The final path component.
    """
    if not conserved_route:
        file_path = str(Path(file_path).stem)
    file_path = file_path.rsplit(".", 1)
    match action:
        case "only":
            return file_path[-1]
        case "without":
            return file_path[0]

def WithoutExtension(file_path: str, conserved_route = True) -> str:
    """Get filename without extension
    Args:
        file_path (str): File path.
        conserved_route (bool, optional): If file contains a route, its conserved if value is True. Defaults to True.

    Returns:
        str: The final path component.
    """
    if conserved_route:
        return file_path.rsplit(".", 1)[0]
    return Path(file_path).stem

def ExistFile(*files_path: str) -> bool:
    """Whether this path is a regular file (also True for symlinks pointing to regular files).
    Args:
        files_path (tuple[str, ...]): files path

    Returns:
        bool: If all files are exists
    """
    for file in files_path:
        if not Path(file).is_file():
            return False
    return True

def GetFileContent(file_from:str, mode:ActionReadFile="text", **kwargs:str|None) -> Union[str,bytes, None]:
    """Get contents from file.

    Args:
        file_from (str): File path.
        mode (ActionReadFile, optional): Mode to read between (text|bytes). Defaults to "text".
        **kwargs (str|None): some options in pathlib.Path.read_text

    Raises:
        TypeError: If mode to read file is not between [text|bytes]

    Returns:
        Union[str,bytes]: File readed.
        
        None: File not exists.
    """
    if ExistFile(file_from):
        file_from:Path = Path(file_from)
        match mode:
            case "text":
                return file_from.read_text(**kwargs)
            case "bytes":
                return file_from.read_bytes()
            case _:
                raise TypeError("Read file mode not accepted.")
            
def CreateFile(file_path:str, strContent:str = "", mode:TypeAlias = "w", **kwargs) -> None:
    """Create an file and write text

    Args:
        file_path (str): File path
        strContent (str, optional): Content to write in file. Defaults to "".

    Returns:
        str: File path
    """
    file_path:Path = Path(file_path)
    if PATH_STRICT and file_path.is_file():
        raise FileExistsError(f"Strict mode enabled: {file_path} already exists.")
    with open(file_path, mode, **kwargs) as file:
        file.write(strContent)
    return file_path

def CopyMoveFile(file_from_path:str, file_to_path:str, action:ActionCopyMove) -> Union[ tuple[str, str] | None]:
    """Copy an file to other ubication.

    Args:
        file_from_path (str): Filename from path
        file_to_path (str): Filename to path

    Returns:
        Union[ tuple[str, str] | None]: returns files if they're moved. If they aren't created, return None
    """
    folder_to = Path(file_to_path).parent.resolve()
    if not ExistFile(file_from_path) or folder_to.is_file():
        return None
    match action:
        case "copy":
            copyfile(file_from_path, file_to_path)
            return file_from_path, file_to_path
        case "move":
            Path(file_from_path).rename(file_to_path)
            return file_from_path, file_to_path
            
def DeleteFile(*files_path:str):
    """Delete some files

    Args:
        files_path (str): Files path

    Raises:
        PermissionError: If strict mode is enabled.

    Returns:
        List[str, None]: Deleted files log
    """
    if PATH_STRICT:
        raise PermissionError(f"Strict mode enabled: Deletion of file {files_path} and others files are blocked.")
    files_log = []
    for file in files_path: 
        if ExistFile(file):
            Path(file).unlink()
            files_log.append(file)
    return files_log

def FileNotUsed(file_path:str) -> bool:
    """Check if file is not used

    Args:
        file_path (str): File path

    Returns:
        bool: If file is not used
    """
    if not ExistFile(file_path):
        return False
    try:
        # Attempt to open the file in exclusive mode (will fail if it's open elsewhere)
        with open(file_path, 'r+') as file:
            file.close()
            return True  # File is not in use
    except IOError as e:
        if e.errno == errno.EACCES or e.errno == errno.EPERM:
            return False  # File is in use (permission denied)
        else:
            return True  # Other error, assume not in use