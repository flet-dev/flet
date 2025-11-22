from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
    Number,
    StrOrControl,
)

__all__ = ["CircleAvatar"]


@control("CircleAvatar")
class CircleAvatar(LayoutControl):
    """
    A circle that represents a user.

    If [`foreground_image_src`][(c).] fails then [`background_image_src`][(c).] is used,
    and if this also fails, then [`bgcolor`][(c).] is used.

    ```python
    ft.CircleAvatar(
        content=ft.Text("AB"),
        bgcolor=ft.Colors.PRIMARY,
        color=ft.Colors.ON_PRIMARY,
    )
    ```
    """

    content: Optional[StrOrControl] = None
    """
    The content of this avatar.

    Typically a [`Text`][flet.] control.

    Tip:
        If this avatar is to have an image, use [`background_image_src`][(c).] instead.
    """

    foreground_image_src: Optional[Union[str, bytes]] = None
    """
    The source (local asset file or URL) of the foreground image in the circle.

    Fallbacks to [`background_image_src`][(c).].

    Typically used as profile image.
    """

    background_image_src: Optional[Union[str, bytes]] = None
    """
    The source (local asset file or URL) of the background image in the circle.
    Changing the background image will cause the avatar to animate to the new image.

    If this avatar is to have the user's initials, use [`content`][(c).] instead.

    Typically used as a fallback image for [`foreground_image_src`][(c).].
    """

    color: Optional[ColorValue] = None
    """
    The default color for text in this avatar.

    Defaults to the primary text theme color if no [`bgcolor`][(c).] is specified.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The color with which to fill the circle.

    Changing the background color will cause this avatar to animate to the new color.
    """

    radius: Optional[Number] = None
    """
    The size of the avatar, expressed as the radius (half the diameter). If `radius` is
    specified, then neither [`min_radius`][(c).] nor
    [`max_radius`][(c).] may be specified.

    Raises:
        ValueError: If it is less than `0.0` or if it is
            provided while [`min_radius`][(c).] or [`max_radius`][(c).] is set.
    """

    min_radius: Optional[Number] = None
    """
    The minimum size of the avatar, expressed as the radius (half the diameter). If
    `min_radius` is specified, then [`radius`][(c).] should not be specified.

    Defaults to `0.0`.

    Raises:
        ValueError: If it is negative.
    """

    max_radius: Optional[Number] = None
    """
    The maximum size of the avatar, expressed as the radius (half the diameter).

    Defaults to "infinity".

    Note:
        If `max_radius` is specified, then [`radius`][(c).] should not be specified.

    Raises:
        ValueError: If it is less than `0.0` or if it is
            provided while [`radius`][(c).] is set.
    """

    on_image_error: Optional[ControlEventHandler["CircleAvatar"]] = None
    """
    Called when an error occurs while loading the [`background_image_src`][(c).] or
    [`foreground_image_src`][(c).].

    The [`data`][flet.Event.] property of the event handler argument is
    a string whose value is either `"background"` or `"foreground"`
    indicating the error's origin.
    """

    def before_update(self):
        super().before_update()
        if self.radius is not None and self.radius < 0:
            raise ValueError(
                f"radius must be greater than or equal to 0, got {self.radius}"
            )
        if self.min_radius is not None and self.min_radius < 0:
            raise ValueError(
                f"min_radius must be greater than or equal to 0, got {self.min_radius}"
            )
        if self.max_radius is not None and self.max_radius < 0:
            raise ValueError(
                f"max_radius must be greater than or equal to 0, got {self.max_radius}"
            )
        if self.radius is not None and not (
            self.min_radius is None and self.max_radius is None
        ):
            raise ValueError("If radius is set, min_radius and max_radius must be None")
