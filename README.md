# typingx
[![Tests](https://github.com/PrettyWood/typingx/workflows/Tests/badge.svg)](https://github.com/PrettyWood/typingx/actions)
[![codecov](https://codecov.io/gh/PrettyWood/typingx/branch/main/graph/badge.svg)](https://codecov.io/gh/PrettyWood/typingx)
[![pypi](https://img.shields.io/pypi/v/typingx.svg)](https://pypi.python.org/pypi/typingx)
[![versions](https://img.shields.io/pypi/pyversions/typingx.svg)](https://github.com/PrettyWood/typingx)
[![license](https://img.shields.io/github/license/PrettyWood/typingx.svg)](https://github.com/PrettyWood/typingx/blob/master/LICENSE)

`typing` is great but it changed a lot since 3.6 and it's not over!

This library purpose is to have a consistent behaviour for all those versions to mimic the most recent one
and go even further with `typing` (and `typing_extensions`).

It provides:
- `get_args` and `get_origin` for python `3.6` to `3.9` that mimic `3.10` behaviour
- `is_literal`, `is_typeddict` helpers
- most `typing` types but with homogeneous behaviour
  (e.g. with `3.8`, `typing.TypedDict` won't store information to distinguish optional and required keys. This lib will hence choose `typing_extensions` version)

but also:
- `isinstancex`: like `isinstance` but with `typing(x)` types
- extra types:
  * `Listx` and `Tuplex`: more sophisticated versions of `List` and `Tuple` to add `...` anywhere in the parameters
- extanded types:
  * `TypedDict` has a `__extra__` field (value can be changed) to allow type checking on optional fields

## Installation

``` bash
    pip install typingx
```

## Usage
```python
from collections import ChainMap, Counter

from typingx import (
    Any,
    Dict,
    List,
    Listx,
    Literal,
    Mapping,
    Sequence,
    Set,
    Tuple,
    Tuplex,
    Type,
    TypedDict,
    Union,
    isinstancex,
)

# Dict
assert isinstancex({"a": 1, "b": 2}, Dict[str, int]) is True
assert isinstancex({"a": 1, "b": 2}, Dict[str, str]) is False
assert isinstancex({"a": 1, "b": 2}, Dict[int, str]) is False
assert isinstancex({"a": 1, "b": 2}, Dict[str, Any]) is True

# List
assert isinstancex([1, 2, 3], List[int]) is True
assert isinstancex([1, 2, "q"], List[int]) is False
assert isinstancex([1, 2, "q"], List[Union[str, int]]) is True

# Listx
assert isinstancex([1, 2, 3, 4], Listx[int]) is True
assert isinstancex([1, 2, "q"], Listx[int, ..., str]) is True
assert isinstancex([1, 2, "q", "w", "e"], Listx[int, ..., str]) is False
assert isinstancex([1, 2, "q", "w", "e"], Listx[int, ..., str, ...]) is True
assert isinstancex([1, 2, "q", "w", b"xyz", "e"], Listx[int, ..., str, ...]) is False
assert isinstancex([1, 2, "q", "w", b"xyz", "e"], Listx[int, ..., Union[str, bytes], ...]) is True

# Literal
assert isinstancex("a", Literal["a"]) is True
assert isinstancex(Literal["a"], Literal["a"]) is True
assert isinstancex("b", Literal["a"]) is False
assert isinstancex("b", Literal["a", Literal[Literal["b"]]]) is True
assert isinstancex(Literal["a", "b"], Literal["b", "a", "c"]) is True

# Mapping
assert isinstancex(Counter({"red": 4, "blue": 2}), Mapping[str, int]) is True
assert isinstancex(ChainMap({"art": "van gogh"}, {"music": "bach"}), Mapping[str, str]) is True

# Sequence
assert isinstancex("abc", Sequence[Any]) is True
assert isinstancex("abc", Sequence[int]) is False
assert isinstancex((1, 3, 5), Sequence[int]) is True

# Set
assert isinstancex({"a", "b"}, Set[str]) is True
assert isinstancex({"a", "b"}, Set[int]) is False

# Tuple
assert isinstancex((1, 2), Tuple[int, ...]) is True
assert isinstancex((1, 2), Tuple[int, int]) is True
assert isinstancex((1, 2), Tuple[int, int, int]) is False

# Tuplex
assert isinstancex((3, "a", "b"), Tuplex[int, str, ...]) is True
assert isinstancex((3, "a", "b", "c"), Tuplex[int, str, ...]) is True
assert isinstancex((3, "a", "b", "c"), Tuplex[int, str, ..., bool]) is False
assert isinstancex((3, "a", "b", "c", True), Tuplex[int, str, ..., bool]) is True
assert isinstancex((3, "a", "b", "c", 3), Tuplex[int, str, ..., bool]) is False
assert isinstancex((3, "a", "b", "c", True, False), Tuplex[int, str, ..., bool, ...]) is True

# Type
class User: ...
class BaseUser(User): ...

assert isinstancex(BaseUser, Type[BaseUser]) is True
assert isinstancex(BaseUser, Type[User]) is True
assert isinstancex(User, Type[User]) is True
assert isinstancex(User, Type[BaseUser]) is False

# TypedDict
FullMovie = TypedDict("FullMovie", {"name": str, "year": int})

class PartialMovie(TypedDict, total=False):
    name: str
    year: int

class ExtraMovie(TypedDict):
    name: str
    year: int
    __extra__: str

assert isinstancex({"name": "The Matrix", "year": 1999}, FullMovie) is True
assert isinstancex({"name": "The Matrix", "year": "1999"}, FullMovie) is False
assert isinstancex({"name": "The Matrix"}, FullMovie) is False
assert isinstancex({"name": "The Matrix", "year": 1999, "extra": "qwe"}, FullMovie) is False

assert isinstancex({"name": "The Matrix", "year": 1999}, PartialMovie) is True
assert isinstancex({"name": "The Matrix"}, PartialMovie) is True
assert isinstancex({"name": "The Matrix", "year": 1999, "extra": "qwe"}, PartialMovie) is False

assert isinstancex({"name": "The Matrix", "year": 1999}, ExtraMovie) is True
assert isinstancex({"name": "The Matrix", "year": 1999, "q": "w", "e": "r"}, ExtraMovie) is True
assert isinstancex({"name": "The Matrix", "year": 1999, "q": "w", "e": 1}, ExtraMovie) is False
```
