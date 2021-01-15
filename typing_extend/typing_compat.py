"""
Module that handles differences between supported versions of Python
for some methods / classes of the `typing` module
"""
import sys
from typing import Any, Callable, Dict, Optional, Tuple, cast

from .utils import TypeLike

__all__ = ("NoneType", "TypedDict", "get_args", "get_origin", "get_type_hints", "is_typeddict")


NoneType = type(None)

if sys.version_info < (3, 9):
    # Even though `TypedDict` is already in python 3.8,
    # the class doesn't have `__required_keys__` and `__optional_keys__`,
    # which prevents a perfect support
    from typing_extensions import TypedDict
else:
    from typing import TypedDict


def get_args(tp: TypeLike) -> Tuple[Any, ...]:
    # Python 3.8+
    if sys.version_info >= (3, 8):
        from typing import get_args

        return get_args(tp)

    # Python 3.6 and 3.7
    else:
        return cast(Tuple[Any, ...], getattr(tp, "__args__", ()))


def get_origin(tp: TypeLike) -> Optional[TypeLike]:
    # Python 3.8+
    if sys.version_info >= (3, 8):
        from typing import get_origin

        return get_origin(tp)

    # Python 3.7
    elif sys.version_info[:2] == (3, 7):
        return getattr(tp, "__origin__", None)

    # Python 3.6
    else:
        assert sys.version_info[:2] == (3, 6)

        from typing import Dict, List, Set, Tuple, Type

        # In python 3.6, the origin of `List[str]` for example
        # is `List` and not `list`. We hence need an explicit mapping...
        typing_to_builtin_map = {
            Dict: dict,
            List: list,
            Set: set,
            Tuple: tuple,
            Type: type,
        }

        origin = getattr(tp, "__origin__", None)
        return typing_to_builtin_map.get(origin, origin)


def get_type_hints(
    obj: Callable[..., Any],
    globalns: Optional[Dict[str, Any]] = None,
    localns: Optional[Dict[str, Any]] = None,
    include_extras: bool = False,
) -> Dict[str, Any]:
    # Python 3.9+
    if sys.version_info >= (3, 9):
        from typing import get_type_hints

        return get_type_hints(
            obj, globalns=globalns, localns=localns, include_extras=include_extras
        )

    # Python 3.7 and 3.8
    elif sys.version_info >= (3, 7):
        from typing_extensions import get_type_hints

        return get_type_hints(
            obj, globalns=globalns, localns=localns, include_extras=include_extras
        )

    # Python 3.6
    else:
        assert sys.version_info[:2] == (3, 6)

        from typing import get_type_hints

        return get_type_hints(obj, globalns=globalns, localns=localns)


def is_typeddict(tp: TypeLike) -> bool:
    # Python 3.10+
    if sys.version_info >= (3, 10):
        from typing import is_typeddict

        return is_typeddict(tp)

    # Python 3.6 to Python 3.9
    else:
        from .utils import lenient_issubclass

        return lenient_issubclass(tp, dict) and hasattr(tp, "__annotations__")
