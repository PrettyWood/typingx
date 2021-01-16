import sys
import typing as T

from .utils import OneOrManyTypes

__all__ = ("XTuple",)


class XTupleMeta(type):
    def __getitem__(self, params: OneOrManyTypes) -> T.Type["XTuple"]:
        if not isinstance(params, tuple):
            params = (params,)

        if sys.version_info >= (3, 7):
            xtuple_cls = T._GenericAlias(tuple, params, name="XTuple")  # type: ignore[attr-defined]
        else:
            xtuple_cls = type("XTuple", (), {"__args__": params, "__origin__": tuple})

        return T.cast(T.Type["XTuple"], xtuple_cls)


class XTuple(metaclass=XTupleMeta):
    ...
