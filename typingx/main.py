from typing import Any, Dict, List, Sequence, Set, Union

from .types import Listx, Tuplex
from .typing_compat import TypedDict, get_args, get_origin, get_type_hints, is_literal, is_typeddict
from .utils import TypeLike, lenient_isinstance

__all__ = ("isinstancex",)

TYPED_DICT_EXTRA_KEY = "__extra__"


def isinstancex(obj: Any, tp: Any) -> bool:
    """Extend `isinstance` with `typing` types"""
    if tp is Any:
        return True

    if lenient_isinstance(tp, tuple):
        return any(isinstancex(obj, sub_tp) for sub_tp in tp)

    origin = get_origin(tp)

    # e.g. Union[str, int]
    if origin is Union:
        return isinstancex(obj, get_args(tp))

    # e.g. Dict[str, int]
    if origin is dict:
        if tp is Dict:
            tp = Dict[Any, Any]
        keys_type, values_type = get_args(tp)
        return all(isinstancex(key, keys_type) for key in obj.keys()) and all(
            isinstancex(value, values_type) for value in obj.values()
        )

    # e.g. List[str] or Listx[int, str, ...]
    elif origin is list:
        # With recent python versions, `get_args` returns `(~T,)`, which we want to handle easily
        if tp is List:
            tp = List[Any]

        return _is_valid_sequence(obj, tp, is_list=True)

    # e.g. Set[str]
    elif origin is set:
        # With recent python versions, `get_args` returns `(~T,)`, which we want to handle easily
        if tp is Set:
            tp = Set[Any]

        return all(isinstancex(x, get_args(tp)) for x in obj)

    # e.g. Tuple[int, ...] or Tuplex[int, str, ...]
    elif origin is tuple:
        return _is_valid_sequence(obj, tp, is_list=False)

    # e.g. Type[int]
    elif origin is type:
        return issubclass(obj, get_args(tp))

    # e.g. TypedDict('Movie', {'name': str, 'year': int})
    elif is_typeddict(tp):
        if not (isinstance(obj, dict) and all(isinstance(k, str) for k in obj)):
            return False

        return _is_valid_typeddict(obj, tp)

    # e.g. Literal['Pika']
    elif is_literal(tp):
        values_to_check = get_args(obj) if is_literal(obj) else (obj,)
        return all(v in get_args(tp) for v in values_to_check)

    # plain `Listx`
    elif tp is Listx:
        tp = list

    # plain `Tuplex`
    elif tp is Tuplex:
        tp = tuple

    return lenient_isinstance(obj, tp)


def _is_valid_sequence(obj: Sequence[Any], tp: TypeLike, *, is_list: bool) -> bool:
    """
    Check that a sequence respects a type with args like [str], [str, int], [str, ...]
    but also args like [str, int, ...] or even [str, int, ..., bool, ..., float]
    """
    expected_types = get_args(tp) or (Any, ...)

    # We consider expected types of `List[int]` as [int, ...]
    if is_list and len(expected_types) == 1:
        expected_types += (...,)

    current_index = 0
    for item in obj:

        try:
            if expected_types[current_index] is ...:
                # Check first with previous type...
                if isinstancex(item, expected_types[current_index - 1]):
                    continue

                # ...else check with a new type
                if isinstancex(item, expected_types[current_index + 1]):
                    current_index += 2
                    continue
            else:
                if isinstancex(item, expected_types[current_index]):
                    current_index += 1
                    continue
        except IndexError:
            return False

        return False
    else:
        # Check remaining types
        return expected_types[current_index:] in ((), (...,))


def _is_valid_typeddict(obj: Dict[str, Any], tp: TypedDict) -> bool:
    # ensure it's a dict that contains all the required keys but extra values are allowed
    resolved_annotations = get_type_hints(tp)

    if TYPED_DICT_EXTRA_KEY in resolved_annotations:
        rest_type = resolved_annotations.pop(TYPED_DICT_EXTRA_KEY)
        required_keys = set(tp.__required_keys__) - {TYPED_DICT_EXTRA_KEY}
        if not set(obj).issuperset(required_keys):
            return False

        are_required_keys_valid = all(
            isinstancex(v, resolved_annotations[k]) for k, v in obj.items() if k in required_keys
        )
        are_extra_keys_valid = all(
            isinstancex(v, rest_type) for k, v in obj.items() if k not in required_keys
        )
        return are_required_keys_valid and are_extra_keys_valid

    else:
        # ensure it's a dict that contains all the required keys without extra key
        if not (
            set(obj).issuperset(tp.__required_keys__) and set(obj).issubset(tp.__annotations__)
        ):
            return False

        return all(isinstancex(v, resolved_annotations[k]) for k, v in obj.items())
