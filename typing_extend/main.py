from typing import Any, Union

from .typing_compat import get_args, get_origin

__all__ = ("extended_isinstance",)


def extended_isinstance(obj: Any, tp: Any) -> bool:
    """Extend `isinstance` with `typing` types"""
    if tp is Any:
        return True

    if isinstance(tp, tuple):
        return any(extended_isinstance(obj, sub_tp) for sub_tp in tp)

    origin = get_origin(tp)

    # e.g. List[str]
    if origin is list:
        return isinstance(obj, origin) and all(extended_isinstance(x, get_args(tp)) for x in obj)
    # e.g. Union[str, int]
    elif origin is Union:
        return extended_isinstance(obj, get_args(tp))
    return isinstance(obj, tp)
