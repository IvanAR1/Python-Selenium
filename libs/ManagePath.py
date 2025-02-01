import os
import pathlib

def NormalizePath(path:str):
    return os.path.normpath(path)

def ExpandVars(path:str):
    return os.path.expandvars(path)

def NormalizePathExpandVars(path:str):
    path = ExpandVars(path)
    return NormalizePath(path)

def BaseName(path:str):
    return os.path.basename(path)

def GetNameFilesInPath(route:str):
    return [arch.name for arch in pathlib.Path(route).iterdir() if arch.is_file()]

def ExistFile(path:str):
    return os.path.exists(path)

def ExistPath(path:str):
    return os.path.isdir(path)

def AcceptFile(path:str, accept_files:str|list):
    if isinstance(accept_files, str):
        accept_files = accept_files.split("|")
    return os.path.splitext(path)[1] in accept_files

def CreatePath(path:str):
    if ExistPath(path) == False:
        os.makedirs(path)
    return path

def DeleteFile(file:str):
    if ExistFile(file):
        os.remove(file)

def DeletePath(path:str):
    if ExistPath(path):
        os.rmdir(path)