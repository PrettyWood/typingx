import collections.abc
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, cast

from .types import Listx, Tuplex
from .typing_compat import (
    Annotated,
    Literal,
    NoneType,
    OneOrManyTypes,
    TypedDict,
    TypeLike,
    get_args,
    get_origin,
    get_type_hints,
    is_literal,
    is_newtype,
    is_typeddict,
)

__all__ = ("Constraints", "isinstancex", "issubclassx")

TYPED_DICT_EXTRA_KEY = "__extra__"
NONE_TYPES = {None, NoneType, Literal[None]}
if sys.version_info < (3, 10):
    UNION_TYPES = {Union}
else:
    import types

    UNION_TYPES = {Union, types.UnionType}


@dataclass(frozen=True, repr=False)
class Constraints:
    # int, float, ...
    ge: Optional[float] = None
    gt: Optional[float] = None
    le: Optional[float] = None
    lt: Optional[float] = None
    multiple_of: Optional[float] = None

    # sequences-like (str, list, ...)
    min_length: Optional[int] = None
    max_length: Optional[int] = None

    # str
    regex: Optional[str] = None

    def is_valid(self, v: Any) -> bool:
        if self.ge is not None and v < self.ge:
            return False
        if self.gt is not None and v <= self.gt:
            return False
        if self.le is not None and v > self.le:
            return False
        if self.lt is not None and v >= self.lt:
            return False
        if self.multiple_of is not None and v % self.multiple_of != 0:
            return False

        if self.min_length is not None and len(v) < self.min_length:
            return False
        if self.max_length is not None and len(v) > self.max_length:
            return False
        if self.regex is not None:
            import re

            if re.search(self.regex, v) is None:
                return False

        return True

    def __repr__(self) -> str:
        defined_fields = (f"{k}={v}" for k, v in self.__dict__.items() if v is not None)
        return f"Constraints({', '.join(defined_fields)})"


def isinstancex(obj: Any, tp: OneOrManyTypes, *, constraints: Optional[Constraints] = None) -> bool:
    try:
        return _isinstancex(obj, tp, constraints)
    except (AttributeError, TypeError):
        return False


def issubclassx(obj: Any, tp: OneOrManyTypes) -> bool:
    try:
        return _issubclassx(obj, tp)
    except (AttributeError, TypeError):
        return False


def _isinstancex(obj: Any, tp: TypeLike, constraints: Optional[Constraints] = None) -> bool:
    """Extend `isinstance` with `typing` types"""
    origin = get_origin(tp)

    if origin is Annotated:
        tp, constraints = get_args(tp)
        origin = get_origin(tp)

    if tp is Any:
        return True

    while is_newtype(tp):
        tp = tp.__supertype__

    # https://www.python.org/dev/peps/pep-0484/#using-none
    if obj is None and tp in NONE_TYPES:
        return True

    # convert
    # - a plain dictionary to Dict or TypedDict
    # - a plain list to Listx[...]
    # - a plain tuple to Tuplex[...]
    if origin is None:
        # tp is of form `{'a': TypeLike, ...}`, `{...: TypeLike}`
        if isinstance(tp, dict):
            tp = {(TYPED_DICT_EXTRA_KEY if k is ... else k): v for k, v in tp.items()}
            td = TypedDict("_TypedDict", tp)  # type: ignore[call-overload]
            return isinstancex(obj, td, constraints=constraints)
        elif isinstance(tp, list):
            return isinstancex(obj, Listx[tuple(tp)], constraints=constraints)
        elif isinstance(tp, tuple):
            return isinstancex(obj, Tuplex[tuple(tp)], constraints=constraints)

    # e.g. Union[str, int] (or str|int in 3.10)
    if origin in UNION_TYPES:
        return any(isinstancex(obj, arg, constraints=constraints) for arg in get_args(tp))

    # e.g. Callable[[int], str]
    elif origin is collections.abc.Callable:
        if not callable(obj):
            return False

        expected_args_types, expected_return_type = get_args(tp) or (..., Any)

        if expected_args_types is ... and expected_return_type is Any:
            return True

        args_types, return_type = _get_function_type_hints(obj)

        if not issubclassx(return_type, expected_return_type):
            return False

        if expected_args_types is ...:
            return True

        return len(args_types) == len(expected_args_types) and all(
            issubclassx(a_tp, e_tp) for (a_tp, e_tp) in zip(args_types, expected_args_types)
        )

    # e.g. Dict[str, int]
    elif origin is dict:
        if tp is Dict:
            tp = Dict[Any, Any]
        return isinstancex(obj, dict, constraints=constraints) and _is_valid_mapping(
            obj, tp, constraints
        )

    # e.g. List[str] or Listx[int, str, ...]
    elif origin is list:
        # With recent python versions, `get_args` returns `(~T,)`, which we want to handle easily
        if tp is List:
            tp = List[Any]

        name = getattr(tp, "_name", None) or getattr(tp, "__name__", None)

        # We consider Listx[int] to check if a list as ONLY ONE item
        return isinstancex(obj, list, constraints=constraints) and _is_valid_sequence(
            obj, tp, is_list=name != "Listx"
        )

    # e.g. Set[str]
    elif origin is set:
        # With recent python versions, `get_args` returns `(~T,)`, which we want to handle easily
        if tp is Set:
            tp = Set[Any]

        return isinstancex(obj, set, constraints=constraints) and all(
            isinstancex(x, Union[get_args(tp)]) for x in obj
        )

    # e.g. Tuple[int, ...] or Tuplex[int, str, ...]
    elif origin is tuple:
        return isinstancex(obj, tuple, constraints=constraints) and _is_valid_sequence(
            obj, tp, is_list=False
        )

    # e.g. Type[int]
    elif origin is type:
        return issubclassx(obj, Union[get_args(tp)])

    # e.g. TypedDict('Movie', {'name': str, 'year': int})
    elif is_typeddict(tp):
        tp = cast(TypedDict, tp)
        return _is_valid_typeddict(obj, tp, constraints)

    # e.g. Literal['Pika']
    elif is_literal(tp):
        values_to_check = get_args(obj) if is_literal(obj) else (obj,)
        return all(v in get_args(tp) for v in values_to_check)

    # e.g. Collection[int]
    elif origin is collections.abc.Collection:
        return _is_valid_sequence(obj, tp, is_list=True) and (
            constraints is None or constraints.is_valid(obj)
        )

    # e.g. Sequence[int]
    elif origin is collections.abc.Sequence:
        return _is_valid_sequence(obj, tp, is_list=True) and (
            constraints is None or constraints.is_valid(obj)
        )

    # e.g. Maping[str, int]
    elif origin is collections.abc.Mapping:
        return _is_valid_mapping(obj, tp, constraints)

    # plain `Listx`
    elif tp is Listx:
        tp = list

    # plain `Tuplex`
    elif tp is Tuplex:
        tp = tuple

    return isinstance(obj, tp) and (constraints is None or constraints.is_valid(obj))


