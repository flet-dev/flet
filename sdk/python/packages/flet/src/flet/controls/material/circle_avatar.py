from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.types import (
    ColorValue,
    Number,
    StrOrControl,
)

__all__ = ["CircleAvatar"]


@control("CircleAvatar")
class CircleAvatar(ConstrainedControl):
    """
    A circle that represents a user.

    If [`foreground_image_src`][(c).] fails then [`background_image_src`][(c).] is used,
    and if this also fails, then [`bgcolor`][(c).] is used.

    Raises:
        AssertionError: If [`radius`][(c).] or [`min_radius`][(c).] or [`max_radius`][(c).] is negative.
        AssertionError: If [`radius`][(c).] is set and [`min_radius`][(c).] or [`max_radius`][(c).] is not None.
    """

    content: Optional[StrOrControl] = None
    """
    The content of this avatar.
    
    Typically a [`Text`][flet.Text] control. 
    
    If this avatar is to have an image, use
    [`background_image_src`][flet.CircleAvatar.background_image_src] instead.
    """

    foreground_image_src: Optional[str] = None
    """
    The source (local asset file or URL) of the foreground image in the circle.
    
    Fallbacks to [`background_image_src`][flet.CircleAvatar.background_image_src].
    
    Typically used as profile image. 
    """

    background_image_src: Optional[str] = None
    """
    The source (local asset file or URL) of the background image in the circle.
    Changing the background image will cause the avatar to animate to the new image.
    
    Typically used as a fallback image for [`foreground_image_src`][flet.CircleAvatar.foreground_image_src]. 
    If this avatar is to have the user's initials, use [`content`][flet.CircleAvatar.content] instead.
    """

    color: Optional[ColorValue] = None
    """
    The default color for text in this avatar. 
    
    Defaults to the primary text theme color if no `bgcolor` is specified.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color with which to fill the circle.
    
    Changing the background color will cause this avatar to animate to the new color.
    """

    radius: Optional[Number] = None
    """
    The size of the avatar, expressed as the radius (half the diameter). If `radius` is
    specified, then neither [`min_radius`][flet.CircleAvatar.min_radius] nor 
    [`max_radius`][flet.CircleAvatar.max_radius] may be specified.
    """

    min_radius: Optional[Number] = None
    """
    The minimum size of the avatar, expressed as the radius (half the diameter). If
    `min_radius` is specified, then [`radius`][flet.CircleAvatar.radius] should not be specified.
    
    Defaults to `0.0`.
    """

    max_radius: Optional[Number] = None
    """
    The maximum size of the avatar, expressed as the radius (half the diameter). 
    
    If `max_radius` is specified, then [`radius`][flet.CircleAvatar.radius] should not be specified. 
    
    Defaults to "infinity".
    """

    on_image_error: Optional[ControlEventHandler["CircleAvatar"]] = None
    """
    Called when an error occurs while loading the [`background_image_src`][flet.CircleAvatar.background_image_src] or
    [`foreground_image_src`][flet.CircleAvatar.foreground_image_src].

    The [`data`][flet.Event.data] property of the event handler argument is a string whose value is 
    either `"background"` or `"foreground"` indicating the error's origin.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.radius is None or self.radius >= 0
        ), f"radius must be greater than or equal to 0, got {self.radius}"
        assert (
            self.min_radius is None or self.min_radius >= 0
        ), f"min_radius must be greater than or equal to 0, got {self.min_radius}"
        assert (
            self.max_radius is None or self.max_radius >= 0
        ), f"max_radius must be greater than or equal to 0, got {self.max_radius}"
        assert self.radius is None or (
            self.min_radius is None and self.max_radius is None
        ), "If radius is set, min_radius and max_radius must be None"
