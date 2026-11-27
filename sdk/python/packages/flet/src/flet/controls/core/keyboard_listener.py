from dataclasses import dataclass
from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler
from flet.controls.keyboard_key import KeyboardKey, PhysicalKeyboardKey

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

    key: Union[KeyboardKey, str]
    """
    The key that was pressed down, such as :attr:`~flet.KeyboardKey.A`,
    :attr:`~flet.KeyboardKey.ENTER` or :attr:`~flet.KeyboardKey.SHIFT_LEFT`.

    A key that has no :class:`~flet.KeyboardKey` member is a plain string,
    such as `"Ü"`.
    """

    physical_key: Union[PhysicalKeyboardKey, int, None] = None
    """
    The position of the key that was pressed down on the keyboard, such as
    :attr:`flet.PhysicalKeyboardKey.W`, whatever the active layout.

    A key that has no :class:`~flet.PhysicalKeyboardKey` member is its USB HID
    usage code. Older clients that omit the physical key leave this as `None`.
    """


@dataclass
class KeyUpEvent(Event["KeyboardListener"]):
    """
    Event triggered when a key is released.

    Useful for tracking when a key is no longer being pressed after
    a key down or repeat event.
    """

    key: Union[KeyboardKey, str]
    """
    The key that was released.

    A key that has no :class:`~flet.KeyboardKey` member is a plain string,
    such as `"Ü"`.
    """

    physical_key: Union[PhysicalKeyboardKey, int, None] = None
    """
    The position of the key that was released on the keyboard, such as
    :attr:`flet.PhysicalKeyboardKey.W`, whatever the active layout.

    A key that has no :class:`~flet.PhysicalKeyboardKey` member is its USB HID
    usage code. Older clients that omit the physical key leave this as `None`.
    """


@dataclass
class KeyRepeatEvent(Event["KeyboardListener"]):
    """
    Event triggered when a key is held down and repeating.

    This event fires continuously while the key remains pressed,
    depending on the system's key repeat rate.
    """

    key: Union[KeyboardKey, str]
    """
    The key that is being held down and repeating, such as
    :attr:`~flet.KeyboardKey.ARROW_DOWN` or :attr:`~flet.KeyboardKey.BACKSPACE`.

    A key that has no :class:`~flet.KeyboardKey` member is a plain string,
    such as `"Ü"`.
    """

    physical_key: Union[PhysicalKeyboardKey, int, None] = None
    """
    The position of the key being held down on the keyboard, such as
    :attr:`flet.PhysicalKeyboardKey.W`, whatever the active layout.

    A key that has no :class:`~flet.PhysicalKeyboardKey` member is its USB HID
    usage code. Older clients that omit the physical key leave this as `None`.
    """


@control("KeyboardListener")
class KeyboardListener(Control):
    """
    A control that calls a callback whenever the user presses or releases a key on a \
    keyboard.
    """

    content: Control
    """
    The content control of the keyboard listener.
    """

    autofocus: bool = False
    """
    True if this control will be selected as the initial focus when no other node in \
    its scope is currently focused.
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
        """Requests focus for this control."""
        await self._invoke_method("focus")
