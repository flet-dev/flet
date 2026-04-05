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
    Badges are used to show notifications, counts, or status information on navigation \
    items such as :class:`~flet.NavigationBar` or :class:`~flet.NavigationRail` \
    destinations or a button's icon.

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
    :attr:`small_size` diameter.

    If `label` is provided, it is a :class:`~flet.StadiumBorder` shaped
    badge with height equal to :attr:`large_size`.
    """

    offset: Optional[OffsetValue] = None
    """
    Combined with `alignment` to determine the location of the :attr:`label` relative \
    to the content.

    Note:
        Has effect only used if :attr:`label` is also provided.
    """

    alignment: Optional[Alignment] = None
    """
    Aligns the :attr:`~flet.Badge.label` relative to the content of the badge.

    The alignment positions the :attr:`label` in similar way
    :attr:`flet.Container.content` is positioned using :attr:`flet.Container.alignment`,
    except that the badge alignment is resolved as if the `label` was a
    :attr:`large_size` square and :attr:`offset` is added to the result.

    Note:
        Has effect only used if :attr:`label` is also provided.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of the :attr:`label`.
    """

    label_visible: bool = True
    """
    Whether the :attr:`label` should be visible.

    It can be used to create a badge only shown under certain conditions.
    """

    large_size: Optional[Number] = None
    """
    The badge's label height if :attr:`label` is provided.

    If the default value is overridden then it may be useful to also override
    :attr:`padding` and :attr:`alignment`.

    Defaults to :attr:`flet.BadgeTheme.large_size`, or if that is `None`,
    falls back to `16`.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding added to the :attr:`label`.

    Defaults to :attr:`flet.BadgeTheme.padding`, or if that is `None`,
    falls back to `4` pixels on the left and right.

    Note:
        Has effect only if :attr:`label` is not `None`.
    """

    small_size: Optional[Number] = None
    """
    The badge's label diameter if :attr:`label` is not provided.

    Defaults to :attr:`flet.BadgeTheme.small_size`, or if that is `None`,
    falls back to `6`.
    """

    text_color: Optional[ColorValue] = None
    """
    The color of the text shown in the :attr:`label`.

    It overrides the color of the :attr:`label`'s :attr:`text_style`.
    """

    text_style: Optional[TextStyle] = None
    """
    The text style to use for text in the :attr:`label`.
    """


BadgeValue = Union[str, Badge]
"""Type alias for badge content values.

Represents a badge as either:
- a `str` value, rendered as a text label badge,
- or a :class:`~flet.Badge`.
"""
