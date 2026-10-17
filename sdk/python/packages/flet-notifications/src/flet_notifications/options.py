"""Per-platform notification options — the full detail surface.

Mirrors `flutter_local_notifications`' `NotificationDetails` one-to-one:
one options object per platform, merged into the notification payload.
The everyday knobs (title, body, payload, actions, style, progress,
grouping, channel) stay as flat method kwargs; this is the complete
escape hatch for everything else.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Priority(str, Enum):
    """Android notification priority (pre-8.0 semantics)."""

    MIN = "min"
    LOW = "low"
    DEFAULT = "default"
    HIGH = "high"
    MAX = "max"


class Visibility(str, Enum):
    """Android notification visibility (lock-screen disclosure)."""

    PUBLIC = "public"
    PRIVATE = "private"
    SECRET = "secret"


class InterruptionLevel(str, Enum):
    """iOS/macOS interruption level (iOS 15+/macOS 12+)."""

    PASSIVE = "passive"
    ACTIVE = "active"
    TIME_SENSITIVE = "timeSensitive"  # needs the Time Sensitive capability
    CRITICAL = "critical"  # needs an Apple entitlement


class LinuxUrgency(str, Enum):
    """Linux notification-server urgency."""

    LOW = "low"
    NORMAL = "normal"
    CRITICAL = "critical"


class WindowsScenario(str, Enum):
    """Windows toast scenario."""

    REMINDER = "reminder"
    ALARM = "alarm"
    INCOMING_CALL = "incomingCall"
    URGENT = "urgent"


def _validate_hex(value: str, what: str) -> str:
    v = value.strip()
    if not v.startswith("#") or len(v) not in (7, 9):
        raise ValueError(f"{what} must be #RRGGBB or #AARRGGBB, got {value!r}")
    try:
        int(v[1:], 16)
    except ValueError as e:
        raise ValueError(f"{what} must be #RRGGBB or #AARRGGBB, got {value!r}") from e
    return v


@dataclass(kw_only=True)
class AndroidOptions:
    """Android notification and channel details.

    Channel fields (`channel_description`, `channel_bypass_dnd`,
    `audio_attributes_usage`) apply when the channel is created — on
    Android 8+ sound/vibration are immutable after creation, so changing
    them needs a new channel id.
    """

    channel_id: str | None = None
    channel_description: str | None = None
    channel_bypass_dnd: bool | None = None
    audio_attributes_usage: str | None = None
    icon: str | None = None  # drawable resource name
    importance: str | None = None  # Importance enum value
    priority: Priority | str | None = None
    play_sound: bool | None = None
    sound: str | None = None  # raw resource name or URI
    enable_vibration: bool | None = None
    vibration_pattern: list[int] | None = None
    channel_show_badge: bool | None = None
    auto_cancel: bool | None = None
    ongoing: bool | None = None
    silent: bool | None = None
    color: str | None = None
    colorized: bool | None = None
    large_icon: str | None = None  # drawable / file path / content URI
    only_alert_once: bool | None = None
    show_when: bool | None = None
    when: int | None = None  # epoch ms override
    uses_chronometer: bool | None = None
    chronometer_count_down: bool | None = None
    sub_text: str | None = None
    number: int | None = None
    visibility: Visibility | str | None = None
    timeout_after: int | None = None  # ms
    category: str | None = None  # AndroidNotificationCategory value
    full_screen_intent: bool | None = None
    shortcut_id: str | None = None
    additional_flags: list[str] | None = None
    ticker: str | None = None
    tag: str | None = None
    enable_lights: bool | None = None
    led_color: str | None = None
    led_on_ms: int | None = None
    led_off_ms: int | None = None

    def __post_init__(self) -> None:
        for name in ("color", "led_color"):
            value = getattr(self, name)
            if value is not None:
                setattr(self, name, _validate_hex(value, name))

    def to_dict(self) -> dict:
        return {
            k: v
            for k, v in {
                "channel_id": self.channel_id,
                "channel_description": self.channel_description,
                "channel_bypass_dnd": self.channel_bypass_dnd,
                "audio_attributes_usage": self.audio_attributes_usage,
                "icon": self.icon,
                "importance": self.importance,
                "priority": self.priority,
                "play_sound": self.play_sound,
                "sound": self.sound,
                "enable_vibration": self.enable_vibration,
                "vibration_pattern": list(self.vibration_pattern)
                if self.vibration_pattern
                else None,
                "channel_show_badge": self.channel_show_badge,
                "auto_cancel": self.auto_cancel,
                "ongoing": self.ongoing,
                "silent": self.silent,
                "color": self.color,
                "colorized": self.colorized,
                "large_icon": self.large_icon,
                "only_alert_once": self.only_alert_once,
                "show_when": self.show_when,
                "when": self.when,
                "uses_chronometer": self.uses_chronometer,
                "chronometer_count_down": self.chronometer_count_down,
                "sub_text": self.sub_text,
                "number": self.number,
                "visibility": self.visibility,
                "timeout_after": self.timeout_after,
                "category": self.category,
                "full_screen_intent": self.full_screen_intent,
                "shortcut_id": self.shortcut_id,
                "additional_flags": list(self.additional_flags)
                if self.additional_flags
                else None,
                "ticker": self.ticker,
                "tag": self.tag,
                "enable_lights": self.enable_lights,
                "led_color": self.led_color,
                "led_on_ms": self.led_on_ms,
                "led_off_ms": self.led_off_ms,
            }.items()
            if v is not None
        }


@dataclass(kw_only=True)
class DarwinOptions:
    """iOS and macOS notification details."""

    sound: str | None = None  # named sound from the app bundle
    badge_number: int | None = None  # 0 clears the badge
    subtitle: str | None = None
    thread_identifier: str | None = None  # grouping
    interruption_level: InterruptionLevel | str | None = None
    critical_sound_volume: float | None = None  # 0.0 - 1.0
    attachments: list[str] | None = None  # file paths
    present_alert: bool | None = None
    present_badge: bool | None = None
    present_sound: bool | None = None
    present_banner: bool | None = None
    present_list: bool | None = None

    def to_dict(self) -> dict:
        return {
            k: v
            for k, v in {
                "sound": self.sound,
                "badge_number": self.badge_number,
                "subtitle": self.subtitle,
                "thread_identifier": self.thread_identifier,
                "interruption_level": self.interruption_level,
                "critical_sound_volume": self.critical_sound_volume,
                "attachments": list(self.attachments) if self.attachments else None,
                "present_alert": self.present_alert,
                "present_badge": self.present_badge,
                "present_sound": self.present_sound,
                "present_banner": self.present_banner,
                "present_list": self.present_list,
            }.items()
            if v is not None
        }


@dataclass(kw_only=True)
class LinuxOptions:
    """Linux (freedesktop) notification details."""

    icon: str | None = None
    sound: str | None = None
    category: str | None = None
    urgency: LinuxUrgency | str | None = None
    timeout_ms: int | None = None
    resident: bool | None = None
    transient: bool | None = None
    suppress_sound: bool | None = None
    action_key_as_icon_name: bool | None = None

    def to_dict(self) -> dict:
        return {
            k: v
            for k, v in {
                "icon": self.icon,
                "sound": self.sound,
                "category": self.category,
                "urgency": self.urgency,
                "timeout_ms": self.timeout_ms,
                "resident": self.resident,
                "transient": self.transient,
                "suppress_sound": self.suppress_sound,
                "action_key_as_icon_name": self.action_key_as_icon_name,
            }.items()
            if v is not None
        }


@dataclass(kw_only=True)
class WindowsOptions:
    """Windows toast details."""

    header: str | None = None
    audio: str | None = None  # URI or ms-winsoundevent name
    duration: str | None = None  # "long" | "short"
    scenario: WindowsScenario | str | None = None
    timestamp: int | None = None  # epoch ms
    subtitle: str | None = None
    images: list[str] | None = None  # image URIs
    bindings: dict[str, str] | None = None  # {name: value} substitutions

    def to_dict(self) -> dict:
        return {
            k: v
            for k, v in {
                "header": self.header,
                "audio": self.audio,
                "duration": self.duration,
                "scenario": self.scenario,
                "timestamp": self.timestamp,
                "subtitle": self.subtitle,
                "images": list(self.images) if self.images else None,
                "bindings": dict(self.bindings) if self.bindings else None,
            }.items()
            if v is not None
        }


@dataclass(kw_only=True)
class WebOptions:
    """Web (Browser Notification API) details."""

    direction: str | None = None  # "auto" | "ltr" | "rtl"
    badge_url: str | None = None
    icon_url: str | None = None
    image_url: str | None = None
    lang: str | None = None
    require_interaction: bool | None = None
    is_silent: bool | None = None
    renotify: bool | None = None
    timestamp: int | None = None

    def to_dict(self) -> dict:
        return {
            k: v
            for k, v in {
                "direction": self.direction,
                "badge_url": self.badge_url,
                "icon_url": self.icon_url,
                "image_url": self.image_url,
                "lang": self.lang,
                "require_interaction": self.require_interaction,
                "is_silent": self.is_silent,
                "renotify": self.renotify,
                "timestamp": self.timestamp,
            }.items()
            if v is not None
        }


@dataclass(kw_only=True)
class NotificationOptions:
    """Per-platform notification details, mirroring FLN's
    `NotificationDetails`.

    Example::

        await notifications.show(
            id=1,
            title="Quiet",
            body="Shh",
            options=NotificationOptions(
                android=AndroidOptions(silent=True, category="alarm"),
                iOS=DarwinOptions(interruption_level="passive"),
            ),
        )
    """

    android: AndroidOptions | None = None
    iOS: DarwinOptions | None = None
    macOS: DarwinOptions | None = None
    linux: LinuxOptions | None = None
    windows: WindowsOptions | None = None
    web: WebOptions | None = None

    def to_dict(self) -> dict:
        return {
            "android": self.android.to_dict() if self.android else None,
            "iOS": self.iOS.to_dict() if self.iOS else None,
            "macOS": self.macOS.to_dict() if self.macOS else None,
            "linux": self.linux.to_dict() if self.linux else None,
            "windows": self.windows.to_dict() if self.windows else None,
            "web": self.web.to_dict() if self.web else None,
        }
