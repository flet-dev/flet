from typing import Annotated, Optional, Union

from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ColorValue,
    Number,
    StrOrControl,
)
from flet.utils.validation import V, ValidationRules

__all__ = ["CircleAvatar"]


@control("CircleAvatar")
class CircleAvatar(LayoutControl):
    """
    A circle that represents a user.

    If [`foreground_image_src`][(c).] fails then [`background_image_src`][(c).] is used,
    and if this also fails, then [`bgcolor`][(c).] is used.

    Example:
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

    radius: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The size of the avatar, expressed as the radius (half the diameter).

    If set to a non `None` value, then neither [`min_radius`][(c).] nor
    [`max_radius`][(c).] may be specified.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
        ValueError: If it is set while [`min_radius`][(c).]
            or [`max_radius`][(c).] is set.
    """

    min_radius: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The minimum size of the avatar, expressed as the radius (half the diameter).
    If set to a non `None` value, then [`radius`][(c).] must be `None` (default).

    Defaults to `0.0`.

    Raises:
        ValueError: If it is not greater than or equal to `0.0`.
        ValueError: If it is set while [`radius`][(c).] is set.
    """

    max_radius: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The maximum size of the avatar, expressed as the radius (half the diameter).
    If set to a non `None` value, then [`radius`][(c).] must be `None` (default).

    Defaults to `float('inf')` i.e. infinity.

    Raises:
        ValueError: If it is not greater than or equal to `0.0`.
        ValueError: If it is set while [`radius`][(c).] is set.
    """

    on_image_error: Optional[ControlEventHandler["CircleAvatar"]] = None
    """
    Called when an error occurs while loading the [`background_image_src`][(c).] or \
    [`foreground_image_src`][(c).].

    The [`data`][flet.Event.] property of the event handler argument is
    a string whose value is either `"background"` or `"foreground"`
    indicating the error's origin.
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda ctrl: ctrl.radius is None
            or (ctrl.min_radius is None and ctrl.max_radius is None),
            message="if radius is set, min_radius and max_radius must be None",
        ),
    )
