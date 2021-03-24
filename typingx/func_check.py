from functools import wraps
from inspect import signature
from typing import Any

from .main import isinstancex
from .typing_compat import display_type, get_type_hints


def func_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        sig = signature(func)

        # Default annotations types
        p_types = {
            p.name: Any if p.annotation is p.empty else p.annotation
            for p in sig.parameters.values()
        }
        p_types["return"] = Any
        # Add right annotations if set like `Annotated` or actual return type
        p_types.update(get_type_hints(func, include_extras=True))

        # Default set values
        p_values = {p.name: p.default for p in sig.parameters.values()}
        # Add set values
        p_values.update(dict(zip(p_values, args)))
        p_values.update(kwargs)

        for p_name, value in p_values.items():
            if not isinstancex(value, p_types[p_name]):
                raise TypeError(
                    f"Input {p_name} (value: {value!r}) is not "
                    f"a valid {display_type(p_types[p_name])}"
                )

        res = func(*args, **kwargs)

        # validate output
        if not isinstancex(res, p_types["return"]):
            raise TypeError(
                f"Output (value: {res!r}) is not a valid {display_type(p_types['return'])}"
            )

        return res

    return wrapper
