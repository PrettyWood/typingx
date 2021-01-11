import sys

__all__ = ("get_args", "get_origin")

# Python 3.8+
if sys.version_info >= (3, 8):
    from typing import get_args, get_origin

# Python 3.7
elif sys.version_info >= (3, 7):
    from typing import Any, Optional, Tuple, Type

    def get_args(tp: Type[Any]) -> Tuple[Any, ...]:
        return getattr(tp, "__args__", ())

    def get_origin(tp: Type[Any]) -> Optional[Type[Any]]:
        return getattr(tp, "__origin__", None)


# Python 3.6
else:
    from typing import Any, Dict, List, Optional, Set, Tuple, Type

    TYPING_TO_BUILTIN_MAP = {
        Dict: dict,
        List: list,
        Set: set,
        Tuple: tuple,
    }

    def get_args(tp: Type[Any]) -> Tuple[Any, ...]:
        return getattr(tp, "__args__", ())

    def get_origin(tp: Type[Any]) -> Optional[Type[Any]]:
        origin = getattr(tp, "__origin__", None)
        return TYPING_TO_BUILTIN_MAP.get(origin, origin)
