# typing-extend
[![Tests](https://github.com/PrettyWood/typing-extend/workflows/Tests/badge.svg)](https://github.com/PrettyWood/typing-extend/actions)
[![codecov](https://codecov.io/gh/PrettyWood/typing-extend/branch/main/graph/badge.svg)](https://codecov.io/gh/PrettyWood/typing-extend)
[![pypi](https://img.shields.io/pypi/v/typing-extend.svg)](https://pypi.python.org/pypi/typing-extend)
[![versions](https://img.shields.io/pypi/pyversions/typing-extend.svg)](https://github.com/PrettyWood/typing-extend)
[![license](https://img.shields.io/github/license/PrettyWood/typing-extend.svg)](https://github.com/PrettyWood/typing-extend/blob/master/LICENSE)

`typing` is great but it changed a lot since 3.6 and it's not over!

This library purpose is to have a consistent behaviour for all those versions to mimic the most recent one
and go even further with `typing` (and `typing_extensions`).

It hences provides:
- `get_args` and `get_origin` for python `3.6` to `3.9` that mimic `3.10` behaviour
- `is_literal`, `is_typeddict` helpers
- most `typing` types but with homogeneous behaviour (e.g. with `3.8`, `typing.TypedDict` won't store information to distinguish optional and required keys)

but also:
- `xisinstance`: like `isinstance` but with `typing` types
- extra types:
  * `XList` and `XTuple`: more sophisticated versions of `List` and `Tuple` to add `...` anywhere in the parameters

## Installation

``` bash
    pip install typing_extend
```

## Usage
```python
from typing_extend import (
    Any,
    Dict,
    List,
    Literal,
    Set,
    Tuple,
    Type,
    TypedDict,
    Union,
    XList,
    XTuple,
    xisinstance,
)

# Dict
assert xisinstance({"a": 1, "b": 2}, Dict[str, int]) is True
assert xisinstance({"a": 1, "b": 2}, Dict[str, str]) is False
assert xisinstance({"a": 1, "b": 2}, Dict[int, str]) is False
assert xisinstance({"a": 1, "b": 2}, Dict[str, Any]) is True

# List
assert xisinstance([1, 2, 3], List[int]) is True
assert xisinstance([1, 2, "q"], List[int]) is False
assert xisinstance([1, 2, "q"], List[Union[str, int]]) is True

# XList
assert xisinstance([1, 2, 3, 4], XList[int]) is True
assert xisinstance([1, 2, "q"], XList[int, ..., str]) is True
assert xisinstance([1, 2, "q", "w", "e"], XList[int, ..., str]) is False
assert xisinstance([1, 2, "q", "w", "e"], XList[int, ..., str, ...]) is True
assert xisinstance([1, 2, "q", "w", b"xyz", "e"], XList[int, ..., str, ...]) is False
assert xisinstance([1, 2, "q", "w", b"xyz", "e"], XList[int, ..., Union[str, bytes], ...]) is True

# Literal
assert xisinstance("a", Literal["a"]) is True
assert xisinstance(Literal["a"], Literal["a"]) is True
assert xisinstance("b", Literal["a"]) is False
assert xisinstance("b", Literal["a", Literal[Literal["b"]]]) is True
assert xisinstance(Literal["a", "b"], Literal["b", "a", "c"]) is True

# Set
assert xisinstance({"a", "b"}, Set[str]) is True
assert xisinstance({"a", "b"}, Set[int]) is False

# Tuple
assert xisinstance((1, 2), Tuple[int, ...]) is True
assert xisinstance((1, 2), Tuple[int, int]) is True
assert xisinstance((1, 2), Tuple[int, int, int]) is False

# XTuple
assert xisinstance((3, "a", "b"), XTuple[int, str, ...]) is True
assert xisinstance((3, "a", "b", "c"), XTuple[int, str, ...]) is True
assert xisinstance((3, "a", "b", "c"), XTuple[int, str, ..., bool]) is False
assert xisinstance((3, "a", "b", "c", True), XTuple[int, str, ..., bool]) is True
assert xisinstance((3, "a", "b", "c", 3), XTuple[int, str, ..., bool]) is False
assert xisinstance((3, "a", "b", "c", True, False), XTuple[int, str, ..., bool, ...]) is True

# Type
class User: ...
class BaseUser(User): ...

assert xisinstance(BaseUser, Type[BaseUser]) is True
assert xisinstance(BaseUser, Type[User]) is True
assert xisinstance(User, Type[User]) is True
assert xisinstance(User, Type[BaseUser]) is False

# TypedDict
FullMovie = TypedDict("FullMovie", {"name": str, "year": int})

class PartialMovie(TypedDict, total=False):
    name: str
    year: int

assert xisinstance({"name": "The Matrix", "year": 1999}, FullMovie) is True
assert xisinstance({"name": "The Matrix", "year": "1999"}, FullMovie) is False
assert xisinstance({"name": "The Matrix"}, FullMovie) is False
assert xisinstance({"name": "The Matrix", "year": 1999, "extra": "qwe"}, FullMovie) is False

assert xisinstance({"name": "The Matrix", "year": 1999}, PartialMovie) is True
assert xisinstance({"name": "The Matrix"}, PartialMovie) is True
assert xisinstance({"name": "The Matrix", "year": 1999, "extra": "qwe"}, PartialMovie) is False
```
