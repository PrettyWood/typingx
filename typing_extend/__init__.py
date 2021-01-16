# flake8: noqa
from typing import *

from .main import xisinstance
from .types import XTuple
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
    "XTuple",
    "get_args",
    "get_origin",
    "is_literal",
    "is_typeddict",
)
