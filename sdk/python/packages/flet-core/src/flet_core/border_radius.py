import dataclasses
from typing import Union


@dataclasses.dataclass
class BorderRadius:
    topLeft: Union[float, int] = dataclasses.field(default=0)
    topRight: Union[float, int] = dataclasses.field(default=0)
    bottomLeft: Union[float, int] = dataclasses.field(default=0)
    bottomRight: Union[float, int] = dataclasses.field(default=0)


def all(value: float):
    return BorderRadius(
        topLeft=value, topRight=value, bottomLeft=value, bottomRight=value
    )


def horizontal(left: float = 0, right: float = 0):
    return BorderRadius(
        topLeft=left, topRight=right, bottomLeft=left, bottomRight=right
    )


def vertical(top: float = 0, bottom: float = 0):
    return BorderRadius(
        topLeft=top, topRight=top, bottomLeft=bottom, bottomRight=bottom
    )


def only(
    topLeft: float = 0,
    topRight: float = 0,
    bottomLeft: float = 0,
    bottomRight: float = 0,
):
    return BorderRadius(
        topLeft=topLeft,
        topRight=topRight,
        bottomLeft=bottomLeft,
        bottomRight=bottomRight,
    )
