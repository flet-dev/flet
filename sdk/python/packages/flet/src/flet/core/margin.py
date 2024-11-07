import dataclasses
from typing import Union


@dataclasses.dataclass
class Margin:
    left: Union[float, int]
    top: Union[float, int]
    right: Union[float, int]
    bottom: Union[float, int]


def all(value: float) -> Margin:
    return Margin(left=value, top=value, right=value, bottom=value)


def symmetric(vertical: float = 0, horizontal: float = 0) -> Margin:
    return Margin(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


def only(
        left: float = 0, top: float = 0, right: float = 0, bottom: float = 0
) -> Margin:
    return Margin(left=left, top=top, right=right, bottom=bottom)
