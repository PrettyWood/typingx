# flake8: noqa
from typing import *

from .func_check import func_check
from .main import Constraints, isinstancex, issubclassx
from .types import Listx, Tuplex
from .typing_compat import (  # type: ignore[misc]
    Annotated,
    Literal,
    NoneType,
    TypedDict,
    TypeLike,
    get_args,
    get_origin,
    get_type_hints,
    is_literal,
    is_newtype,
    is_typeddict,
)

__all__ = (
    # main
    "Constraints",
    "isinstancex",
    "issubclassx",
    # func_check
    "func_check",
    # typing, typing_extensions or own backport
    "Annotated",
    "Any",
    "Callable",
    "Collection",
    "Dict",
    "FrozenSet",
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
    "TypeLike",
    "TypeVar",
    "TypedDict",
    "get_args",
    "get_origin",
    "get_type_hints",
    "is_literal",
    "is_newtype",
    "is_typeddict",
)
