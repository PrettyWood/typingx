# flake8: noqa
from typing import *

from .main import xisinstance
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
    "xisinstance",
    # typing, typing_extensions or own backport
    "Any",
    "Dict",
    "Literal",
    "List",
    "Optional",
    "NoneType",
    "Union",
    "Set",
    "Tuple",
    "Type",
    "TypedDict",
    "get_args",
    "get_origin",
    "is_literal",
    "is_typeddict",
)
