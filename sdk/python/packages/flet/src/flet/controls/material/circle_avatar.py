from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.types import (
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
    OptionalString,
)

__all__ = ["CircleAvatar"]


@control("CircleAvatar")
class CircleAvatar(ConstrainedControl):
    """
    A circle that represents a user.

    If `foreground_image_src` fails then `background_image_src` is used. If `background_image_src` fails too,
    then `bgcolor` is used.

    Online docs: https://flet.dev/docs/controls/circleavatar
    """

    content: Optional[Control] = None
    foreground_image_src: OptionalString = None
    background_image_src: OptionalString = None
    color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    radius: OptionalNumber = None
    min_radius: OptionalNumber = None
    max_radius: OptionalNumber = None
    on_image_error: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert self.radius is None or self.radius >= 0, "radius cannot be negative"
        assert (
            self.min_radius is None or self.min_radius >= 0
        ), "min_radius cannot be negative"
        assert (
            self.max_radius is None or self.max_radius >= 0
        ), "max_radius cannot be negative"
        assert self.radius is None or (
            self.min_radius is None and self.max_radius is None
        ), "If radius is set, min_radius and max_radius must be None"
