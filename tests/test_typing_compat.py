import pytest

from typing_extend import (
    Any,
    Dict,
    List,
    Literal,
    NoneType,
    Optional,
    Set,
    Tuple,
    Type,
    TypedDict,
    Union,
    XList,
    XTuple,
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
        (XList[str], (str,)),
        (XList[str, int], (str, int)),
        (XList[str, int, ...], (str, int, ...)),
        (XList[str, int, ..., bool], (str, int, ..., bool)),
        (XTuple[str], (str,)),
        (XTuple[str, int], (str, int)),
        (XTuple[str, int, ...], (str, int, ...)),
        (XTuple[str, int, ..., bool], (str, int, ..., bool)),
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
        (XList[str, int, ...], list),
        (XTuple[str, int, ...], tuple),
    ],
)
def test_get_origin(tp, expected_origin):
    assert get_origin(tp) == expected_origin


def test_is_typeddict():
    assert is_typeddict(FullMovie) is True
    assert is_typeddict(dict) is False
