from typing_extend import TypedDict
from typing_extend.utils import lenient_isinstance, lenient_issubclass


def test_lenient_isinstance():
    assert lenient_isinstance(3, int)
    assert lenient_isinstance(3, (str, int))
    assert not lenient_isinstance(3, TypedDict)
    assert lenient_isinstance(3, (TypedDict, int))


def test_lenient_issubclass():
    assert lenient_issubclass(int, int)
    assert lenient_issubclass(int, (str, int))
    assert not lenient_issubclass(3, int)
    assert not lenient_issubclass(int, TypedDict)
    assert lenient_issubclass(int, (TypedDict, int))
