import sys

__all__ = ("get_args", "get_origin", "is_typeddict", "TypedDict")

# Python 3.10+
if sys.version_info >= (3, 10):
    from typing import TypedDict, get_args, get_origin, is_typeddict

# Python 3.9+
elif sys.version_info >= (3, 9):
    from typing import Any, Type, get_args, get_origin

    from typing_extensions import TypedDict

    from .utils import lenient_issubclass

    def is_typeddict(tp: Type[Any]) -> bool:
        return lenient_issubclass(tp, dict) and getattr(tp, "__annotations__", None)


# Python 3.8+
elif sys.version_info >= (3, 8):
    from typing import Any, Type, get_args, get_origin

    from typing_extensions import TypedDict

    from .utils import lenient_issubclass

    def is_typeddict(tp: Type[Any]) -> bool:
        return lenient_issubclass(tp, dict) and getattr(tp, "__annotations__", None)


# Python 3.7
elif sys.version_info >= (3, 7):
    from typing import Any, Optional, Tuple, Type

    from typing_extensions import TypedDict

    from .utils import lenient_issubclass

    def get_args(tp: Type[Any]) -> Tuple[Any, ...]:
        return getattr(tp, "__args__", ())

    def get_origin(tp: Type[Any]) -> Optional[Type[Any]]:
        return getattr(tp, "__origin__", None)

    def is_typeddict(tp: Type[Any]) -> bool:
        return lenient_issubclass(tp, dict) and getattr(tp, "__annotations__", None)


# Python 3.6
else:
    from typing import Any, Dict, List, Optional, Set, Tuple, Type

    from typing_extensions import TypedDict

    from .utils import lenient_issubclass

    TYPING_TO_BUILTIN_MAP = {
        Dict: dict,
        List: list,
        Set: set,
        Tuple: tuple,
        Type: type,
    }

    def get_args(tp: Type[Any]) -> Tuple[Any, ...]:
        return getattr(tp, "__args__", ())

    def get_origin(tp: Type[Any]) -> Optional[Type[Any]]:
        origin = getattr(tp, "__origin__", None)
        return TYPING_TO_BUILTIN_MAP.get(origin, origin)

    def is_typeddict(tp: Type[Any]) -> bool:
        return lenient_issubclass(tp, dict) and getattr(tp, "__annotations__", None)
