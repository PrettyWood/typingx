from collections import ChainMap, Counter

import pytest

from typingx import (
    Any,
    Dict,
    List,
    Listx,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Tuplex,
    Type,
    TypedDict,
    Union,
    isinstancex,
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
def test_isinstancex_basic(obj, tp, expected):
    """It should work by default like builtin `isinstance`"""
    assert isinstancex(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ("3", Any, True),
        ([1, "3"], Any, True),
    ],
)
def test_isinstancex_any(obj, tp, expected):
    """It should support `Any`"""
    assert isinstancex(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ({"a": 1}, dict, True),
        ({"a": 1}, Dict, True),
        ({"a": 1}, Dict[Any, Any], True),
        ({"a": 1}, Dict[str, Any], True),
        ({"a": 1}, Dict[int, Any], False),
        (["a", "b"], Dict[str, str], False),
    ],
)
def test_isinstancex_dict(obj, tp, expected):
    """It should support `Dict`"""
    assert isinstancex(obj, tp) is expected


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
        ((3, 4), List[int], False),
    ],
)
def test_isinstancex_list(obj, tp, expected):
    """It should support `List`"""
    assert isinstancex(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ({"a"}, set, True),
        ({"a"}, Set, True),
        ({"a"}, Set[Any], True),
        ({"a"}, Set[str], True),
        ({"a", 1}, Set[str], False),
        ({"a", 1}, Set[Union[str, int]], True),
        (("a", "b"), Set[int], False),
    ],
)
def test_isinstancex_set(obj, tp, expected):
    """It should support `Set`"""
    assert isinstancex(obj, tp) is expected


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
        ([3], Tuple[int], False),
    ],
)
def test_isinstancex_tuple(obj, tp, expected):
    """It should support `Tuple`"""
    assert isinstancex(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ([3], Listx, True),
        ([3], Listx[Any], True),
        ([3], Listx[int], True),
        ([3, 4, 5], Listx[int], True),
        ([3, "pika"], Listx[int, int], False),
        ([3], Listx[str], False),
        ([3, "pika"], Listx[int, str, ...], True),
        ([1, 2, "q", "w", "e"], Listx[int, ..., str], False),
        ([1, 2, "q", "w", "e"], Listx[int, ..., str, ...], True),
        ([3, "pika", "bulbi"], Listx[int, str, ...], True),
        ([3, "pika", "bulbi", "cara"], Listx[int, str, ...], True),
        ([3, "pika", "bulbi", "cara"], Listx[int, str, ..., bool], False),
        ([3, "pika", "bulbi", "cara", True], Listx[int, str, ..., bool], True),
        ([3, "pika", "bulbi", "cara", 3], Listx[int, str, ..., bool], False),
        ([3, "pika", "bulbi", "cara", True, False], Listx[int, str, ..., bool, ...], True),
    ],
)
def test_isinstancex_xlist(obj, tp, expected):
    """It should support `Listx`"""
    assert isinstancex(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ((3,), Tuplex, True),
        ((3,), Tuplex[Any], True),
        ((3,), Tuplex[int], True),
        ((3,), Tuplex[int, ...], True),
        ((3,), Tuplex[int, int], False),
        ((3,), Tuplex[str], False),
        ((3, "pika"), Tuplex[int, str, ...], True),
        ((3, "pika", "bulbi"), Tuplex[int, str, ...], True),
        ((3, "pika", "bulbi", "cara"), Tuplex[int, str, ...], True),
        ((3, "pika", "bulbi", "cara"), Tuplex[int, str, ..., bool], False),
        ((3, "pika", "bulbi", "cara", True), Tuplex[int, str, ..., bool], True),
        ((3, "pika", "bulbi", "cara", 3), Tuplex[int, str, ..., bool], False),
        ((3, "pika", "bulbi", "cara", True, False), Tuplex[int, str, ..., bool, ...], True),
    ],
)
def test_isinstancex_xtuple(obj, tp, expected):
    """It should support `Tuplex`"""
    assert isinstancex(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        (3, Optional[int], True),
        (None, Optional[int], True),
        ("3", Optional[int], False),
        (3, Union[int, str], True),
    ],
)
def test_isinstancex_union(obj, tp, expected):
    """It should support `Union` (and `Optional`)"""
    assert isinstancex(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        (int, Type[int], True),
        (type(3), Type[int], True),
        (Pika, Type[Pika], True),
        (Pika, Type[Pokemon], True),
        (Bulbi, Type[Pika], False),
        (Bulbi, Type[Pokemon], True),
        (3, Type[int], False),
    ],
)
def test_isinstancex_type(obj, tp, expected):
    """It should support `Type`"""
    assert isinstancex(obj, tp) is expected


class FullMovie(TypedDict, total=True):
    name: str
    year: int


class PartialMovie(TypedDict, total=False):
    name: str
    year: int


class StrExtra(TypedDict):
    a: int
    b: float
    __extra__: str


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ((1,), FullMovie, False),
        ({1: "a", "b": "c"}, FullMovie, False),
        ({"name": "The Matrix", "year": 1999}, FullMovie, True),
        ({"name": "The Matrix", "year": "1999"}, FullMovie, False),
        ({"name": "The Matrix"}, FullMovie, False),
        ({"name": "The Matrix", "year": 1999, "extra": "qwe"}, FullMovie, False),
        ({"name": "The Matrix", "year": 1999}, PartialMovie, True),
        ({"name": "The Matrix"}, PartialMovie, True),
        ({"name": "The Matrix", "year": 1999, "extra": "qwe"}, PartialMovie, False),
        ({"a": 1}, StrExtra, False),
        ({"a": 1, "b": 0.1}, StrExtra, True),
        ({"a": 1, "b": 0.1, "c": "pika", "d": "bulbi"}, StrExtra, True),
        ({"a": 1, "b": 0.1, "c": "pika", "d": 1}, StrExtra, False),
    ],
)
def test_isinstancex_typeddict(obj, tp, expected):
    """It should support `TypeDict`"""
    assert isinstancex(obj, tp) is expected


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
def test_isinstancex_literal(obj, tp, expected):
    """It should support `Literal`"""
    assert isinstancex(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        (1, Sequence[str], False),
        ("pika", Sequence[str], True),
        (["pika", "chu"], Sequence[str], True),
        (("pika", "chu"), Sequence[str], True),
        (("pika", "chu"), Sequence[int], False),
    ],
)
def test_isinstancex_sequence(obj, tp, expected):
    """It should support `Sequence`"""
    assert isinstancex(obj, tp) is expected


@pytest.mark.parametrize(
    "obj,tp,expected",
    [
        ("pika", Mapping[str, int], False),
        ({"pika": "chu"}, Mapping[str, str], True),
        ({"pika": "chu"}, Mapping[str, int], False),
        (Counter({"red": 4, "blue": 2}), Mapping[str, int], True),
        (Counter({"red": 4, "blue": 2}), Mapping[int, int], False),
        (
            ChainMap({"art": "van gogh", "opera": "carmen"}, {"music": "bach", "art": "rembrandt"}),
            Mapping[str, str],
            True,
        ),
    ],
)
def test_isinstancex_mapping(obj, tp, expected):
    """It should support `Mapping`"""
    assert isinstancex(obj, tp) is expected


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
def test_isinstancex_mix(obj, tp, expected):
    """It should support a mix of all those types"""
    assert isinstancex(obj, tp) is expected
