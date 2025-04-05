from typing import Optional

from flet.controls.material.badge import BadgeValue
from flet.core.control import Control, control
from flet.core.types import OptionalControlEventCallable, OptionalNumber

__all__ = ["Semantics"]


@control("Semantics")
class Semantics(Control):
    """
    A control that annotates the control tree with a description of the meaning of the widgets.

    Used by accessibility tools, search engines, and other semantic analysis software to determine the meaning of the application.

    -----

    Online docs: https://flet.dev/docs/controls/semantics
    """

    content: Optional[Control] = None
    label: Optional[str] = None
    expanded: Optional[bool] = None
    hidden: Optional[bool] = None
    selected: Optional[bool] = None
    button: Optional[bool] = None
    obscured: Optional[bool] = None
    multiline: Optional[bool] = None
    focusable: Optional[bool] = None
    read_only: Optional[bool] = None
    focus: Optional[bool] = None
    slider: Optional[bool] = None
    tooltip: Optional[str] = None
    badge: Optional[BadgeValue] = None
    toggled: Optional[bool] = None
    max_value_length: OptionalNumber = None
    checked: Optional[bool] = None
    value: Optional[str] = None
    increased_value: Optional[str] = None
    decreased_value: Optional[str] = None
    hint_text: Optional[str] = None
    on_tap_hint_text: Optional[str] = None
    current_value_length: Optional[int] = None
    heading_level: Optional[int] = None
    exclude_semantics: Optional[bool] = None
    mixed: Optional[bool] = None
    on_long_press_hint_text: Optional[str] = None
    container: Optional[bool] = None
    live_region: Optional[bool] = None
    textfield: Optional[bool] = None
    link: Optional[bool] = None
    header: Optional[bool] = None
    image: Optional[bool] = None
    on_tap: OptionalControlEventCallable = None
    on_double_tap: OptionalControlEventCallable = None
    on_increase: OptionalControlEventCallable = None
    on_decrease: OptionalControlEventCallable = None
    on_dismiss: OptionalControlEventCallable = None
    on_scroll_left: OptionalControlEventCallable = None
    on_scroll_right: OptionalControlEventCallable = None
    on_scroll_up: OptionalControlEventCallable = None
    on_scroll_down: OptionalControlEventCallable = None
    on_copy: OptionalControlEventCallable = None
    on_cut: OptionalControlEventCallable = None
    on_paste: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_move_cursor_forward_by_character: OptionalControlEventCallable = None
    on_move_cursor_backward_by_character: OptionalControlEventCallable = None
    on_did_gain_accessibility_focus: OptionalControlEventCallable = None
    on_did_lose_accessibility_focus: OptionalControlEventCallable = None
    on_set_text: OptionalControlEventCallable = None
