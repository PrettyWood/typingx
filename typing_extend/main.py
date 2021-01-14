from typing import Any, Dict, List, Set, Union

from .typing_compat import get_args, get_origin, get_type_hints, is_typeddict
from .utils import lenient_isinstance

__all__ = ("xisinstance",)


def xisinstance(obj: Any, tp: Any) -> bool:
    """Extend `isinstance` with `typing` types"""
    if tp is Any:
        return True

    if lenient_isinstance(tp, tuple):
        return any(xisinstance(obj, sub_tp) for sub_tp in tp)

    origin = get_origin(tp)

    # e.g. Union[str, int]
    if origin is Union:
        return xisinstance(obj, get_args(tp))

    # e.g. Dict[str, int]
    if origin is dict:
        if tp is Dict:
            tp = Dict[Any, Any]
        keys_type, values_type = get_args(tp)
        return all(xisinstance(key, keys_type) for key in obj.keys()) and all(
            xisinstance(value, values_type) for value in obj.values()
        )

    # e.g. List[str] or Set[str]
    elif origin in {list, set}:
        # With recent python versions, `get_args` returns `(~T,)`, which we want to handle easily
        if tp is List:
            tp = List[Any]
        elif tp is Set:
            tp = Set[Any]

        return all(xisinstance(x, get_args(tp)) for x in obj)

    # e.g. Tuple[int, ...]
    elif origin is tuple:
        expected_types = get_args(tp) or (Any, ...)

        if len(expected_types) == 2 and expected_types[1] is ...:
            return all(xisinstance(item, expected_types[0]) for item in obj)
        else:
            return len(expected_types) == len(obj) and all(
                xisinstance(item, item_tp) for item, item_tp in zip(obj, expected_types)
            )

    # e.g. Type[int]
    elif origin is type:
        return issubclass(obj, get_args(tp))

    # e.g. TypedDict('Movie', {'name': str, 'year': int})
    elif is_typeddict(tp):
        # ensure it's a dict that contains all the required keys
        if not (
            isinstance(obj, dict)
            and set(obj).issuperset(tp.__required_keys__)
            and set(obj).issubset(tp.__annotations__)
        ):
            return False

        resolved_annotations = get_type_hints(tp)
        return all(xisinstance(v, resolved_annotations[k]) for k, v in obj.items())

    return lenient_isinstance(obj, tp)
