from typing import Any, Dict, List, Optional, Tuple, Union

import pytest

from typing_extend import extended_isinstance


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        # Basic `isinstance` checks
        (3, int, True),
        ("3", int, False),
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
    ],
)
def test_extended_isinstance(obj, tp, expected):
    assert extended_isinstance(obj, tp) is expected
