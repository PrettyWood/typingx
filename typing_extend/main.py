from typing import Any, Dict, List, Set, Union

from .types import XTuple
from .typing_compat import get_args, get_origin, get_type_hints, is_literal, is_typeddict
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

    # e.g. Tuple[int, ...] or XTuple[int, str, ...]
    elif origin is tuple:
        expected_types = get_args(tp) or (Any, ...)

        current_index = 0
        for item in obj:
            if expected_types[current_index] is ...:
                # Check first with previous type...
                if xisinstance(item, expected_types[current_index - 1]):
                    continue

                # ...else check with a new type
                if xisinstance(item, expected_types[current_index + 1]):
                    current_index += 2
                    continue
            else:
                if xisinstance(item, expected_types[current_index]):
                    current_index += 1
                    continue

            return False
        else:
            # Check remaining types
            return expected_types[current_index:] in ((), (...,))

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

    # e.g. Literal['Pika']
    elif is_literal(tp):
        values_to_check = get_args(obj) if is_literal(obj) else (obj,)
        return all(v in get_args(tp) for v in values_to_check)

    # plain `XTuple`
    elif tp is XTuple:
        tp = tuple

    return lenient_isinstance(obj, tp)
