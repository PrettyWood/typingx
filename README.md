# typingx
[![Tests](https://github.com/PrettyWood/typingx/workflows/Tests/badge.svg)](https://github.com/PrettyWood/typingx/actions)
[![codecov](https://codecov.io/gh/PrettyWood/typingx/branch/main/graph/badge.svg)](https://codecov.io/gh/PrettyWood/typingx)
[![pypi](https://img.shields.io/pypi/v/typingx.svg)](https://pypi.python.org/pypi/typingx)
[![versions](https://img.shields.io/pypi/pyversions/typingx.svg)](https://github.com/PrettyWood/typingx)
[![license](https://img.shields.io/github/license/PrettyWood/typingx.svg)](https://github.com/PrettyWood/typingx/blob/master/LICENSE)


How many times have you wanted to answer one of those questions in application code or while writing tests?
- Is `x` a valid list of only `int` values
- Is `x` a dictionary with only `'a'` and `'b'` keys
- ...

This library purpose is to leverage `typing` (and `typing_extensions` for python 3.8-) types at runtime
to do some validations on a type or an object.
Since `typing` changed a lot since python `3.6`, this library also makes sure the whole behaviour
is consistent with the latest python version `3.10`.

It hence provides:
- `isinstancex` and `issubclassx`: like `isinstance` and `issubclass` but with `typing` types and extra types provided by this library
- `get_args` and `get_origin` that have the exact same behaviour as the `3.10` python version ones, no matter which python version is used (the only exception being `get_args` with `Generic` on python 3.6)
- `is_literal`, `is_newtype`, `is_typeddict` helpers
- most `typing` types but with homogeneous behaviour (e.g. with `3.8`, this libray will choose `typing_extensions.TypedDict` instead of `typing.TypedDict` since the latter doesn't store information to distinguish optional and required keys)
- extanded types:
  * `TypedDict` has a `__extra__` field (value can be changed) to allow type checking on optional fields
- extra types:
  * `Listx` and `Tuplex`: more sophisticated versions of `List` and `Tuple` to add `...` anywhere in the parameters

## Installation

``` bash
    pip install typingx
```

## Usage
```python
from collections import ChainMap, Counter

from typingx import *

# Dict
assert isinstancex({"a": 1, "b": 2}, Dict[str, int]) is True
assert isinstancex({"a": 1, "b": 2}, Dict[str, str]) is False
assert isinstancex({"a": 1, "b": 2}, Dict[int, str]) is False
assert isinstancex({"a": 1, "b": 2}, Dict[str, Any]) is True
# Can be written with the shortcut!
assert isinstancex({"a": 1, "b": 2}, {str: int}) is True

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
# Can be written with the shortcut!
assert isinstancex([1, 2, 3, 4], [int]) is True

# Literal
assert isinstancex("a", Literal["a"]) is True
assert isinstancex(Literal["a"], Literal["a"]) is True
assert isinstancex("b", Literal["a"]) is False
assert isinstancex("b", Literal["a", Literal[Literal["b"]]]) is True
assert isinstancex(Literal["a", "b"], Literal["b", "a", "c"]) is True

# Mapping
assert isinstancex(Counter({"red": 4, "blue": 2}), Mapping[str, int]) is True
assert isinstancex(ChainMap({"art": "van gogh"}, {"music": "bach"}), Mapping[str, str]) is True

# NewType
UserId = NewType("UserId", int)
ProUserId = NewType("ProUserId", UserId)

assert isinstancex(1, UserId) is True
assert isinstancex(1, ProUserId) is True
assert isinstancex(UserId(1), UserId) is True
assert isinstancex("3", UserId) is False

# None
assert isinstancex([None, None], List[None]) is True
assert isinstancex([None, None], List[NoneType]) is True
assert isinstancex([None, None], List[type(None)]) is True
assert isinstancex([None, None], List[Literal[None]]) is True

# Sequence
assert isinstancex("abc", Sequence[Any]) is True
assert isinstancex("abc", Sequence[int]) is False
assert isinstancex((1, 3, 5), Sequence[int]) is True

# Set
assert isinstancex({"a", "b"}, Set[str]) is True
assert isinstancex({"a", "b"}, Set[int]) is False
# Can be written with the shortcut!
assert isinstancex({"a", "b"}, {str}) is True

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
# Can be written with the shortcut!
assert isinstancex((3, "a", "b", "c"), (int, str, ...)) is True

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
