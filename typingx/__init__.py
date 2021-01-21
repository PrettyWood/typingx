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
    is_newtype,
    is_typeddict,
)

__all__ = (
    # main methods
    "isinstancex",
    # typing, typing_extensions or own backport
    "Any",
    "Dict",
    "Generic",
    "Literal",
    "List",
    "Listx",
    "Mapping",
    "Optional",
    "NewType",
    "NoneType",
    "Union",
    "Set",
    "Sequence",
    "Tuple",
    "Tuplex",
    "Type",
    "TypeVar",
    "TypedDict",
    "get_args",
    "get_origin",
    "is_literal",
    "is_newtype",
    "is_typeddict",
)
