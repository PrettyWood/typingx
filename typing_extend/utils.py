from typing import Any, Tuple, Type, Union

__all__ = ("lenient_isinstance", "lenient_issubclass")


def lenient_isinstance(obj: Any, tp: Union[Type[Any], Tuple[Type[Any], ...]]) -> bool:
    """Forgiving version of `isinstance` as we may check "unofficial" types like `TypedDict`"""
    try:
        return isinstance(obj, tp)
    except TypeError:
        return False


def lenient_issubclass(obj: Any, tp: Union[Type[Any], Tuple[Type[Any], ...]]) -> bool:
    """Forgiving version of `issubclass` as we may check "unofficial" types like `TypedDict`"""
    return lenient_isinstance(obj, type) and issubclass(obj, tp)
