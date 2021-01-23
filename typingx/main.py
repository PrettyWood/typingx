import collections.abc
import sys
from typing import Any, Callable, Dict, List, Set, Union, cast

from .types import Listx, Tuplex
from .typing_compat import (
    Literal,
    NoneType,
    OneOrManyTypes,
    TypedDict,
    TypeLike,
    get_args,
    get_origin,
    get_type_hints,
    is_generic,
    is_literal,
    is_newtype,
    is_typeddict,
)

__all__ = ("isinstancex", "issubclassx")

TYPED_DICT_EXTRA_KEY = "__extra__"
NONE_TYPES = (None, NoneType, Literal[None])
if sys.version_info < (3, 10):
    UNION_TYPES = (Union,)
else:
    import types

    UNION_TYPES = (Union, types.Union)


def _isinstancex(obj: Any, tp: TypeLike) -> bool:
    """Extend `isinstance` with `typing` types"""
    if tp is Any:
        return True

    while is_newtype(tp):
        tp = tp.__supertype__

    # https://www.python.org/dev/peps/pep-0484/#using-none
    if obj is None and tp in NONE_TYPES:
        return True

    origin = get_origin(tp)

    # convert
    # - a plain dictionary to Dict or TypedDict
    # - a plain list to Listx[...]
    if origin is None:
        if isinstance(tp, dict):
            tp = {(TYPED_DICT_EXTRA_KEY if k is ... else k): v for k, v in tp.items()}
            if len(tp) == 1 and not isinstancex(list(tp.keys())[0], str):
                # tp is of form `{TypeLike: TypeLike}`
                return _isinstancex(obj, Dict[list(tp.items())[0]])  # type: ignore
            else:
                # tp is of form `{'a': TypeLike, ...}`, `{...: TypeLike}`
                return _isinstancex(obj, TypedDict("_TypedDict", tp))  # type: ignore
        elif isinstance(tp, list):
            return _isinstancex(obj, Listx[tuple(tp)])

    # e.g. Union[str, int] (or str|int in 3.10)
    if origin in UNION_TYPES:
        return isinstancex(obj, get_args(tp))

    # e.g. Dict[str, int]
    elif origin is dict:
        if tp is Dict:
            tp = Dict[Any, Any]
        return isinstancex(obj, dict) and _is_valid_mapping(obj, tp)

    # e.g. List[str] or Listx[int, str, ...]
    elif origin is list:
        # With recent python versions, `get_args` returns `(~T,)`, which we want to handle easily
        if tp is List:
            tp = List[Any]

        return isinstancex(obj, list) and _is_valid_sequence(obj, tp, is_list=True)

    # e.g. Set[str]
    elif origin is set:
        # With recent python versions, `get_args` returns `(~T,)`, which we want to handle easily
        if tp is Set:
            tp = Set[Any]

        return isinstancex(obj, set) and all(isinstancex(x, get_args(tp)) for x in obj)

    # e.g. Tuple[int, ...] or Tuplex[int, str, ...]
    elif origin is tuple:
        return isinstance(obj, tuple) and _is_valid_sequence(obj, tp, is_list=False)

    # e.g. Type[int]
    elif origin is type:
        return issubclassx(obj, get_args(tp))

    # e.g. TypedDict('Movie', {'name': str, 'year': int})
    elif is_typeddict(tp):
        tp = cast(TypedDict, tp)
        return _is_valid_typeddict(obj, tp)

    # e.g. Literal['Pika']
    elif is_literal(tp):
        values_to_check = get_args(obj) if is_literal(obj) else (obj,)
        return all(v in get_args(tp) for v in values_to_check)

    # e.g. Sequence[int]
    elif origin is collections.abc.Sequence:
        return _is_valid_sequence(obj, tp, is_list=True)

    # e.g. Maping[str, int]
    elif origin is collections.abc.Mapping:
        return _is_valid_mapping(obj, tp)

    # plain `Listx`
    elif tp is Listx:
        tp = list

    # plain `Tuplex`
    elif tp is Tuplex:
        tp = tuple

    return isinstance(obj, tp)


def _issubclassx(obj: Any, tp: TypeLike) -> bool:
    if obj is tp:
        return True

    if is_generic(obj) and is_generic(tp):
        obj_mother_class = get_origin(obj.__orig_bases__[0])
        obj_mother_args = get_args(obj.__orig_bases__[0])

        return issubclassx(obj_mother_class, get_origin(tp)) and all(
            issubclassx(arg, get_args(tp)) for arg in obj_mother_args
        )

    return issubclass(obj, tp)


def _safe_multi(f: Callable[[Any, TypeLike], bool]) -> Callable[[Any, OneOrManyTypes], bool]:
    def safe_f_multi(obj: Any, tp: OneOrManyTypes) -> bool:
        try:
            if isinstance(tp, tuple):
                return any(f(obj, sub_tp) for sub_tp in tp)
            else:
                return f(obj, tp)
        except (AttributeError, TypeError):
            return False

    return safe_f_multi


isinstancex = _safe_multi(_isinstancex)
issubclassx = _safe_multi(_issubclassx)


#######################################
# get_args
#######################################
def _is_valid_mapping(obj: Any, tp: TypeLike) -> bool:
    keys_type, values_type = get_args(tp)
    return all(isinstancex(key, keys_type) for key in obj.keys()) and all(
        isinstancex(value, values_type) for value in obj.values()
    )


def _is_valid_sequence(obj: Any, tp: TypeLike, *, is_list: bool) -> bool:
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


def _is_valid_typeddict(obj: Any, tp: TypedDict) -> bool:
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
