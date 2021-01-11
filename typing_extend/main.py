from typing import Any, List, Union

from .typing_compat import get_args, get_origin

__all__ = ("extended_isinstance",)


def extended_isinstance(obj: Any, tp: Any) -> bool:
    """Extend `isinstance` with `typing` types"""
    if tp is Any:
        return True

    if isinstance(tp, tuple):
        return any(extended_isinstance(obj, sub_tp) for sub_tp in tp)

    origin = get_origin(tp)

    # e.g. Union[str, int]
    if origin is Union:
        return extended_isinstance(obj, get_args(tp))

    if origin in (list, tuple) and not isinstance(obj, origin):
        return False

    # e.g. List[str]
    if origin is list:
        if tp is List:
            tp = List[Any]
        return all(extended_isinstance(x, get_args(tp)) for x in obj)

    # e.g. Tuple[int, ...]
    elif origin is tuple:
        expected_types = get_args(tp) or (Any, ...)

        if len(expected_types) == 2 and expected_types[1] is ...:
            return all(extended_isinstance(item, expected_types[0]) for item in obj)
        else:
            return len(expected_types) == len(obj) and all(
                extended_isinstance(item, item_tp) for item, item_tp in zip(obj, expected_types)
            )

    return isinstance(obj, tp)
