import dataclasses
from typing import Union


@dataclasses.dataclass
class BorderRadius:
    top_left: Union[float, int]
    top_right: Union[float, int]
    bottom_left: Union[float, int]
    bottom_right: Union[float, int]


def all(value: float) -> BorderRadius:
    return BorderRadius(
        top_left=value, top_right=value, bottom_left=value, bottom_right=value
    )


def horizontal(left: float = 0, right: float = 0) -> BorderRadius:
    return BorderRadius(
        top_left=left, top_right=right, bottom_left=left, bottom_right=right
    )


def vertical(top: float = 0, bottom: float = 0) -> BorderRadius:
    return BorderRadius(
        top_left=top, top_right=top, bottom_left=bottom, bottom_right=bottom
    )


def only(
    top_left: float = 0,
    top_right: float = 0,
    bottom_left: float = 0,
    bottom_right: float = 0,
) -> BorderRadius:
    return BorderRadius(
        top_left=top_left,
        top_right=top_right,
        bottom_left=bottom_left,
        bottom_right=bottom_right,
    )
