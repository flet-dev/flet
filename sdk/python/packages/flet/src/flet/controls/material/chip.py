from typing import Annotated, Optional

from flet.controls.animation import AnimationStyle
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.box import BoxConstraints
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_event import ControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    Number,
    StrOrControl,
    VisualDensity,
)
from flet.utils.validation import V, ValidationRules

__all__ = ["Chip"]


@control("Chip")
class Chip(LayoutControl):
    """
    Chips are compact elements that represent an attribute, text, entity, or action.

    Example:
    ```python
    ft.Chip(
        label="Explore topics",
        leading=ft.Icon(ft.Icons.EXPLORE_OUTLINED),
    )
    ```
    """

    label: StrOrControl
    """
    The primary content of this chip.

    Typically a :class:`~flet.Text` control.
    """

    leading: Optional[Control] = None
    """
    A `Control` to display to the left of this chip's :attr:`label`.

    Typically the leading control is an :class:`~flet.Icon` or a \
    :class:`~flet.CircleAvatar`.
    """

    selected: bool = False
    """
    If :attr:`on_select` event is specified, `selected` property is used to determine \
    whether this chip is selected or not.
    """

    selected_color: Optional[ColorValue] = None
    """
    The color used for this chip's background when it is selected.
    """

    elevation: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    A non-negative value which defines the size of the shadow below this chip.

    Defaults to `0`.

    Raises:
        ValueError: If :attr:`elevation` is negative.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color to be used for the unselected, enabled chip's background.
    """

    show_checkmark: bool = True
    """
    If :attr:`on_select` event is specified and chip is selected, `show_checkmark` is \
    used to determine whether or not to show a checkmark.
    """

    check_color: Optional[ColorValue] = None
    """
    The color of this chip's check mark when a check mark is visible.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color used for this chip's background when the elevation is greater than `0` \
    and this chip is not selected.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the border around this chip.

    Defaults to :attr:`flet.ChipTheme.shape`, or if that is resolves to
    `None`, falls back to `RoundedRectangleBorder(radius=8)`.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding between the :attr:`label` and the outside shape.

    Defaults to `8` logical pixels on all sides.
    """

    delete_icon: Optional[Control] = None
    """
    A `Control` to display to the right of this chip's :attr:`label`
    in case :attr:`on_delete` event is specified.
    """

    delete_icon_tooltip: Optional[str] = None
    """
    The text to be used for this chip's `delete_icon` tooltip. If not provided or \
    provided with an empty string, the tooltip of the delete icon will not be \
    displayed.
    """

    delete_icon_color: Optional[ColorValue] = None
    """
    The color of the :attr:`delete_icon`.
    """

    disabled_color: Optional[ColorValue] = None
    """
    The color used for this chip's background if it is disabled.
    """

    label_padding: Optional[PaddingValue] = None
    """
    The padding around the :attr:`label`.

    By default, this is `4` logical pixels at the beginning and the end of
    the :attr:`label`, and zero on `top` and `bottom`.
    """

    label_text_style: Optional[TextStyle] = None
    """
    The style to be applied to this chip's :attr:`label`.
    """

    selected_shadow_color: Optional[ColorValue] = None
    """
    The color used for this chip's background when the elevation is greater than `0` \
    and this chip is selected.
    """

    autofocus: bool = False
    """
    Whether this chip will be selected as the initial focus.

    If there is more than one control on a page with autofocus set,
    then the first one added to the page will get focus.
    """

    color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color that fills this chip in various :class:`~flet.ControlState`.
    """

    elevation_on_click: Annotated[
        Optional[Number],
        V.ge(0),
    ] = None
    """
    The elevation to be applied on this chip relative to its parent during the press \
    motion. This controls the size of the shadow below this chip.

    Defaults to `8.0`.

    Raises:
        ValueError: If it is not greater than or equal to `0.0`.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The content will be clipped (or not) according to this option.
    """

    visual_density: Optional[VisualDensity] = None
    """
    TBD
    """

    border_side: Optional[BorderSide] = None
    """
    Defines the color and weight of this chip's outline.
    """

    leading_size_constraints: Optional[BoxConstraints] = None
    """
    The size constraints for the :attr:`leading` control.

    If `None`, it defaults to a minimum size of chip height or label height
    (whichever is greater) and a padding of `8.0` pixels on all sides.
    """

    delete_icon_size_constraints: Optional[BoxConstraints] = None
    """
    The size constraints for the :attr:`delete_icon` control.

    If `None`, it defaults to a minimum size of chip height or label height
    (whichever is greater) and a padding of 8.0 pixels on all sides.
    """

    enable_animation_style: Optional[AnimationStyle] = None
    """
    The animation style for the enable and disable animations.
    """

    select_animation_style: Optional[AnimationStyle] = None
    """
    The animation style for the select and unselect animations.
    """

    leading_drawer_animation_style: Optional[AnimationStyle] = None
    """
    The animation style for the :attr:`leading` control's animations.
    """

    delete_drawer_animation_style: Optional[AnimationStyle] = None
    """
    The animation style for the :attr:`delete_icon`'s animations.
    """

    on_click: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when the user clicks on this chip.

    Raises:
        ValueError: If specified together with :attr:`on_select`.
    """

    on_delete: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when the user clicks on the :attr:`delete_icon`.
    """

    on_select: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when the user clicks on this chip.

    It internally changes :attr:`selected` property to the opposite value.

    Raises:
        ValueError: If specified together with :attr:`on_click`.
    """

    on_focus: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when this chip has received focus.
    """

    on_blur: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when this chip has lost focus.
    """

    __validation_rules__: ValidationRules = (
        V.ensure(
            lambda ctrl: ctrl.on_select is None or ctrl.on_click is None,
            message="on_select and on_click cannot be used together",
        ),
    )
