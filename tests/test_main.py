from typing import Any, Dict, List, Optional, Set, Tuple, Union

import pytest

from typing_extend import extended_isinstance


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        (3, int, True),
        ("3", int, False),
    ],
)
def test_extended_isinstance_basic(obj, tp, expected):
    """It should work by default like builtin `isinstance`"""
    assert extended_isinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ("3", Any, True),
        ([1, "3"], Any, True),
    ],
)
def test_extended_isinstance_any(obj, tp, expected):
    """It should support `Any`"""
    assert extended_isinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ({"a": 1}, dict, True),
        ({"a": 1}, Dict, True),
        ({"a": 1}, Dict[Any, Any], True),
        ({"a": 1}, Dict[str, Any], True),
        ({"a": 1}, Dict[int, Any], False),
    ],
)
def test_extended_isinstance_dict(obj, tp, expected):
    """It should support `Dict`"""
    assert extended_isinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ([3], list, True),
        ([3], List, True),
        ([3], List[Any], True),
        ([3], List[int], True),
        ([3, 4, 1, 2], List[int], True),
        (["3"], List[int], False),
        ([3, 4, "1", 2], List[int], False),
        ([3, 4, 1.1, 2], List[float], False),
    ],
)
def test_extended_isinstance_list(obj, tp, expected):
    """It should support `List`"""
    assert extended_isinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ({"a"}, set, True),
        ({"a"}, Set, True),
        ({"a"}, Set[Any], True),
        ({"a"}, Set[str], True),
        ({"a", 1}, Set[str], False),
        ({"a", 1}, Set[Union[str, int]], True),
    ],
)
def test_extended_isinstance_set(obj, tp, expected):
    """It should support `Set`"""
    assert extended_isinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ((3,), tuple, True),
        ((3,), Tuple, True),
        ((3,), Tuple[Any], True),
        ((3,), Tuple[int], True),
        ((3,), Tuple[int, ...], True),
        ((3,), Tuple[int, int], False),
        ((3,), Tuple[str], False),
        ((3,), Tuple[int, str], False),
    ],
)
def test_extended_isinstance_tuple(obj, tp, expected):
    """It should support `Tuple`"""
    assert extended_isinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        (3, Optional[int], True),
        (None, Optional[int], True),
        ("3", Optional[int], False),
        (3, Union[int, str], True),
    ],
)
def test_extended_isinstance_union(obj, tp, expected):
    """It should support `Union` (and `Optional`)"""
    assert extended_isinstance(obj, tp) is expected


Number = Union[int, float]


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ([3, 4, 1.1, 2], List[Number], True),
        ([3, "3"], List[Union[int, str]], True),
        ([[3, 4], ["q", "w"]], List[Union[List[int], List[str]]], True),
        ([[3, 4, "q"], ["q", "w"]], List[Union[List[int], List[str]]], False),
    ],
)
def test_extended_isinstance_mix(obj, tp, expected):
    """It should support a mix of all those types"""
    assert extended_isinstance(obj, tp) is expected
