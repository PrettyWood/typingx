import sys

import pytest

from typingx import Annotated, Constraints, func_check


def test_args():
    @func_check
    def my_func(a: int, b: int) -> int:
        return a + b

    assert my_func(a=1, b=2) == 3

    with pytest.raises(TypeError) as e:
        my_func(1, "x")
    assert str(e.value) == "Input b (value: 'x') is not a valid int"


def test_untyped():
    @func_check
    def foo(a, b):
        return f"{a} {b}"

    assert foo(1, 2) == "1 2"
    assert foo(1, "2") == "1 2"
    assert foo("1", "2") == "1 2"


@pytest.mark.skipif(sys.version_info < (3, 7), reason="Annotated should be used with 3.7+")
def test_annotated():
    @func_check
    def my_func(a: int, b: Annotated[int, Constraints(ge=5)]) -> Annotated[int, Constraints(le=10)]:
        return a + b

    with pytest.raises(TypeError) as e:
        my_func(1, 4)
    assert str(e.value) == "Input b (value: 4) is not a valid Annotated[int, Constraints(ge=5)]"

    assert my_func(1, 6) == 7

    with pytest.raises(TypeError) as e:
        my_func(5, 6)
    assert str(e.value) == "Output (value: 11) is not a valid Annotated[int, Constraints(le=10)]"
