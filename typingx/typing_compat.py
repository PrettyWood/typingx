"""
Module that handles differences between supported versions of Python
for some methods / classes of the `typing` module
"""
import sys
import typing as T

__all__ = (
    "Literal",
    "NoneType",
    "OneOrManyTypes",
    "TypedDict",
    "TypeLike",
    "get_args",
    "get_origin",
    "get_type_hints",
    "is_generic",
    "is_literal",
    "is_newtype",
    "is_typeddict",
)


NoneType = type(None)
TypeLike = T.Union[T.Type[T.Any], T.Union[T.Any]]
OneOrManyTypes = T.Union[TypeLike, T.Tuple[TypeLike, ...]]


#######################################
# get_args
#######################################
if sys.version_info >= (3, 8):
    T_get_args = T.get_args

else:

    def T_get_args(tp: TypeLike) -> T.Tuple[T.Any, ...]:
        return getattr(tp, "__args__", ())


def get_args(tp: TypeLike) -> T.Tuple[T.Any, ...]:
    if sys.version_info >= (3, 10):
        return T_get_args(tp)
    else:
        # Handle nested literals (see https://www.python.org/dev/peps/pep-0586)
        if is_literal(tp):
            return _get_all_literal_values(tp)

        return T_get_args(tp) or ()


#######################################
# get_origin
#######################################
if sys.version_info >= (3, 8):
    T_get_origin = T.get_origin

elif sys.version_info[:2] == (3, 7):

    def T_get_origin(tp: TypeLike) -> T.Optional[TypeLike]:
        return getattr(tp, "__origin__", None)


else:
    import collections.abc

    def T_get_origin(tp: TypeLike) -> T.Optional[TypeLike]:
        # In python 3.6, the origin of `List[str]` for example
        # is `List` and not `list`. We hence need an explicit mapping...
        typing_to_builtin_map = {
            T.Dict: dict,
            T.List: list,
            T.Mapping: collections.abc.Mapping,
            T.Set: set,
            T.Sequence: collections.abc.Sequence,
            T.Tuple: tuple,
            T.Type: type,
        }

        origin = getattr(tp, "__origin__", None)
        # change `List[Tuple[~T, ~T]]` into `List`
        origin = getattr(origin, "_gorg", origin)
        return typing_to_builtin_map.get(origin, origin)


def get_origin(tp: TypeLike) -> T.Optional[TypeLike]:
    # Python 3.8+
    if sys.version_info >= (3, 8):
        return T_get_origin(tp)

    # Python 3.7
    elif sys.version_info >= (3, 7):
        if tp is T.Generic:
            return T.Generic
        return T_get_origin(tp)

    # Python 3.6
    else:
        if is_literal(tp):
            return Literal

        elif tp is T.Generic:
            return T.Generic

        return T_get_origin(tp)


#######################################
# get_type_hints
#######################################
def get_type_hints(
    obj: T.Callable[..., T.Any],
    globalns: T.Optional[T.Dict[str, T.Any]] = None,
    localns: T.Optional[T.Dict[str, T.Any]] = None,
    include_extras: bool = False,
) -> T.Dict[str, T.Any]:
    # Python 3.9+
    if sys.version_info >= (3, 9):
        return T.get_type_hints(
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
        return T.get_type_hints(obj, globalns=globalns, localns=localns)


#######################################
# TypedDict
#######################################
if T.TYPE_CHECKING:

    class TypedDict(T.Dict[str, T.Any]):
        __annotations__: T.Dict[str, T.Type[T.Any]]
        __total__: bool
        __required_keys__: T.FrozenSet[str]
        __optional_keys__: T.FrozenSet[str]

        def __call__(self, *args: T.Any, **kwargs: T.Any) -> T.Any:
            ...


elif sys.version_info >= (3, 9):
    TypedDict = T.TypedDict

else:
    # Even though `TypedDict` is already in python 3.8,
    # the class doesn't have `__required_keys__` and `__optional_keys__`,
    # which prevents a perfect support
    from typing_extensions import TypedDict


def is_typeddict(tp: TypeLike) -> bool:
    # Python 3.10+
    if sys.version_info >= (3, 10):
        return T.is_typeddict(tp)

    # Python 3.6 to Python 3.9
    else:
        return isinstance(tp, type) and issubclass(tp, dict) and hasattr(tp, "__annotations__")


#######################################
# Literal
#######################################
if sys.version_info >= (3, 8):
    Literal = T.Literal
else:
    from typing_extensions import Literal


def is_literal(tp: TypeLike) -> bool:
    """
    Check if a type is a `Literal`
    """
    if sys.version_info >= (3, 7):
        return T_get_origin(tp) is Literal
    else:
        return hasattr(tp, "__values__") and tp == Literal[tp.__values__]


def _get_literal_values(tp: TypeLike) -> T.Tuple[T.Any, ...]:
    if sys.version_info >= (3, 7):
        return T_get_args(tp)
    else:
        return getattr(tp, "__values__", ())


def _get_all_literal_values(tp: TypeLike) -> T.Tuple[T.Any, ...]:
    if not is_literal(tp):
        return (tp,)

    literal_values = _get_literal_values(tp)
    return tuple(x for v in literal_values for x in _get_all_literal_values(v))


#######################################
# NewType
#######################################
TestType = T.NewType("TestType", str)


def is_newtype(tp: TypeLike) -> bool:
    """
    Check if a type is a `NewType`
    """
    return tp.__class__ is TestType.__class__


#######################################
# Generic
#######################################
def is_generic(tp: TypeLike) -> bool:
    return hasattr(tp, "__parameters__")
