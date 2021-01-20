import collections

import pytest

from typingx import (
    Any,
    Dict,
    List,
    Listx,
    Literal,
    Mapping,
    NoneType,
    Optional,
    Sequence,
    Set,
    Tuple,
    Tuplex,
    Type,
    TypedDict,
    Union,
    get_args,
    get_origin,
    is_typeddict,
)


class FullMovie(TypedDict):
    name: str
    year: int


@pytest.mark.parametrize(
    "tp,expected_args",
    [
        (int, ()),
        (Any, ()),
        (Union[str, int], (str, int)),
        (Optional[str], (str, NoneType)),
        (List[int], (int,)),
        (Dict[str, int], (str, int)),
        (Set[str], (str,)),
        (Type[int], (int,)),
        (FullMovie, ()),
        (Literal["pika"], ("pika",)),
        (Literal["pika", Literal[Literal["bulbi"]]], ("pika", "bulbi")),
        (Listx[str], (str,)),
        (Listx[str, int], (str, int)),
        (Listx[str, int, ...], (str, int, ...)),
        (Listx[str, int, ..., bool], (str, int, ..., bool)),
        (Tuplex[str], (str,)),
        (Tuplex[str, int], (str, int)),
        (Tuplex[str, int, ...], (str, int, ...)),
        (Tuplex[str, int, ..., bool], (str, int, ..., bool)),
        (Sequence[int], (int,)),
        (Mapping[str, int], (str, int)),
    ],
)
def test_get_args(tp, expected_args):
    assert get_args(tp) == expected_args


@pytest.mark.parametrize(
    "tp,expected_origin",
    [
        (int, None),
        (Any, None),
        (Union[str, int], Union),
        (Optional[str], Union),
        (List[int], list),
        (Dict[str, int], dict),
        (Set[str], set),
        (Tuple[int], tuple),
        (Type[int], type),
        (FullMovie, None),
        (Literal["pika"], Literal),
        (Literal["pika", Literal[Literal["bulbi"]]], Literal),
        (Listx[str, int, ...], list),
        (Tuplex[str, int, ...], tuple),
        (Sequence[int], collections.abc.Sequence),
        (Mapping[str, int], collections.abc.Mapping),
    ],
)
def test_get_origin(tp, expected_origin):
    assert get_origin(tp) == expected_origin


def test_is_typeddict():
    assert is_typeddict(FullMovie) is True
    assert is_typeddict(dict) is False
