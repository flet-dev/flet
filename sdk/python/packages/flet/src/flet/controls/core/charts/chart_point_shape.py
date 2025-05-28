from dataclasses import dataclass

from flet.controls.types import Number, OptionalColorValue, OptionalNumber


@dataclass(kw_only=True)
class ChartPointShape:
    type: str = ""


@dataclass
class ChartCirclePoint(ChartPointShape):
    color: OptionalColorValue = None
    """
    The fill [color](https://flet.dev/docs/reference/colors) to use for the circle.
    """

    radius: OptionalNumber = None
    """
    The radius of the circle.
    """

    stroke_color: OptionalColorValue = None
    """
    The stroke [color](https://flet.dev/docs/reference/colors) to use for the circle
    """

    stroke_width: Number = 0
    """
    The stroke width to use for the circle.

    Defaults to `1.0`.
    """

    def __post_init__(self):
        self.type = "circle"


@dataclass
class ChartSquarePoint(ChartPointShape):
    color: OptionalColorValue = None
    """
    The fill [color](https://flet.dev/docs/reference/colors) to use for the square.
    """

    size: Number = 4.0
    """
    The size of the square.

    Defaults to `4.0`.
    """

    stroke_color: OptionalColorValue = None
    """
    The stroke [color](https://flet.dev/docs/reference/colors) to use for the square.
    """

    stroke_width: Number = 1.0
    """
    The stroke width to use for the square.

    Defaults to `1.0`.
    """

    def __post_init__(self):
        self.type = "square"


@dataclass
class ChartCrossPoint(ChartPointShape):
    color: OptionalColorValue = None
    """
    The fill [color](https://flet.dev/docs/reference/colors) to use for the cross-mark(X).
    """

    size: Number = 8.0
    """
    The size of the cross-mark.

    Defaults to `8.0`.
    """

    width: Number = 2.0
    """
    The thickness of the cross-mark.

    Defaults to `2.0`.
    """

    def __post_init__(self):
        self.type = "cross"

