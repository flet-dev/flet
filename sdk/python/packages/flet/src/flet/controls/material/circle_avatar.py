from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.types import (
    OptionalColorValue,
    OptionalNumber,
    OptionalString,
    StrOrControl,
)

__all__ = ["CircleAvatar"]


@control("CircleAvatar")
class CircleAvatar(ConstrainedControl):
    """
    A circle that represents a user.

    If `foreground_image_src` fails then `background_image_src` is used. If
    `background_image_src` fails too, then `bgcolor` is used.

    Online docs: https://flet.dev/docs/controls/circleavatar
    """

    content: Optional[StrOrControl] = None
    """
    Typically a `Text` control. If the CircleAvatar is to have an image, use 
    `background_image_src` instead.
    """

    foreground_image_src: OptionalString = None
    """
    The source (local asset file or URL) of the foreground image in the circle. 
    Typically used as profile image. For fallback use `background_image_src`.
    """

    background_image_src: OptionalString = None
    """
    The source (local asset file or URL) of the background image in the circle. 
    Changing the background image will cause the avatar to animate to the new image. 
    Typically used as a fallback image for `foreground_image_src`. If the CircleAvatar 
    is to have the user's initials, use `content` instead.
    """

    color: OptionalColorValue = None
    """
    The default text [color](https://flet.dev/docs/reference/colors) for text in the 
    circle. Defaults to the primary text theme color if no `bgcolor` is specified.
    """

    bgcolor: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) with which to fill the circle. 
    Changing the background color will cause the avatar to animate to the new color.
    """

    radius: OptionalNumber = None
    """
    The size of the avatar, expressed as the radius (half the diameter). If radius is 
    specified, then neither minRadius nor maxRadius may be specified.
    """

    min_radius: OptionalNumber = None
    """
    The minimum size of the avatar, expressed as the radius (half the diameter). If 
    minRadius is specified, then radius must not also be specified. Defaults to zero.
    """

    max_radius: OptionalNumber = None
    """
    The maximum size of the avatar, expressed as the radius (half the diameter). If 
    maxRadius is specified, then radius must not also be specified. Defaults to 
    "infinity".
    """

    on_image_error: OptionalControlEventHandler["CircleAvatar"] = None
    """
    Fires when an error occurs while loading the `background_image_src` or 
    `foreground_image_src`.

    The event data (`e.data`) is a string whose value is either `"background"` or 
    `"foreground"` indicating the error's origin.
    """

    def before_update(self):
        super().before_update()
        assert self.radius is None or self.radius >= 0, "radius cannot be negative"
        assert self.min_radius is None or self.min_radius >= 0, (
            "min_radius cannot be negative"
        )
        assert self.max_radius is None or self.max_radius >= 0, (
            "max_radius cannot be negative"
        )
        assert self.radius is None or (
            self.min_radius is None and self.max_radius is None
        ), "If radius is set, min_radius and max_radius must be None"
