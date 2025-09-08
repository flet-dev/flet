from collections.abc import Sequence
from typing import Any


def shallow_compare_args(
    prev_args: Sequence[Any],
    args: Sequence[Any],
) -> bool:
    if prev_args is args:
        return True
    if len(prev_args) != len(args):
        return False
    return all(not (a is not b and a != b) for a, b in zip(prev_args, args))


def shallow_compare_kwargs(
    prev_kwargs: dict[str, Any],
    kwargs: dict[str, Any],
) -> bool:
    if prev_kwargs is kwargs:
        return True
    if prev_kwargs.keys() != kwargs.keys():
        return False
    for k in prev_kwargs:
        a, b = prev_kwargs[k], kwargs[k]
        if a is not b and a != b:
            return False
    return True


def shallow_compare_args_and_kwargs(
    prev_args: tuple[Any, ...],
    prev_kwargs: dict[str, Any],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
) -> bool:
    return shallow_compare_args(prev_args, args) and shallow_compare_kwargs(
        prev_kwargs, kwargs
    )
