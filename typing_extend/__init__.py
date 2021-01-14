# flake8: noqa
from typing import *

from .main import xisinstance
from .typing_compat import TypedDict, get_args, get_origin, is_typeddict

__all__ = (
    # main methods
    "xisinstance",
    # typing, typing_extensions or own backport
    "Any",
    "Dict",
    "List",
    "Optional",
    "Union",
    "Set",
    "Tuple",
    "Type",
    "TypedDict",
    "get_args",
    "get_origin",
    "is_typeddict",
)
