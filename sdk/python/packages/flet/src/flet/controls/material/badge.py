from typing import Optional, Union

from flet.controls.alignment import Alignment
from flet.controls.base_control import BaseControl, control
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.transform import OffsetValue
from flet.controls.types import ColorValue, Number, StrOrControl

__all__ = ["Badge", "BadgeValue"]


@control("Badge")
class Badge(BaseControl):
    """
    Badges are used to show notifications, counts, or status information on navigation
    items such as [`NavigationBar`][flet.] or [`NavigationRail`][flet.] destinations
    or a button's icon.

    ```python
    ft.FilledIconButton(
        icon=ft.Icons.PHONE,
        badge=ft.Badge(label="3"),
    )
    ```
    """

    label: Optional[StrOrControl] = None
    """
    The label of this badge.

    Typically a `1` to `4` characters text.

    If the label is not provided, the badge is shown as a filled circle of
    [`small_size`][(c).] diameter.

    If `label` is provided, it is a [`StadiumBorder`][flet.] shaped
    badge with height equal to [`large_size`][(c).].
    """

    offset: Optional[OffsetValue] = None
    """
    Combined with `alignment` to determine the location of the
    [`label`][(c).] relative to the content.

    Note:
        Has effect only used if [`label`][(c).] is also provided.
    """

    alignment: Optional[Alignment] = None
    """
    Aligns the [`label][flet.Badge.label] relative to the content of the badge.

    The alignment positions the [`label`][(c).] in similar way
    [`Container.content`][flet.] is positioned using [`Container.alignment`][flet.],
    except that the badge alignment is resolved as if the `label` was a
    [`large_size`][(c).] square and [`offset`][(c).] is added to the result.

    Note:
        Has effect only used if [`label`][(c).] is also provided.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of the [`label`][(c).].
    """

    label_visible: bool = True
    """
    Whether the [`label`][(c).] should be visible.

    It can be used to create a badge only shown under certain conditions.
    """

    large_size: Optional[Number] = None
    """
    The badge's label height if [`label`][(c).] is provided.

    If the default value is overridden then it may be useful to also override
    [`padding`][(c).] and [`alignment`][(c).].

    Defaults to [`BadgeTheme.large_size`][flet.], or if that is `None`,
    falls back to `16`.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding added to the [`label`][(c).].

    Defaults to [`BadgeTheme.padding`][flet.], or if that is `None`,
    falls back to `4` pixels on the left and right.

    Note:
        Has effect only if [`label`][(c).] is not `None`.
    """

    small_size: Optional[Number] = None
    """
    The badge's label diameter if [`label`][(c).] is not provided.

    Defaults to [`BadgeTheme.small_size`][flet.], or if that is `None`,
    falls back to `6`.
    """

    text_color: Optional[ColorValue] = None
    """
    The color of the text shown in the [`label`][(c).].

    It overrides the color of the [`label`][(c).]'s [`text_style`][(c).].
    """

    text_style: Optional[TextStyle] = None
    """
    The text style to use for text in the [`label`][(c).].
    """


BadgeValue = Union[str, Badge]
