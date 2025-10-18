from typing import Optional

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

__all__ = ["Chip"]


@control("Chip")
class Chip(LayoutControl):
    """
    Chips are compact elements that represent an attribute, text, entity, or action.

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

    Typically a [`Text`][flet.] control.
    """

    leading: Optional[Control] = None
    """
    A `Control` to display to the left of this chip's [`label`][(c).].

    Typically the leading control is an [`Icon`][flet.] or a [`CircleAvatar`][flet.].
    """

    selected: bool = False
    """
    If [`on_select`][(c).] event is specified, `selected` property is used to
    determine whether this chip is selected or not.
    """

    selected_color: Optional[ColorValue] = None
    """
    The color used for this chip's background when it is selected.
    """

    elevation: Optional[Number] = None
    """
    A non-negative value which defines the size of the shadow below this chip.

    Defaults to `0`.

    Raises:
        ValueError: If [`elevation`][(c).] is negative.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Color to be used for the unselected, enabled chip's background.
    """

    show_checkmark: bool = True
    """
    If [`on_select`][(c).] event is specified and chip is selected, `show_checkmark`
    is used to determine whether or not to show a checkmark.
    """

    check_color: Optional[ColorValue] = None
    """
    The color of this chip's check mark when a check mark is visible.
    """

    shadow_color: Optional[ColorValue] = None
    """
    The color used for this chip's background
    when the elevation is greater than `0` and this chip is not selected.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the border around this chip.

    Defaults to [`ChipTheme.shape`][flet.], or if that is resolves to
    `None`, falls back to `RoundedRectangleBorder(radius=8)`.
    """

    padding: Optional[PaddingValue] = None
    """
    The padding between the [`label`][(c).] and the outside shape.

    Defaults to `8` logical pixels on all sides.
    """

    delete_icon: Optional[Control] = None
    """
    A `Control` to display to the right of this chip's [`label`][(c).]
    in case [`on_delete`][(c).] event is specified.
    """

    delete_icon_tooltip: Optional[str] = None
    """
    The text to be used for this chip's `delete_icon` tooltip. If not provided or
    provided with an empty string, the tooltip of the delete icon will not be displayed.
    """

    delete_icon_color: Optional[ColorValue] = None
    """
    The color of the [`delete_icon`][(c).].
    """

    disabled_color: Optional[ColorValue] = None
    """
    The color used for this chip's background if it is disabled.
    """

    label_padding: Optional[PaddingValue] = None
    """
    The padding around the [`label`][(c).].

    By default, this is `4` logical pixels at the beginning and the end of
    the [`label`][(c).], and zero on `top` and `bottom`.
    """

    label_text_style: Optional[TextStyle] = None
    """
    The style to be applied to this chip's [`label`][(c).].
    """

    selected_shadow_color: Optional[ColorValue] = None
    """
    The color used for this chip's background
    when the elevation is greater than `0` and this chip is selected.
    """

    autofocus: bool = False
    """
    Whether this chip will be selected as the initial focus.

    If there is more than one control on a page with autofocus set,
    then the first one added to the page will get focus.
    """

    color: Optional[ControlStateValue[ColorValue]] = None
    """
    The color that fills this chip in various [`ControlState`][flet.].
    """

    elevation_on_click: Optional[Number] = None
    """
    The elevation to be applied on this chip relative to its parent during the press
    motion. This controls the size of the shadow below this chip.

    Defaults to `8.0`.

    Raises:
        ValueError: If it is less than `0.0`.
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
    The size constraints for the [`leading`][(c).] control.

    If `None`, it defaults to a minimum size of chip height or label height
    (whichever is greater) and a padding of `8.0` pixels on all sides.
    """

    delete_icon_size_constraints: Optional[BoxConstraints] = None
    """
    The size constraints for the [`delete_icon`][(c).] control.

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
    The animation style for the [`leading`][(c).] control's animations.
    """

    delete_drawer_animation_style: Optional[AnimationStyle] = None
    """
    The animation style for the [`delete_icon`][(c).]'s animations.
    """

    on_click: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when the user clicks on this chip.

    Raises:
        ValueError: If specified together with [`on_select`][(c).].
    """

    on_delete: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when the user clicks on the [`delete_icon`][(c).].
    """

    on_select: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when the user clicks on this chip.

    It internally changes [`selected`][(c).] property to the opposite value.

    Raises:
        ValueError: If specified together with [`on_click`][(c).].
    """

    on_focus: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when this chip has received focus.
    """

    on_blur: Optional[ControlEventHandler["Chip"]] = None
    """
    Called when this chip has lost focus.
    """

    def before_update(self):
        super().before_update()
        if self.on_select is not None and self.on_click is not None:
            raise ValueError("on_select and on_click cannot be used together")
        if self.elevation is not None and self.elevation < 0.0:
            raise ValueError(
                f"elevation must be greater than or equal to 0, got {self.elevation}"
            )
        if self.elevation_on_click is not None and self.elevation_on_click < 0.0:
            raise ValueError(
                "elevation_on_click must be greater than or equal to 0, got "
                f"{self.elevation_on_click}"
            )
