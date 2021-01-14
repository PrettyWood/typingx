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
from typing import Any, Dict, List, Set, Tuple, Union
from typing_extend import extended_isinstance

# Dict
assert extended_isinstance({'a': 1, 'b': 2}, Dict[str, int])
assert not extended_isinstance({'a': 1, 'b': 2}, Dict[str, str])
assert not extended_isinstance({'a': 1, 'b': 2}, Dict[int, str])
assert extended_isinstance({'a': 1, 'b': 2}, Dict[str, Any])

# List
assert extended_isinstance([1, 2, 3], List[int])
assert not extended_isinstance([1, 2, 'q'], List[int])
assert extended_isinstance([1, 2, 'q'], List[Union[str, int]])

# Set
assert extended_isinstance({'a', 'b'}, Set[str])
assert not extended_isinstance({'a', 'b'}, Set[int])

# Tuple
assert extended_isinstance((1, 2), Tuple[int, ...])
assert extended_isinstance((1, 2), Tuple[int, int])
assert not extended_isinstance((1, 2), Tuple[int, int, int])

# Type
assert extended_isinstance(BaseUser, Type[User])
assert extended_isinstance(User, Type[User])
assert not extended_isinstance(AnotherClass, Type[User])
```
