from typing import (
    Any,
    Type,
    List,
)


def assert_type(var: Any, varname: str, type_: Type, noneable=False) -> None:
    assert noneable or var, f"{varname} is None"
    assert isinstance(var, type_),\
        f"Invalid type {varname}. Desire {type_} but given {type(var)}"


def assert_types(var: Any, varname: str, types: List[Type]) -> None:
    assert any(isinstance(var, t) for t in types), \
        f"Invalid type {varname}. Valid list: {types}"
