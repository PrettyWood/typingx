from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pytest

from typing_extend import get_args, get_origin


@pytest.mark.parametrize(
    "tp,expected_args",
    [
        (int, ()),
        (List[int], (int,)),
        (Dict[str, int], (str, int)),
    ],
)
def test_get_args(tp, expected_args):
    assert get_args(tp) == expected_args


@pytest.mark.parametrize(
    "tp,expected_origin",
    [
        (int, None),
        (List[int], list),
        (Dict[str, int], dict),
    ],
)
def test_get_origin(tp, expected_origin):
    assert get_origin(tp) == expected_origin
