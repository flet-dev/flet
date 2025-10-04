from dataclasses import dataclass
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler

__all__ = [
    "KeyDownEvent",
    "KeyRepeatEvent",
    "KeyUpEvent",
    "KeyboardListener",
]


@dataclass
class KeyDownEvent(Event["KeyboardListener"]):
    """
    Event triggered when a key is pressed down.

    Typically used to detect the initial press of a key before it is released
    or repeated.
    """

    key: str
    """
    The key that was pressed down.

    Represents the physical key (e.g., <kbd>A</kbd>, <kbd>Enter</kbd>,
    <kbd>Shift</kbd>) that triggered the key down event.
    """


@dataclass
class KeyUpEvent(Event["KeyboardListener"]):
    """
    Event triggered when a key is released.

    Useful for tracking when a key is no longer being pressed after
    a key down or repeat event.
    """

    key: str
    """
    The key that was released.

    Indicates which key was previously pressed and has now been lifted.
    """


@dataclass
class KeyRepeatEvent(Event["KeyboardListener"]):
    """
    Event triggered when a key is held down and repeating.

    This event fires continuously while the key remains pressed,
    depending on the system's key repeat rate.
    """

    key: str
    """
    The key that is being held down and repeating.

    Represents the physical key that is generating repeat events (e.g.,
    <kbd>ArrowDown</kbd>, <kbd>Backspace</kbd>).
    """


@control("KeyboardListener")
class KeyboardListener(Control):
    """
    A control that calls a callback whenever the user presses or releases
    a key on a keyboard.
    """

    content: Control
    """
    The content control of the keyboard listener.
    """

    autofocus: bool = False
    """
    True if this control will be selected as the initial focus when no other node
    in its scope is currently focused.
    """

    include_semantics: bool = True
    """
    Include semantics information in this control.
    """

    on_key_down: Optional[EventHandler[KeyDownEvent]] = None
    """
    Fires when a keyboard key is pressed.
    """

    on_key_up: Optional[EventHandler[KeyUpEvent]] = None
    """
    Fires when a keyboard key is released.
    """

    on_key_repeat: Optional[EventHandler[KeyRepeatEvent]] = None
    """
    Fires when a keyboard key is being hold, causing repeated events.
    """

    async def focus(self):
        await self._invoke_method("focus")
