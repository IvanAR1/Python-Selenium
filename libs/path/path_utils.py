import os
import errno
import shutil
import inspect
import pathlib
import warnings
import functools
from typing import Callable, List, Union

warnings.simplefilter('always', DeprecationWarning)

def deprecated(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        frame = inspect.stack()[1]
        message = (
            f"{func.__name__} and all methods in module 'libs.path.path_utils' are deprecated and deleted in other version. Please, use the module 'libs.path.utils'; version=1.0.0"
            f"\nCalled from {frame.filename}, file {frame.lineno}"
        )
        warnings.warn(message,
            category=DeprecationWarning, 
            stacklevel=2
        )
        warnings.simplefilter("default", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper

@deprecated
def NormalizePath(path: str) -> str:
    """Normaliza la ruta para el sistema operativo actual."""
    return os.path.normpath(path)

@deprecated
def ExpandVars(path: str) -> str:
    """Expande las variables de entorno en la ruta."""
    return os.path.expandvars(path)

@deprecated
def NormalizePathExpandVars(path: str) -> str:
    """Normaliza la ruta y expande variables de entorno."""
    return NormalizePath(ExpandVars(path))

@deprecated
def CheckAbsPath(path: str) -> str:
    """Obtiene la ruta absoluta de un directorio."""
    return os.path.abspath(path)

@deprecated
def CheckAbsPathFile(filePath: str) -> str:
    """Obtiene la ruta absoluta del directorio de un archivo."""
    return os.path.dirname(CheckAbsPath(filePath))

@deprecated
def BaseName(path: str) -> str:
    """Obtiene el nombre base de una ruta."""
    return os.path.basename(path)

@deprecated
def WithoutExtension(file: str) -> str:
    """Obtiene el nombre del archivo sin su extensión."""
    return file.rsplit(".", 1)[0]


@deprecated
def GetArchFilesInPath(path: str) -> List[pathlib.Path]:
    """Obtiene una lista de archivos en el directorio especificado."""
    return [arch for arch in pathlib.Path(path).iterdir() if arch.is_file()]

@deprecated
def GetNameFilesInPath(path: str, accept_files: Union[str, List[str]] = None) -> List[str]:
    """Obtiene los nombres de los archivos en un directorio con extensiones aceptadas."""
    all_files = [arch.name for arch in GetArchFilesInPath(path)]
    if accept_files:
        all_files = [file for file in all_files if AcceptFile(file, accept_files)]
    return all_files

@deprecated
def GetFullPathFilesInPath(path: str, accept_files: Union[str, List[str]] = None) -> List[str]:
    """Obtiene las rutas completas de los archivos en un directorio con extensiones aceptadas."""
    all_files = [str(arch.resolve()) for arch in GetArchFilesInPath(path)]
    if accept_files:
        all_files = [file for file in all_files if AcceptFile(file, accept_files)]
    return all_files

@deprecated
def ExistFile(*files_path: str) -> bool:
    """Verifica si un archivo existe."""
    for file_path in files_path:
        if not os.path.exists(file_path):
            return False
    return True

@deprecated
def ExistPath(*folders_path: str) -> bool:
    """Verifica si un directorio existe."""
    for folder_path in folders_path:
        if not os.path.isdir(folder_path):
            return False
    return True

@deprecated
def AcceptFile(file_path:str, accept_files:Union[str, List[str]]) -> bool:
    """Verifica si un archivo tiene una extensión aceptada."""
    if isinstance(accept_files, str):
        accept_files = accept_files.split("|")
    return f".{file_path.rsplit('.', 1)[-1]}" in accept_files

@deprecated
def CreatePath(*folders_path: str) -> str:
    """Crea un directorio si no existe."""
    for folder_path in folders_path:
        if not ExistPath(folder_path):
            os.makedirs(folder_path)
    return folders_path

@deprecated
def CreateFile(filePath: str, strContent: str = "") -> None:
    """Crea un archivo con el contenido especificado."""
    with open(filePath, "w") as f:
        f.write(strContent)

@deprecated
def CopyFile(fileFrom: str, fileTo: str) -> None:
    """Copia un archivo a otra ubicación."""
    if ExistFile(fileFrom):
        shutil.copyfile(fileFrom, fileTo)

@deprecated
def MoveFile(fileFrom: str, fileTo: str, implements="rename", **kwargs) -> None:
    """Mueve un archivo a otra ubicación."""
    if ExistFile(fileFrom):
        if not ExistPath(CheckAbsPathFile(fileTo)):
            CreatePath(CheckAbsPathFile(fileTo))
        match implements:
            case "rename":
                pathlib.Path(fileFrom, **kwargs).rename(fileTo)
            case "shutil":
                shutil.move(fileFrom, fileTo, **kwargs)

@deprecated
def DeleteFile(file: str) -> None:
    """Elimina un archivo si existe."""
    if ExistFile(file):
        os.remove(file)

@deprecated
def DeletePath(path: str) -> None:
    """Elimina un directorio si está vacío."""
    if ExistPath(path):
        os.rmdir(path)

@deprecated
def JoinFile(path: str, file: str) -> str:
    """Une una ruta y un nombre de archivo."""
    return os.path.join(path, file)

@deprecated
def FileContainStr(file: str, search: str) -> bool:
    """Verifica si un archivo contiene una cadena específica en su nombre."""
    return search in file.lower()

@deprecated
def RecursiveFiles(path: str, callback: Callable[[str], bool] = None, accept_files: Union[str, List[str]] = None) -> List[str]:
    """Busca archivos recursivamente aplicando un callback."""
    values_returned = []
    if ExistPath(path):
        for file in GetFullPathFilesInPath(path, accept_files):
            if isinstance(callback, Callable):
                value_returned = callback(file)
                if value_returned:
                    values_returned.append(value_returned)
                continue
            values_returned.append(file)
    return values_returned

@deprecated
def CountValidFiles(folder_path: str, valid_extensions: Union[str, List[str]] = None) -> int:
    """
    Cuenta archivos con extensiones válidas en una carpeta.

    :param folder_path: Ruta al directorio.
    :param valid_extensions: Lista de extensiones válidas (e.g., ['.txt', '.jpg'] | ".txt|.str").
    :return: Cantidad de archivos con extensiones válidas.
    """
    folder = pathlib.Path(folder_path)
    return sum(1 for file in folder.iterdir() if file.is_file() and AcceptFile(file.name, valid_extensions))

@deprecated
def is_file_not_used(file_path:str):
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