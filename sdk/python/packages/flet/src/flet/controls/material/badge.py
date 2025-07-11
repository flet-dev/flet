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
    items such as [`NavigationBar`][flet.NavigationBar] or
    [`NavigationRail`][flet.NavigationRail] destinations or a button's icon.
    """

    label: Optional[StrOrControl] = None
    """
    The label of this badge.

    Typically a 1 to 4 characters text.

    If the label is not provided, the badge is shown as a filled circle of
    [`small_size`][flet.Badge.small_size] diameter.

    If `label` is provided, the label is a `StadiumBorder` shaped badge with height equal
    to [`large_size`][flet.Badge.large_size].
    """

    offset: Optional[OffsetValue] = None
    """
    Combined with `alignment` to determine the location of the
    [`label`][flet.Badge.label] relative to the content.

    Has effect only used if [`label`][flet.Badge.label] is also provided.
    """

    alignment: Optional[Alignment] = None
    """
    Aligns the [`label][flet.Badge.label] relative to the content of the badge.

    The alignment positions the label in similar way [`Container.content`][flet.Container.content] is
    positioned using [`Container.alignment`][flet.Container.alignment],
    except that the badge alignment is resolved as if the label was a [`large_size`][flet.Badge.large_size]
    square and [`offset`][flet.Badge.offset] is added to the result.

    Has effect only used if [`label`][flet.Badge.label] is also provided.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of the [`label`][flet.Badge.label].
    """

    label_visible: bool = True
    """
    Whether the [`label`][flet.Badge.label] should be visible.

    It can be used to create a badge only shown under certain conditions.
    """

    large_size: Optional[Number] = None
    """
    The badge's label height if [`label`][flet.Badge.label] is provided.

    If the default value is overridden then it may be useful to also override `padding`
    and `alignment`.

    Defaults to [`BadgeTheme.large_size`][flet.BadgeTheme.large_size], or if that is `None`,
    falls back to `16`.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding added to the [`label`][flet.Badge.label].

    Has effect only if `label` is not `None`.

    Defaults to [`BadgeTheme.padding`][flet.BadgeTheme.padding], or if that is `None`,
    falls back to `4` pixels on the left and right.
    """

    small_size: Optional[Number] = None
    """
    The badge's label diameter if [`label`][flet.Badge.label] is not provided.

    Defaults to [`BadgeTheme.small_size`][flet.BadgeTheme.small_size], or if that is `None`,
    falls back to `6`.
    """

    text_color: Optional[ColorValue] = None
    """
    The color of the text shown in the label.
    This color overrides the color of the [`label`][flet.Badge.label]'s `text_style`.
    """

    text_style: Optional[TextStyle] = None
    """
    The text style to use for text in the [`label`][flet.Badge.label].
    """


BadgeValue = Union[str, Badge]
