from typing import Optional, Union

from flet.controls.alignment import Alignment
from flet.controls.base_control import BaseControl, control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.transform import OffsetValue
from flet.controls.types import OptionalColorValue, OptionalNumber, StrOrControl

__all__ = ["Badge", "BadgeValue"]


@control("Badge")
class Badge(BaseControl):
    """
    Badges are used to show notifications, counts, or status information on navigation
    items such as NavigationBar or NavigationRail destinations
    or a button's icon.

    Online docs: https://flet.dev/docs/reference/types/badge
    """

    label: Optional[StrOrControl] = None
    """
    
    The text or Control shown on badge's label, typically a 1 to 4 characters text.

    If the label is not provided, the badge is shown as a filled circle of 
    [`small_size`](#small_size) diameter. 

    If `label` is provided, the label is a StadiumBorder shaped badge with height equal 
    to [`large_size`](#large_size).

    Value is of type `str` or `Control`.
    """

    offset: Optional[OffsetValue] = None
    """
    Combined with `alignment` to determine the location of the label relative to the 
    content.

    Has effect only used if `label` is also provided.

    Value is of type [`OffsetValue`](https://flet.dev/docs/reference/types/aliases#offsetvalue).
    """

    alignment: Optional[Alignment] = None
    """
    Aligns the label relative to the content of the badge.

    The alignment positions the label in similar way content of a container is 
    positioned using its [`alignment`](https://flet.dev/docs/controls/container#alignment), 
    except that the badge alignment is resolved as if the label was a [`large_size`](https://flet.dev/docs/reference/types/badge#large_size) 
    square and `offset` is added to the result.

    This value is only used if `label` property is provided.

    For example:

    ```python
    badge.alignment = ft.Alignment.top_left()
    ```

    Value is of type [`Alignment`](https://flet.dev/docs/reference/types/alignment).
    """

    bgcolor: OptionalColorValue = None
    """
    Background [color](https://flet.dev/docs/reference/colors) of the label.
    """

    label_visible: bool = True
    """
    If `False`, the `label` is not displayed. By default, `label_visible` is True. It 
    can be used to create a badge only shown under certain conditions.

    Value is of type `bool`.
    """

    large_size: OptionalNumber = None
    """
    The badge's label height if `label` is provided.

    If the default value is overridden then it may be useful to also override `padding` 
    and `alignment`.

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber) 
    and defaults to `16`.
    """

    padding: OptionalPaddingValue = None
    """
    The padding added to the badge's label.

    This value is only used if `text` is provided. Defaults to 4 pixels on the left and 
    right.

    Value is of type [`PaddingValue`](https://flet.dev/docs/reference/types/aliases#paddingvalue).
    """

    small_size: OptionalNumber = None
    """
    The badge's label diameter if `label` is not provided.

    Value is of type [`OptionalNumber`](https://flet.dev/docs/reference/types/aliases#optionalnumber) 
    and defaults to `6`.
    """

    text_color: OptionalColorValue = None
    """
    [Color](https://flet.dev/docs/reference/colors) of the text shown in the label. 
    This color overrides the color of the label's `text_style`.
    """

    text_style: Optional[TextStyle] = None
    """
    The text style to use for text in the label.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """


BadgeValue = Union[str, Badge]
