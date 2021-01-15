import pytest

from typing_extend import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Type,
    TypedDict,
    Union,
    xisinstance,
)


class Pokemon:
    ...


class Pika(Pokemon):
    ...


class Bulbi(Pokemon):
    ...


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        (3, int, True),
        ("3", int, False),
        (Pika(), Pika, True),
        (Bulbi(), Pika, False),
        (Pika(), Pokemon, True),
        (Bulbi(), Pokemon, True),
    ],
)
def test_xisinstance_basic(obj, tp, expected):
    """It should work by default like builtin `isinstance`"""
    assert xisinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ("3", Any, True),
        ([1, "3"], Any, True),
    ],
)
def test_xisinstance_any(obj, tp, expected):
    """It should support `Any`"""
    assert xisinstance(obj, tp) is expected


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
def test_xisinstance_dict(obj, tp, expected):
    """It should support `Dict`"""
    assert xisinstance(obj, tp) is expected


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
def test_xisinstance_list(obj, tp, expected):
    """It should support `List`"""
    assert xisinstance(obj, tp) is expected


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
def test_xisinstance_set(obj, tp, expected):
    """It should support `Set`"""
    assert xisinstance(obj, tp) is expected


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
def test_xisinstance_tuple(obj, tp, expected):
    """It should support `Tuple`"""
    assert xisinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        (3, Optional[int], True),
        (None, Optional[int], True),
        ("3", Optional[int], False),
        (3, Union[int, str], True),
    ],
)
def test_xisinstance_union(obj, tp, expected):
    """It should support `Union` (and `Optional`)"""
    assert xisinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        (int, Type[int], True),
        (type(3), Type[int], True),
        (Pika, Type[Pika], True),
        (Pika, Type[Pokemon], True),
        (Bulbi, Type[Pika], False),
        (Bulbi, Type[Pokemon], True),
    ],
)
def test_xisinstance_type(obj, tp, expected):
    """It should support `Type`"""
    assert xisinstance(obj, tp) is expected


class FullMovie(TypedDict, total=True):
    name: str
    year: int


class PartialMovie(TypedDict, total=False):
    name: str
    year: int


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ({"name": "The Matrix", "year": 1999}, FullMovie, True),
        ({"name": "The Matrix", "year": "1999"}, FullMovie, False),
        ({"name": "The Matrix"}, FullMovie, False),
        ({"name": "The Matrix", "year": 1999, "extra": "qwe"}, FullMovie, False),
        ({"name": "The Matrix", "year": 1999}, PartialMovie, True),
        ({"name": "The Matrix"}, PartialMovie, True),
        ({"name": "The Matrix", "year": 1999, "extra": "qwe"}, PartialMovie, False),
    ],
)
def test_xisinstance_typeddict(obj, tp, expected):
    """It should support `TypeDict`"""
    assert xisinstance(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ("pika", Literal["pika"], True),
        (Literal["pika"], Literal["pika"], True),
        ("bulbi", Literal["pika"], False),
        ("bulbi", Literal["pika", "bulbi"], True),
        ("bulbi", Literal["pika", Literal[Literal["bulbi"]]], True),
        (Literal["pika", "bulbi"], Literal["bulbi", "pika"], True),
        (Literal["pika", "bulbi"], Literal["bulbi", "pika", "cara"], True),
    ],
)
def test_xisinstance_literal(obj, tp, expected):
    """It should support `Literal`"""
    assert xisinstance(obj, tp) is expected


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
def test_xisinstance_mix(obj, tp, expected):
    """It should support a mix of all those types"""
    assert xisinstance(obj, tp) is expected
