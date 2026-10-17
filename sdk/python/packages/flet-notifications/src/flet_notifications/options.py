"""Per-platform notification options — the full detail surface.

Mirrors `flutter_local_notifications`' `NotificationDetails` one-to-one:
one options object per platform, merged into the notification payload.
The everyday knobs (title, body, payload, actions, style, progress,
grouping, channel) stay as flat method kwargs; this is the complete
escape hatch for everything else.
"""

from enum import Enum

import flet as ft


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


@ft.value(kw_only=True)
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


@ft.value(kw_only=True)
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


@ft.value(kw_only=True)
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


@ft.value(kw_only=True)
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


@ft.value(kw_only=True)
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


@ft.value(kw_only=True)
class NotificationOptions:
    """Per-platform notification details, mirroring FLN's
    `NotificationDetails`.

    Example:
        ```python
        await notifications.show(
            id=1,
            title="Quiet",
            body="Shh",
            options=NotificationOptions(
                android=AndroidOptions(silent=True, category="alarm"),
                iOS=DarwinOptions(interruption_level="passive"),
            ),
        )
        ```
    """

    android: AndroidOptions | None = None
    iOS: DarwinOptions | None = None
    macOS: DarwinOptions | None = None
    linux: LinuxOptions | None = None
    windows: WindowsOptions | None = None
    web: WebOptions | None = None
