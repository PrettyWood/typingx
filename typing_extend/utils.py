from typing import Any, Callable, Tuple, Type, Union

__all__ = ("OneOrManyTypes", "TypeLike", "lenient_isinstance", "lenient_issubclass")


TypeLike = Union[Type[Any], Union[Any]]
OneOrManyTypes = Union[TypeLike, Tuple[TypeLike, ...]]


def _lenient(f: Callable[[Any, OneOrManyTypes], bool], obj: Any, tp: TypeLike) -> bool:
    try:
        return f(obj, tp)
    except TypeError:
        return False


def lenient_isinstance(obj: Any, tp: OneOrManyTypes) -> bool:
    """Forgiving version of `isinstance` as we may check "unofficial" types like `TypedDict`"""
    if isinstance(tp, tuple):
        return any(_lenient(isinstance, obj, t) for t in tp)
    else:
        return _lenient(isinstance, obj, tp)


def lenient_issubclass(obj: Any, tp: OneOrManyTypes) -> bool:
    """Forgiving version of `issubclass` as we may check "unofficial" types like `TypedDict`"""
    if isinstance(tp, tuple):
        return any(_lenient(issubclass, obj, t) for t in tp)
    else:
        return _lenient(issubclass, obj, tp)
