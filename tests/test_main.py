from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pytest

from typing_extend import extended_isinstance


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        # Basic `isinstance` checks
        (3, int, True),
        ("3", int, False),
        # Support `Any`
        ("3", Any, True),
        ([1, "3"], Any, True),
        # Support `Union`
        (3, Union[int, str], True),
        ([[3, 4], ["q", "w"]], List[Union[List[int], List[str]]], True),
        ([[3, 4, "q"], ["q", "w"]], List[Union[List[int], List[str]]], False),
        # Support `Optional`
        (3, Optional[int], True),
        (None, Optional[int], True),
        ("3", Optional[int], False),
        # Support `Tuple`
        ((3,), tuple, True),
        ((3,), Tuple, True),
        ((3,), Tuple[Any], True),
        ((3,), Tuple[int], True),
        ((3,), Tuple[int, ...], True),
        ((3,), Tuple[int, int], False),
        ((3,), Tuple[str], False),
        ((3,), Tuple[int, str], False),
        # Support `List`
        ([3], list, True),
        ([3], List, True),
        ([3], List[Any], True),
        ([3], List[int], True),
        (["3"], List[int], False),
        ([3, "3"], List[Union[int, str]], True),
        # Support `Set`
        ({"a"}, set, True),
        ({"a"}, Set, True),
        ({"a"}, Set[Any], True),
        ({"a"}, Set[str], True),
        ({"a", 1}, Set[str], False),
        ({"a", 1}, Set[Union[str, int]], True),
        # Support `Dict`
        ({"a": 1}, dict, True),
        ({"a": 1}, Dict, True),
        ({"a": 1}, Dict[Any, Any], True),
        ({"a": 1}, Dict[str, Any], True),
        ({"a": 1}, Dict[int, Any], False),
    ],
)
def test_extended_isinstance(obj, tp, expected):
    assert extended_isinstance(obj, tp) is expected
