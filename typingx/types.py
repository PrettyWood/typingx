import sys
import typing as T

from .typing_compat import OneOrManyTypes

__all__ = (
    "Listx",
    "Tuplex",
)


class ListxMeta(type):
    def __getitem__(self, params: OneOrManyTypes) -> T.Type["Listx"]:
        if not isinstance(params, tuple):
            params = (params,)

        if sys.version_info >= (3, 7):
            xlist_cls = T._GenericAlias(list, params, name="Listx")  # type: ignore[attr-defined]
        else:
            xlist_cls = type("Listx", (), {"__args__": params, "__origin__": list})

        return T.cast(T.Type["Listx"], xlist_cls)


class Listx(metaclass=ListxMeta):
    ...


class TuplexMeta(type):
    def __getitem__(self, params: OneOrManyTypes) -> T.Type["Tuplex"]:
        if not isinstance(params, tuple):
            params = (params,)

        if sys.version_info >= (3, 7):
            xtuple_cls = T._GenericAlias(tuple, params, name="Tuplex")  # type: ignore[attr-defined]
        else:
            xtuple_cls = type("Tuplex", (), {"__args__": params, "__origin__": tuple})

        return T.cast(T.Type["Tuplex"], xtuple_cls)


class Tuplex(metaclass=TuplexMeta):
    ...
