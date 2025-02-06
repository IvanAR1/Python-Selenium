import os
import shutil
import pathlib
from typing import Callable, List, Union

# Normalización de rutas
def NormalizePath(path: str) -> str:
    """Normaliza la ruta para el sistema operativo actual."""
    return os.path.normpath(path)

def ExpandVars(path: str) -> str:
    """Expande las variables de entorno en la ruta."""
    return os.path.expandvars(path)

def NormalizePathExpandVars(path: str) -> str:
    """Normaliza la ruta y expande variables de entorno."""
    return NormalizePath(ExpandVars(path))

def CheckAbsPath(path: str) -> str:
    """Obtiene la ruta absoluta de un directorio."""
    return os.path.abspath(path)

def CheckAbsPathFile(filePath: str) -> str:
    """Obtiene la ruta absoluta del directorio de un archivo."""
    return os.path.dirname(CheckAbsPath(filePath))

def BaseName(path: str) -> str:
    """Obtiene el nombre base de una ruta."""
    return os.path.basename(path)

def WithoutExtension(file: str) -> str:
    """Obtiene el nombre del archivo sin su extensión."""
    return file.rsplit(".", 1)[0]

# Operaciones con archivos y directorios
def GetArchFilesInPath(path: str) -> List[pathlib.Path]:
    """Obtiene una lista de archivos en el directorio especificado."""
    return [arch for arch in pathlib.Path(path).iterdir() if arch.is_file()]

def GetNameFilesInPath(path: str, accept_files: Union[str, List[str]] = None) -> List[str]:
    """Obtiene los nombres de los archivos en un directorio con extensiones aceptadas."""
    all_files = [arch.name for arch in GetArchFilesInPath(path)]
    if accept_files:
        all_files = [file for file in all_files if AcceptFile(file, accept_files)]
    return all_files

def GetFullPathFilesInPath(path: str, accept_files: Union[str, List[str]] = None) -> List[str]:
    """Obtiene las rutas completas de los archivos en un directorio con extensiones aceptadas."""
    all_files = [str(arch.resolve()) for arch in GetArchFilesInPath(path)]
    if accept_files:
        all_files = [file for file in all_files if AcceptFile(file, accept_files)]
    return all_files

def ExistFile(path: str) -> bool:
    """Verifica si un archivo existe."""
    return os.path.exists(path)

def ExistPath(path: str) -> bool:
    """Verifica si un directorio existe."""
    return os.path.isdir(path)

def AcceptFile(file_path:str, accept_files:Union[str, List[str]]) -> bool:
    """Verifica si un archivo tiene una extensión aceptada."""
    if isinstance(accept_files, str):
        accept_files = accept_files.split("|")
    return f".{file_path.rsplit('.', 1)[-1]}" in accept_files

def CreatePath(path: str) -> str:
    """Crea un directorio si no existe."""
    if not ExistPath(path):
        os.makedirs(path)
    return path

def CreateFile(filePath: str, strContent: str = "") -> None:
    """Crea un archivo con el contenido especificado."""
    with open(filePath, "w") as f:
        f.write(strContent)

def CopyFile(fileFrom: str, fileTo: str) -> None:
    """Copia un archivo a otra ubicación."""
    if ExistFile(fileFrom):
        shutil.copyfile(fileFrom, fileTo)

def MoveFile(fileFrom: str, fileTo: str) -> None:
    """Mueve un archivo a otra ubicación."""
    if ExistFile(fileFrom):
        if not ExistPath(CheckAbsPathFile(fileTo)):
            CreatePath(CheckAbsPathFile(fileTo))
        pathlib.Path(fileFrom).rename(fileTo)

def DeleteFile(file: str) -> None:
    """Elimina un archivo si existe."""
    if ExistFile(file):
        os.remove(file)

def DeletePath(path: str) -> None:
    """Elimina un directorio si está vacío."""
    if ExistPath(path):
        os.rmdir(path)

def JoinFile(path: str, file: str) -> str:
    """Une una ruta y un nombre de archivo."""
    return os.path.join(path, file)

def FileContainStr(file: str, search: str) -> bool:
    """Verifica si un archivo contiene una cadena específica en su nombre."""
    return search in file.lower()

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

def CountValidFiles(folder_path: str, valid_extensions: Union[str, List[str]] = None) -> int:
    """
    Cuenta archivos con extensiones válidas en una carpeta.

    :param folder_path: Ruta al directorio.
    :param valid_extensions: Lista de extensiones válidas (e.g., ['.txt', '.jpg'] | ".txt|.str").
    :return: Cantidad de archivos con extensiones válidas.
    """
    folder = pathlib.Path(folder_path)
    return sum(1 for file in folder.iterdir() if file.is_file() and AcceptFile(file.name, valid_extensions))