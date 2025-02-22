from config.framework import EXTENSION_LOADER
from typing import TypeAlias, Literal
from ..utils.file import BaseName

ExtensionsLoader:TypeAlias = Literal[".env", ".env.json"]
extension_loader:ExtensionsLoader = BaseName(EXTENSION_LOADER)
match extension_loader:
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