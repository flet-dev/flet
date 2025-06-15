from typing import Optional

from flet.controls.animation import AnimationStyle
from flet.controls.base_control import control
from flet.controls.border import BorderSide
from flet.controls.box import BoxConstraints
from flet.controls.buttons import OutlinedBorder
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.control_state import ControlStateValue
from flet.controls.padding import OptionalPaddingValue
from flet.controls.text_style import TextStyle
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
    VisualDensity,
)

__all__ = ["Chip"]


@control("Chip")
class Chip(ConstrainedControl):
    """
    Chips are compact elements that represent an attribute, text, entity, or action.

    Online docs: https://flet.dev/docs/controls/chip
    """

    label: StrOrControl
    """
    A `Control` that represents primary content of the chip, typically a [`Text`](https://flet.dev/docs/controls/text). 
    Label is a required property.
    """

    leading: Optional[Control] = None
    """
    A `Control` to display to the left of the chip's `label`.

    Typically the leading control is an [`Icon`](https://flet.dev/docs/controls/icon) 
    or a [`CircleAvatar`](https://flet.dev/docs/controls/circleavatar).
    """

    selected: bool = False
    """
    If `on_select` event is specified, `selected` property is used to determine whether 
    the chip is selected or not.

    Defaults to `False`.
    """

    selected_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used for the chip's background 
    when it is selected.
    """

    elevation: OptionalNumber = None
    """
    A non-negative value which defines the size of the shadow below the chip.

    Defaults to `0`.
    """

    bgcolor: OptionalColorValue = None
    """
    [Color](https://flet.dev/docs/reference/colors) to be used for the unselected, 
    enabled chip's background.
    """

    show_checkmark: bool = True
    """
    If `on_select` event is specified and chip is selected, `show_checkmark` is used to 
    determine whether or not to show a checkmark.

    Defaults to `True`.
    """

    check_color: OptionalColorValue = None
    """
    [Color](https://flet.dev/docs/reference/colors) of the chip's check mark when a 
    check mark is visible.
    """

    shadow_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used for the chip's background 
    when the elevation is greater than `0` and the chip is not selected.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the border around the chip.

    The value is an instance of [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder) 
    class.

    The default shape is a `StadiumBorder`.
    """

    padding: OptionalPaddingValue = None
    """
    The padding between the `label` and the outside shape.

    The value is an instance of [`Padding`](https://flet.dev/docs/reference/types/padding) 
    class or a number.

    By default, this is 4 logical pixels on all sides.
    """

    delete_icon: Optional[Control] = None
    """
    A `Control` to display to the right of the chip's `label` in case `on_delete` event 
    is specified.
    """

    delete_icon_tooltip: Optional[str] = None
    """
    The text to be used for the chip's `delete_icon` tooltip. If not provided or 
    provided with an empty string, the tooltip of the delete icon will not be displayed.
    """

    delete_icon_color: OptionalColorValue = None
    """
    [Color](https://flet.dev/docs/reference/colors) of the `delete_icon`.
    """

    disabled_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used for the chip's background 
    if it is disabled.
    """

    label_padding: OptionalPaddingValue = None
    """
    Padding around the `label`.

    The value is an instance of [`padding.Padding`](https://flet.dev/docs/reference/types/padding) 
    class or a number.

    By default, this is 4 logical pixels at the beginning and the end of the label, and 
    zero on top and bottom.
    """

    label_style: Optional[TextStyle] = None
    """
    The style to be applied to the chip's `label`.

    Value is of type [`TextStyle`](https://flet.dev/docs/reference/types/textstyle).
    """

    selected_shadow_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used for the chip's background 
    when the elevation is greater than `0` and the chip is selected.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus. If there is more than 
    one control on a page with autofocus set, then the first one added to the page will 
    get focus.
    """

    surface_tint_color: OptionalColorValue = None
    """
    The [color](https://flet.dev/docs/reference/colors) used as an overlay on `bgcolor` 
    to indicate elevation.
    """

    color: Optional[ControlStateValue[ColorValue]] = None
    """
    The [color](https://flet.dev/docs/reference/colors) that fills the chip in various [`ControlState`](https://flet.dev/docs/reference/types/controlstate)s.
    """

    click_elevation: OptionalNumber = None
    """
    A non-negative value which defines the elevation of the chip when clicked/pressed.

    Defaults to `8.0`.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The content will be clipped (or not) according to this option.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) 
    and defaults to `ClipBehavior.NONE`.
    """

    visual_density: Optional[VisualDensity] = None
    """
    TBD
    """

    border_side: Optional[BorderSide] = None
    """
    Defines the color and weight of the chip's outline.

    Value is of type [`BorderSide`](https://flet.dev/docs/reference/types/borderside).
    """

    leading_size_constraints: Optional[BoxConstraints] = None
    """
    The size constraints for the `leading` control. 

    When unspecified, it defaults to a minimum size of chip height or label height 
    (whichever is greater) and a padding of 8.0 pixels on all sides.

    Value is of type [`BoxConstraints`](https://flet.dev/docs/reference/types/boxconstraints).
    """

    delete_icon_size_constraints: Optional[BoxConstraints] = None
    """
    The size constraints for the `delete_icon` control. 

    When unspecified, it defaults to a minimum size of chip height or label height 
    (whichever is greater) and a padding of 8.0 pixels on all sides.

    Value is of type [`BoxConstraints`](https://flet.dev/docs/reference/types/boxconstraints).
    """

    enable_animation_style: Optional[AnimationStyle] = None
    """
    The animation style for the enable and disable animations.

    Value is of type [`AnimationStyle`](https://flet.dev/docs/reference/types/animationstyle).
    """

    select_animation_style: Optional[AnimationStyle] = None
    """
    The animation style for the select and unselect animations.

    Value is of type [`AnimationStyle`](https://flet.dev/docs/reference/types/animationstyle).
    """

    leading_drawer_animation_style: Optional[AnimationStyle] = None
    """
    The animation style for the `leading` control's animations.

    Value is of type [`AnimationStyle`](https://flet.dev/docs/reference/types/animationstyle).
    """

    delete_drawer_animation_style: Optional[AnimationStyle] = None
    """
    The animation style for the `delete_icon`'s animations.

    Value is of type [`AnimationStyle`](https://flet.dev/docs/reference/types/animationstyle).
    """

    on_click: OptionalControlEventHandler["Chip"] = None
    """
    Fires when the user clicks on the chip. Cannot be specified together with 
    `on_select` event.
    """

    on_delete: OptionalControlEventHandler["Chip"] = None
    """
    Fires when the user clicks on the `delete_icon`.
    """

    on_select: OptionalControlEventHandler["Chip"] = None
    """
    Fires when the user clicks on the chip. Changes `selected` property to the opposite 
    value. Cannot be specified together with `on_click` event.
    """

    on_focus: OptionalControlEventHandler["Chip"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["Chip"] = None
    """
    Fires when the control has lost focus.
    """

    def before_update(self):
        super().before_update()
        assert self.on_select is None or self.on_click is None, (
            "on_select and on_click cannot be used together"
        )
        assert self.elevation is None or self.elevation >= 0.0, (
            "elevation must be greater than or equal to 0"
        )
        assert self.click_elevation is None or self.click_elevation >= 0.0, (
            "click_elevation must be greater than or equal to 0"
        )
