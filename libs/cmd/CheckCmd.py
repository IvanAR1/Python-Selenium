import sys, os, importlib

dict_cmd = {}
def get_all_params(listConsole:dict = dict_cmd):
    all_args = sys.argv
    for arg in all_args:
        if("--" in arg or "-" in arg):
            listConsole[arg] = ""
            continue
        arg_prev = all_args[all_args.index(arg) - 1]
        if(arg_prev in listConsole.keys()):
            listConsole[arg_prev] = arg
    return listConsole

def get_type_of_param(key: str) -> str|None:
    """
    Get params of console.

    Params:
        param (str):
          Index to found (example "--{param} {value}")

    Returns:
        str:
            Value passed in the param
        None:
            If not found the param
    """
    if(not dict_cmd):
        get_all_params(dict_cmd)
    if(key in dict_cmd.keys()):
        return dict_cmd.get(key)