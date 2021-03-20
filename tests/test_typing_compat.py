import collections

import pytest

from typingx import (
    Annotated,
    Any,
    Callable,
    Collection,
    Constraints,
    Dict,
    FrozenSet,
    Generic,
    List,
    Listx,
    Literal,
    Mapping,
    NewType,
    NoneType,
    Optional,
    Sequence,
    Set,
    Tuple,
    Tuplex,
    Type,
    TypedDict,
    TypeVar,
    Union,
    get_args,
    get_origin,
    is_literal,
    is_newtype,
    is_typeddict,
)


class FullMovie(TypedDict):
    name: str
    year: int


S = TypeVar("S", int, str)
T = TypeVar("T")
U = TypeVar("U")


class StrangePair(Generic[T, S]):
    ...


@pytest.mark.parametrize(
    "tp,expected_args",
    [
        (int, ()),
        (Any, ()),
        (Dict, ()),
        (List, ()),
        (Set, ()),
        (FrozenSet, ()),
        (Type, ()),
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
        (StrangePair[int, str], (int, str)),
        (StrangePair, ()),
        (Callable, ()),
        (Callable[..., str], (..., str)),
        (Callable[[int], str], ([int], str)),
        (Union[int, T, str][float], (int, float, str)),
        (Callable[[], T][int], ([], int)),
        (Callable[[T], T][int], ([int], int)),
        (Callable[[T, float], U][int, str], ([int, float], str)),
        (List[Collection[T]][int], (Collection[int],)),
        (
            Mapping[T, Sequence[U]][str, int],
            (
                str,
                Sequence[int],
            ),
        ),
        (
            Mapping[str, Mapping[T, Collection[U]]][float, int],
            (
                str,
                Mapping[float, Collection[int]],
            ),
        ),
        (Annotated[int, Constraints(ge=4)], (int, Constraints(ge=4))),
        (Annotated[Union[int, float], Constraints(ge=4)], (Union[int, float], Constraints(ge=4))),
    ],
)
def test_get_args(tp, expected_args):
    assert get_args(tp) == expected_args


@pytest.mark.parametrize(
    "tp,expected_origin",
    [
        (int, None),
        (Any, None),
        (Dict, dict),
        (List, list),
        (Set, set),
        (FrozenSet, frozenset),
        (Tuple, tuple),
        (Type, type),
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
        (Generic, Generic),
        (Generic[T], Generic),
        (Union[T, int], Union),
        (Union[T, int][str], Union),
        (List[Tuple[T, T]][int], list),
        (StrangePair[int, str], StrangePair),
        (Callable, collections.abc.Callable),
        (Callable[..., str], collections.abc.Callable),
        (Callable[[int], str], collections.abc.Callable),
        (Collection, collections.abc.Collection),
        (Collection[int], collections.abc.Collection),
        (Annotated[int, Constraints(ge=4)], Annotated),
        (Annotated[Union[int, float], Constraints(ge=4)], Annotated),
    ],
)
def test_get_origin(tp, expected_origin):
    assert get_origin(tp) == expected_origin


def test_is_literal():
    assert is_literal(Literal["pika"]) is True
    assert is_literal(int) is False


def test_is_typeddict():
    assert is_typeddict(FullMovie) is True
    assert is_typeddict(dict) is False


def test_is_newtype():
    UserId = NewType("UserId", int)
    assert is_newtype(UserId) is True
    assert is_newtype(int) is False
