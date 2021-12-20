__version__ = "0.6.0"

from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    FrozenSet,
    Generic,
    List,
    Mapping,
    NewType,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from .func_check import func_check
from .main import Constraints, isinstancex, issubclassx
from .types import Listx, Tuplex
from .typing_compat import (
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
    "List",
    "Listx",
    "Literal",
    "Mapping",
    "NewType",
    "NoneType",
    "Optional",
    "Set",
    "Sequence",
    "Tuple",
    "Tuplex",
    "Type",
    "TypedDict",
    "TypeLike",
    "TypeVar",
    "Union",
    "get_args",
    "get_origin",
    "get_type_hints",
    "is_literal",
    "is_newtype",
    "is_typeddict",
)