def _issubclassx(obj: Any, tp: TypeLike) -> bool:
    if tp is Any:
        return True

    if obj in NONE_TYPES and tp in NONE_TYPES:
        return True

    # convert
    # - a plain tuple to Tuplex[...]
    if isinstance(tp, tuple):
        return issubclassx(obj, Tuplex[tuple(tp)])

    obj_type = get_origin(obj)
    obj_args = get_args(obj)

    ref_type = get_origin(tp) or tp
    ref_args = get_args(tp) or (Any, ...)

    if obj_type in UNION_TYPES:
        return all(issubclassx(o, tp) for o in obj_args)

    if ref_type in UNION_TYPES:
        return any(issubclassx(obj, ref) for ref in ref_args)

    if obj_type is None:
        return issubclass(obj, ref_type)

    if len(ref_args) == 2 and ref_args[1] is ...:
        ref_args = (ref_args[0],) * len(obj_args)

    return len(obj_args) == len(ref_args) and all(
        issubclassx(o, r) for o, r in zip(obj_args, ref_args)
    )


#######################################
# get_args
#######################################
def _is_valid_mapping(obj: Any, tp: TypeLike, constraints: Optional[Constraints]) -> bool:
    keys_type, values_type = get_args(tp)
    return all(isinstancex(key, keys_type, constraints=constraints) for key in obj.keys()) and all(
        isinstancex(value, values_type, constraints=constraints) for value in obj.values()
    )


def _is_valid_sequence(obj: Any, tp: TypeLike, *, is_list: bool) -> bool:
    """
    Check that a sequence respects a type with args like [str], [str, int], [str, ...]
    but also args like [str, int, ...] or even [str, int, ..., bool, ..., float]
    """
    if len(obj) == 0:
        return True

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


def _is_valid_typeddict(obj: Any, tp: TypedDict, constraints: Optional[Constraints]) -> bool:
    # ensure it's a dict that contains all the required keys but extra values are allowed
    resolved_annotations = get_type_hints(tp)

    if TYPED_DICT_EXTRA_KEY in resolved_annotations:
        rest_type = resolved_annotations.pop(TYPED_DICT_EXTRA_KEY)
        required_keys = set(tp.__required_keys__) - {TYPED_DICT_EXTRA_KEY}
        if not set(obj).issuperset(required_keys):
            return False

        are_required_keys_valid = all(
            isinstancex(v, resolved_annotations[k], constraints=constraints)
            for k, v in obj.items()
            if k in required_keys
        )
        are_extra_keys_valid = all(
            isinstancex(v, rest_type, constraints=constraints)
            for k, v in obj.items()
            if k not in required_keys
        )
        return are_required_keys_valid and are_extra_keys_valid

    else:
        # ensure it's a dict that contains all the required keys without extra key
        if not (
            set(obj).issuperset(tp.__required_keys__) and set(obj).issubset(tp.__annotations__)
        ):
            return False

        return all(
            isinstancex(v, resolved_annotations[k], constraints=constraints) for k, v in obj.items()
        )


def _get_function_type_hints(obj: Callable[..., Any]) -> Tuple[List[TypeLike], TypeLike]:
    """Return a tuple <list of types of arguments>, <return type>"""
    import inspect
    import warnings

    sig = inspect.signature(obj)

    args_types: List[TypeLike] = []

    for name, parameter in sig.parameters.items():
        tp = parameter.annotation
        if tp is sig.empty:
            warnings.warn(
                f"No type hint specified for arg {name!r} of {obj.__name__!r}...fallback on `Any`",
                UserWarning,
            )
            tp = Any
        args_types.append(tp)

    return_type = sig.return_annotation
    if return_type is sig.empty:
        warnings.warn(
            f"No return type hint specified for {obj.__name__!r}...fallback on `Any`",
            UserWarning,
        )
        return_type = Any

    return args_types, return_type
