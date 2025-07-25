from dataclasses import field

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint

__all__ = ["Fill"]


@control("Fill")
class Fill(Shape):
    """
    Fills the canvas with the given [`paint`][(c).].

    To fill the canvas with a solid color and blend mode,
    consider [`Color`][(p).color.] shape instead.
    """

    paint: Paint = field(default_factory=lambda: Paint())
    """
    A style to fill the canvas with.
    """
