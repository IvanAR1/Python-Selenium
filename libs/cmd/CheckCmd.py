import sys
from typing import Union, List, Tuple

dict_cmd = {}

def get_all_params():
    all_args = sys.argv[1:]
    listConsole = {}
    i = 0
    while i < len(all_args):
        arg = all_args[i]

        if arg.startswith("--") or (arg.startswith("-") and len(arg) > 1):
            if i + 1 < len(all_args) and not all_args[i + 1].startswith("-"):
                listConsole[arg] = all_args[i + 1]
                i += 1
            else:
                listConsole[arg] = ""
        i += 1
    global dict_cmd
    dict_cmd = listConsole
    return listConsole

def get_type_of_param(keys: Union[str, List, Tuple]) -> str | None:
    """
    Get params of console.

    Params:
        keys (Union[str, List, Tuple]):
          Index to found (example "--{param} {value}")
    Returns:
        str:
            Value passed in the param
        None:
            If not found the param
    """
    if not dict_cmd:
        get_all_params()

    match keys:
        case str():
            return dict_cmd.get(keys)
        case list() | tuple():
            return next((dict_cmd.get(k) for k in keys if k in dict_cmd), None)