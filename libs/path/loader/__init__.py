"""Load charger between [".env" | ".env.json"] by EXTENSION_LOADER into config/framework

Raises:
    ImportError: If charger is not between [".env" | ".env.json"]
"""
from config.framework import EXTENSION_LOADER
from typing import TypeAlias, Literal
from ..utils.file import BaseName

ExtensionsLoader:TypeAlias = Literal[".env", ".env.json"]
EXTENSION_LOADER = extension_loader = BaseName(EXTENSION_LOADER)
match EXTENSION_LOADER:
    case ".env":
        from . import env
        charge_env = env.charge_env
        env = env.env
    case ".env.json":
        from . import json
        charge_env = json.charge_env
        env = json.env
    case _:
        raise ImportError(f"Select an loader between {ExtensionsLoader}")
__all__ = [env, charge_env, extension_loader]