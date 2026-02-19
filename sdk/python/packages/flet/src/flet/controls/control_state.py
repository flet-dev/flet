from enum import Enum
from typing import TypeVar, Union

__all__ = ["ControlState", "ControlStateValue"]


class ControlState(Enum):
    """
    Interactive states that some controls can take on when receiving input
    from the user.

    States are defined by the Material 3 design
    [specification](https://m3.material.io/foundations/interaction/states),
    but are not limited to it.

    Not all states are always applicable to all controls.
    """

    HOVERED = "hovered"
    """
    The state when the user drags their mouse cursor over the given control.

    See [material docs](https://material.io/design/interaction/states.html#hover).
    """

    FOCUSED = "focused"
    """
    The state when the user navigates with the keyboard to a given control.

    This can also sometimes be triggered when a control is tapped. For example,
    when a [`TextField`] is tapped, it becomes [`FOCUSED`][(c).].

    See [material docs](https://material.io/design/interaction/states.html#focus).
    """

    PRESSED = "pressed"
    """
    The state when the user is actively pressing down on the given control.

    See [material docs](https://material.io/design/interaction/states.html#pressed).
    """

    DRAGGED = "dragged"
    """
    The state when this control is being dragged from one place to another by the user.

    See [material docs](https://material.io/design/interaction/states.html#dragged).
    """

    SELECTED = "selected"
    """
    The state when this item has been selected.

    This applies to things that can be toggled (such as chips and checkboxes)
    and things that are selected from a set of options (such as tabs and radio buttons).

    See [material docs](https://material.io/design/interaction/states.html#selected).
    """

    SCROLLED_UNDER = "scrolledUnder"
    """
    The state when this control overlaps the content of a scrollable below.

    Used by [`AppBar`][flet.] to indicate that the primary scrollable's
    content has scrolled up and behind the app bar.
    """

    DISABLED = "disabled"
    """
    The state when this control is disabled and cannot be interacted with.

    Disabled controls should not respond to hover, focus, press, or drag
    interactions.

    See [material docs](https://material.io/design/interaction/states.html#disabled).
    """

    ERROR = "error"
    """
    The state when the control has entered some form of invalid state.

    See [material docs](https://material.io/design/interaction/states.html#usage).
    """

    DEFAULT = "default"
    """
    The default state. Will be used for undeclared states.
    """


T = TypeVar("T")
ControlStateValue = Union[T, dict[ControlState, T]]
"""Type alias for state-dependent control values.

Represents either:
- a single value applied to all (supported) states,
- or a mapping from [`ControlState`][flet.] to per-state values.
"""
