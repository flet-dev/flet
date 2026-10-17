"""Android notification channels."""

from dataclasses import field

import flet as ft
from flet_notifications.types import Importance


@ft.value(kw_only=True)
class NotificationChannel:
    """An Android notification channel (required since Android 8.0).

    Sound and vibration are fixed at channel creation; to change them you
    create a new channel with a new id.
    """

    id: str
    name: str
    description: str = field(default_factory=str)
    group_id: str | None = None
    importance: Importance = Importance.DEFAULT
    bypass_dnd: bool = False
    play_sound: bool = True
    sound: str | None = None  # raw resource name, e.g. "alert"
    enable_vibration: bool = True
    vibration_pattern: list[int] | None = None
    show_badge: bool = True
    enable_lights: bool = False
    led_color: ft.ColorValue | None = None
    """Channel LED color, used when :attr:`enable_lights` is enabled."""

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("channel id is required")
        if not self.name:
            raise ValueError("channel name is required")

    @classmethod
    def from_dict(cls, data: dict) -> "NotificationChannel":
        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            description=str(data.get("description") or ""),
            group_id=data.get("groupId") or data.get("group_id"),
            importance=Importance(data.get("importance", "defaultImportance")),
            bypass_dnd=bool(data.get("bypass_dnd", False)),
            play_sound=bool(data.get("play_sound", True)),
            sound=data.get("sound"),
            enable_vibration=bool(data.get("enable_vibration", True)),
            vibration_pattern=data.get("vibration_pattern"),
            show_badge=bool(data.get("show_badge", True)),
            enable_lights=bool(data.get("enable_lights", False)),
            led_color=data.get("led_color"),
        )
