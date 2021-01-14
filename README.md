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
assert xisinstance({"a": 1, "b": 2}, Dict[str, int]) is True
assert xisinstance({"a": 1, "b": 2}, Dict[str, str]) is False
assert xisinstance({"a": 1, "b": 2}, Dict[int, str]) is False
assert xisinstance({"a": 1, "b": 2}, Dict[str, Any]) is True

# List
assert xisinstance([1, 2, 3], List[int]) is True
assert xisinstance([1, 2, "q"], List[int]) is False
assert xisinstance([1, 2, "q"], List[Union[str, int]]) is True

# Set
assert xisinstance({"a", "b"}, Set[str]) is True
assert xisinstance({"a", "b"}, Set[int]) is False

# Tuple
assert xisinstance((1, 2), Tuple[int, ...]) is True
assert xisinstance((1, 2), Tuple[int, int]) is True
assert xisinstance((1, 2), Tuple[int, int, int]) is False

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
