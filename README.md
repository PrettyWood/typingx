# typing-extend
[![Tests](https://github.com/PrettyWood/typing-extend/workflows/Tests/badge.svg)](https://github.com/PrettyWood/typing-extend/actions)
[![codecov](https://codecov.io/gh/PrettyWood/typing-extend/branch/main/graph/badge.svg)](https://codecov.io/gh/PrettyWood/typing-extend)
[![pypi](https://img.shields.io/pypi/v/typing-extend.svg)](https://pypi.python.org/pypi/typing-extend)
[![versions](https://img.shields.io/pypi/pyversions/typing-extend.svg)](https://github.com/PrettyWood/typing-extend)
[![license](https://img.shields.io/github/license/PrettyWood/typing-extend.svg)](https://github.com/PrettyWood/typing-extend/blob/master/LICENSE)

Extend `typing` functionalities

## Installation

``` bash
    pip install typing_extend
```

## Usage
```python
# By default `typing_extend` forwards most `typing` types
from typing_extend import Any, Dict, List, Set, Tuple, Type, TypedDict, Union, xisinstance

# Dict
assert xisinstance({"a": 1, "b": 2}, Dict[str, int])
assert not xisinstance({"a": 1, "b": 2}, Dict[str, str])
assert not xisinstance({"a": 1, "b": 2}, Dict[int, str])
assert xisinstance({"a": 1, "b": 2}, Dict[str, Any])

# List
assert xisinstance([1, 2, 3], List[int])
assert not xisinstance([1, 2, "q"], List[int])
assert xisinstance([1, 2, "q"], List[Union[str, int]])

# Set
assert xisinstance({"a", "b"}, Set[str])
assert not xisinstance({"a", "b"}, Set[int])

# Tuple
assert xisinstance((1, 2), Tuple[int, ...])
assert xisinstance((1, 2), Tuple[int, int])
assert not xisinstance((1, 2), Tuple[int, int, int])

# Type
class User: ...
class BaseUser(User): ...

assert xisinstance(BaseUser, Type[BaseUser])
assert xisinstance(BaseUser, Type[User])
assert xisinstance(User, Type[User])
assert not xisinstance(User, Type[BaseUser])

# TypedDict
FullMovie = TypedDict("FullMovie", {"name": str, "year": int})

class PartialMovie(TypedDict, total=False):
    name: str
    year: int

assert xisinstance({"name": "The Matrix", "year": 1999}, FullMovie)
assert not xisinstance({"name": "The Matrix"}, FullMovie)
assert not xisinstance({"name": "The Matrix", "year": 1999, "extra": "qwe"}, FullMovie)

assert xisinstance({"name": "The Matrix", "year": 1999}, PartialMovie)
assert xisinstance({"name": "The Matrix"}, PartialMovie)
assert not xisinstance({"name": "The Matrix", "year": 1999, "extra": "qwe"}, PartialMovie)
```
