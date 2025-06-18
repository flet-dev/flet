from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.material.badge import BadgeValue
from flet.controls.types import OptionalNumber

__all__ = ["Semantics"]


@control("Semantics")
class Semantics(Control):
    """
    A control that annotates the control tree with a description of the meaning of the
    widgets.

    Used by accessibility tools, search engines, and other semantic analysis software
    to determine the meaning of the application.

    Online docs: https://flet.dev/docs/controls/semantics
    """

    content: Optional[Control] = None
    """
    The `Control` to annotate.
    """

    label: Optional[str] = None
    """
    A textual description of the `content` control.
    """

    expanded: Optional[bool] = None
    """
    Whether this subtree represents something that can be in an "expanded" or
    "collapsed" state.
    """

    hidden: Optional[bool] = None
    """
    Whether this subtree is currently hidden.
    """

    selected: Optional[bool] = None
    """
    Whether this subtree represents something that can be in a selected or unselected
    state, and what its current state is.
    """

    button: Optional[bool] = None
    """
    Whether this subtree represents a button.
    """

    obscured: Optional[bool] = None
    """
    Whether `value` should be obscured.
    """

    multiline: Optional[bool] = None
    """
    Whether the `value` is coming from a field that supports multiline text editing.
    """

    focusable: Optional[bool] = None
    """
    Whether the node is able to hold input focus.
    """

    read_only: Optional[bool] = None
    """
    Whether this subtree is read only.
    """

    focus: Optional[bool] = None
    """
    Whether the node currently holds input focus.
    """

    slider: Optional[bool] = None
    """
    Whether this subtree represents a slider.
    """

    tooltip: Optional[str] = None
    """
    A textual description of the widget's tooltip.
    """

    badge: Optional[BadgeValue] = None
    """
    TBD
    """

    toggled: Optional[bool] = None
    """
    Whether this subtree represents a toggle switch or similar widget with an "on"
    state, and what its current state is.
    """

    max_value_length: OptionalNumber = None
    """
    The maximum number of characters that can be entered into an editable text field.
    """

    checked: Optional[bool] = None
    """
    Whether this subtree represents a checkbox or similar widget with a "checked"
    state, and what its current state is.
    """

    value: Optional[str] = None
    """
    A textual description of the `value` of the `content` control.
    """

    increased_value: Optional[str] = None
    """
    The value that the semantics node represents when it is increased.
    """

    decreased_value: Optional[str] = None
    """
    The value that the semantics node represents when it is decreased.
    """

    hint_text: Optional[str] = None
    """
    A brief textual description of the result of an action performed on the `content`
    control.
    """

    on_tap_hint_text: Optional[str] = None
    """
    TBD
    """

    current_value_length: Optional[int] = None
    """
    The current number of characters that have been entered into an editable text
    field.
    """

    heading_level: Optional[int] = None
    """
    The heading level in the DOM document structure.
    """

    exclude_semantics: bool = False
    """
    TBD
    """

    mixed: Optional[bool] = None
    """
    Whether this subtree represents a checkbox or similar control with a "half-checked"
    state or similar, and whether it is currently in this half-checked state.
    """

    on_long_press_hint_text: Optional[str] = None
    """
    TBD
    """

    container: Optional[bool] = None
    """
    TBD
    """

    live_region: Optional[bool] = None
    """
    Whether this subtree should be considered a live region.
    """

    textfield: Optional[bool] = None
    """
    Whether  this subtree represents a text field.
    """

    link: Optional[bool] = None
    """
    Whether this subtree represents a link.
    """

    header: Optional[bool] = None
    """
    Whether this subtree represents a header.
    """

    image: Optional[bool] = None
    """
    Whether the node represents an image.
    """

    on_tap: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when this control is tapped.
    """

    on_double_tap: OptionalControlEventHandler["Semantics"] = None
    """
    TBD
    """

    on_increase: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the value represented by the semantics node is increased.
    """

    on_decrease: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the value represented by the semantics node is decreased.
    """

    on_dismiss: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the node is dismissed.
    """

    on_scroll_left: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when a user moves their finger across the screen from right to left.
    """

    on_scroll_right: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when a user moves their finger across the screen from left to right.
    """

    on_scroll_up: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when a user moves their finger across the screen from bottom to top.
    """

    on_scroll_down: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when a user moves their finger across the screen from top to bottom.
    """

    on_copy: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the current selection is copied to the clipboard.
    """

    on_cut: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the current selection is cut to the clipboard.
    """

    on_paste: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the current content of the clipboard is pasted.
    """

    on_long_press: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the node is long-pressed (pressing and holding the screen with the
    finger for a few seconds without moving it).
    """

    on_move_cursor_forward_by_character: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the cursor is moved forward by one character.
    """

    on_move_cursor_backward_by_character: OptionalControlEventHandler["Semantics"] = (
        None
    )
    """
    Fires when the cursor is moved backward by one character.
    """

    on_did_gain_accessibility_focus: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the node has gained accessibility focus.
    """

    on_did_lose_accessibility_focus: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when the node has lost accessibility focus.
    """

    on_set_text: OptionalControlEventHandler["Semantics"] = None
    """
    Fires when a user wants to replace the current text in the text field with a new
    text.

    Voice access users can trigger this handler by speaking type `<text>` to their
    Android devices.
    """
