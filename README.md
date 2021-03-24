# typingx
[![Tests](https://github.com/PrettyWood/typingx/workflows/Tests/badge.svg)](https://github.com/PrettyWood/typingx/actions)
[![codecov](https://codecov.io/gh/PrettyWood/typingx/branch/main/graph/badge.svg)](https://codecov.io/gh/PrettyWood/typingx)
[![pypi](https://img.shields.io/pypi/v/typingx.svg)](https://pypi.python.org/pypi/typingx)
[![versions](https://img.shields.io/pypi/pyversions/typingx.svg)](https://github.com/PrettyWood/typingx)
[![license](https://img.shields.io/github/license/PrettyWood/typingx.svg)](https://github.com/PrettyWood/typingx/blob/master/LICENSE)


How many times have you wanted to check the shape of your data either in application code or while testing?
With this library, you can leverage `typing` types at runtime to do that!

_This is even more powerful when used with generic standard collections (e.g. `list[str]`) introduced in python 3.9 and new union operator `|`
introduced in python 3.10. If you want to use them with older version, a backport [future-typing](https://github.com/PrettyWood/future-typing) exists!_

### Example
```python
# Check if `x` is a string or an integer
isinstancex(x, str | int)

# Check if `my_list` has only numbers
isinstancex(my_list, list[int | float])

# Check if `my_set` has only integers greater than 2 with at least 3 distinct ones
Gt2Int = Annotated[int, Constraints(gt=2)]
isinstancex(my_set, Annotated[set[Gt2Int], Constraints(min_length=3)])  # or `typing.Set`

# Check deeper the shape of `my_dict`
isinstancex(my_dict, {'a': int, 'b': bool, ...: str})  # shortcut for `typing.TypedDict('TD', {'a': int, 'b': bool, __extra__: str})`

# Check if all the keys are 1 lower case letter and values are integers with 1 digit
OneLowerStr = Annotated[str, Constraints(regex='^[a-z]$')]
OneDigitUInt = Annotated[int, Constraints(ge=0, lt=10)]
isinstancex(my_dict, dict[OneLowerStr, OneDigitUInt])

@func_check
def my_func(a: int, b: Annotated[int, Constraints(ge=5)]) -> Annotated[int, Constraints(le=10)]:
    return a + b

try:
    my_func(1, 4)
except TypeError as e:
    assert str(e) == "Input b (value: 4) is not a valid Annotated[int, Constraints(ge=5)]"

try:
    my_func(5, 6)
except TypeError as e:
    assert str(e) == "Output (value: 11) is not a valid Annotated[int, Constraints(le=10)]"
```

Since `typing` changed a lot since python `3.6`, this library also makes sure the whole behaviour
is consistent with `3.10` for all python versions.

It hence provides:
- [`isinstancex`](#isinstancex): like `isinstance` and `issubclass` but with `typing` types and extra types provided by this library
  
  :warning: using a tuple as second parameter will validate against `Tuplex`. If you want to check against multiple types `(int, str)`, wrap it into `Union[(int, str)]`!
- [`issubclassx`](#issubclassx-warning-still-in-wip): same as `isinstancex` but for `issubclass`
- `func_check`: a decorator to check inputs and output of a function based on annotation
- `get_args` and `get_origin` that have the exact same behaviour as the `typing` module with python 3.10, no matter which python version is used!
- `is_literal`, `is_newtype`, `is_typeddict` helpers
- most `typing` types but with homogeneous behaviour (e.g. with `3.8`, this libray will choose `typing_extensions.TypedDict` instead of `typing.TypedDict` since the latter doesn't store information to distinguish optional and required keys)
- extanded types:
  * `TypedDict` with `...` field to allow type checking on optional fields
- extra types:
  * `Listx` and `Tuplex`: more sophisticated versions of `List` and `Tuple` to add `...` anywhere in the parameters

## Installation

``` bash
    pip install typingx
```

## isinstancex

```python
from collections import ChainMap, Counter

from typingx import *

T, U = TypeVar('T'), TypeVar('U')

# Annotated
GT2 = Annotated[int, Constraints(gt=2)]
assert isinstancex(1, int) is True
assert isinstancex(1, GT2) is False
assert isinstancex(3, GT2) is True
assert isinstancex([3, 3], list[GT2]) is True

Between2And5 = Annotated[Union[float, int], Constraints(ge=2, le=5)]
assert isinstancex(3, Between2And5) is True
assert isinstancex(3.5, Between2And5) is True
assert isinstancex('3.5', Between2And5) is False

assert isinstancex(3, Annotated[int, Constraints(multiple_of=1.5)]) is True
assert isinstancex(3., Annotated[int, Constraints(multiple_of=1.5)]) is False
assert isinstancex(3., Annotated[Union[int, float], Constraints(multiple_of=1.5)]) is True

Mult1_5AndLe2 = Annotated[Union[int, float], Constraints(multiple_of=1.5, le=10)]
assert isinstancex(15, Mult1_5AndLe2) is False
assert isinstancex([3.0, 4.5, 9], list[Mult1_5AndLe2]) is True
assert isinstancex([3., 4.3], list[Mult1_5AndLe2]) is False

OneLowerStr = Annotated[str, Constraints(regex='^[a-z]$')]
OneDigitUInt = Annotated[int, Constraints(ge=0, lt=10)]
assert isinstancex({'a': 1, 'b': 2}, dict[OneLowerStr, OneDigitUInt]) is True
assert isinstancex({'a': 1, 'bc': 2}, dict[OneLowerStr, OneDigitUInt]) is False

# Callable
def f(x: int, y: float) -> str:
    return f'{x}{y}'

assert isinstancex(f, Callable) is True
assert isinstancex(f, Callable[..., Any]) is True
assert isinstancex(f, Callable[..., str]) is True
assert isinstancex(f, Callable[[int, float], str]) is True
assert isinstancex(f, Callable[[T, float], U][int, str]) is True

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
assert isinstancex([1, 2, 3, 4], Listx[int]) is False
assert isinstancex([1, 2, 3, 4], Listx[int, ...]) is True
assert isinstancex([1, 2, "q"], Listx[int, ..., str]) is True
assert isinstancex([1, 2, "q", "w", "e"], Listx[int, ..., str]) is False
assert isinstancex([1, 2, "q", "w", "e"], Listx[int, ..., str, ...]) is True
assert isinstancex([1, 2, "q", "w", b"xyz", "e"], Listx[int, ..., str, ...]) is False
assert isinstancex([1, 2, "q", "w", b"xyz", "e"], Listx[int, ..., Union[str, bytes], ...]) is True

# Listx (shortcut)
assert isinstancex([1, 2, 3, 4, "q"], [int, ..., str]) is True

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

# Tuple
assert isinstancex((), Tuple[()]) is True
assert isinstancex((1,), Tuple[()]) is True
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

# Tuplex (shortcut)
assert isinstancex((True, "q", "q", "q", "q"), (bool, Literal["q"], ...)) is True

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

# TypedDict (shortcut)
assert isinstancex({"name": "The Matrix", "year": 1999, "q": "w", "e": "r"}, {"name": str, "year": int, ...: str}) is True

# Union
assert isinstancex(3, Union[str, int]) is True
assert isinstancex(3, Union[str, float]) is False
assert isinstancex(3.14, Union[int, T, str][bool]) is False
assert isinstancex(3.14, Union[int, T, str][float]) is True
```

## issubclassx (:warning: still in WIP)
```python
from typingx import *

assert issubclassx(int, int) is True
assert issubclassx(int, object) is True
assert issubclassx(int, float) is False
assert issubclassx(int, int | str) is True
assert issubclassx(tuple[int], tuple) is True
assert issubclassx(tuple[int], tuple[Any]) is True
assert issubclassx(tuple[int], tuple[Any, ...]) is True
assert issubclassx(tuple[int, str], tuple[object, ...]) is True
assert issubclassx(tuple[int, str], tuple[Any]) is False
assert issubclassx(tuple[int, int], (int, ...)) is True
assert issubclassx(tuple[int, int], (int, str)) is False
assert issubclassx(tuple[int, int], (int, Any)) is True
```
