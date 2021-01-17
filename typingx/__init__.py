# flake8: noqa
from typing import *

from .main import isinstancex
from .types import Listx, Tuplex
from .typing_compat import (
    Literal,
    NoneType,
    TypedDict,
    get_args,
    get_origin,
    is_literal,
    is_typeddict,
)

__all__ = (
    # main methods
    "isinstancex",
    # typing, typing_extensions or own backport
    "Any",
    "Dict",
    "Literal",
    "List",
    "Listx",
    "Optional",
    "NoneType",
    "Union",
    "Set",
    "Tuple",
    "Tuplex",
    "Type",
    "TypedDict",
    "get_args",
    "get_origin",
    "is_literal",
    "is_typeddict",
)
