import os
import shutil
import pathlib
from typing import Callable

def NormalizePath(path:str):
    return os.path.normpath(path)

def ExpandVars(path:str):
    return os.path.expandvars(path)

def NormalizePathExpandVars(path:str):
    return NormalizePath(ExpandVars(path))

def CheckAbsPath(path:str):
    return os.path.abspath(path)

def CheckAbsPathFile(filePath:str):
    return os.path.dirname(CheckAbsPath(filePath))

def BaseName(path:str):
    return os.path.basename(path)

def GetArchFilesInPath(path:str):
    return [arch for arch in pathlib.Path(path).iterdir() if arch.is_file()]

def GetNameFilesInPath(path:str, accept_files:str|list = None):
    all_files = [arch.name for arch in GetArchFilesInPath(path)]
    if accept_files:
        all_files = [file for file in all_files if AcceptFile(file, accept_files)]
    return all_files

def GetFullPathFilesInPath(path:str, accept_files:str|list = None):
    all_files = [str(arch.resolve()) for arch in GetArchFilesInPath(path)]
    if accept_files:
        all_files = [file for file in all_files if AcceptFile(file, accept_files)]
    return all_files

def ExistFile(path:str):
    return os.path.exists(path)

def ExistPath(path:str):
    return os.path.isdir(path)

def AcceptFile(path:str, accept_files:str|list):
    if isinstance(accept_files, str):
        accept_files = accept_files.split("|")
    return os.path.splitext(path)[1] in accept_files

def CreatePath(path:str):
    if not ExistPath(path):
        os.makedirs(path)
    return path

def CopyFile(fileFrom:str, fileTo:str):
    if ExistFile(fileFrom):
        shutil.copyfile(fileFrom, fileTo)

def MoveFile(fileFrom:str, fileTo:str):
    if ExistFile(fileFrom):
        if not ExistPath(CheckAbsPathFile(fileTo)):
            CreatePath(CheckAbsPathFile(fileTo))
        pathlib.Path(fileFrom).rename(fileTo)

def DeleteFile(file:str):
    if ExistFile(file):
        os.remove(file)

def DeletePath(path:str):
    if ExistPath(path):
        os.rmdir(path)

def JoinFile(path:str, file:str):
    return os.path.join(path, file)

def FileContainStr(file:str, search:str):
    return search in file.lower()

def RecursiveFiles(path:str, callback:Callable, accept_files:str|list = None):
    files = []
    if ExistPath(path):
        for file in GetFullPathFilesInPath(path, accept_files):
            if callback(file):
                files.append(file)
    return files