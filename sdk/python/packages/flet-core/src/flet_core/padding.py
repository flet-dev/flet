import dataclasses
from typing import Union


@dataclasses.dataclass
class Padding:
    left: Union[float, int] = dataclasses.field(default=None)
    top: Union[float, int] = dataclasses.field(default=None)
    right: Union[float, int] = dataclasses.field(default=None)
    bottom: Union[float, int] = dataclasses.field(default=None)


def all(value: float):
    return Padding(left=value, top=value, right=value, bottom=value)


def symmetric(vertical: float = 0, horizontal: float = 0):
    return Padding(left=horizontal, top=vertical, right=horizontal, bottom=vertical)


def only(left: float = 0, top: float = 0, right: float = 0, bottom: float = 0):
    return Padding(left=left, top=top, right=right, bottom=bottom)
