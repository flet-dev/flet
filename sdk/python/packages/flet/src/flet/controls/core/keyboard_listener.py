import asyncio
from dataclasses import dataclass
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler

__all__ = [
    "KeyboardListener",
]


@dataclass
class KeyDownEvent(Event["KeyboardListener"]):
    key: str


@dataclass
class KeyUpEvent(Event["KeyboardListener"]):
    key: str


@dataclass
class KeyRepeatEvent(Event["KeyboardListener"]):
    key: str


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

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
