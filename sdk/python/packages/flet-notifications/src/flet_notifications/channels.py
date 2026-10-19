from dataclasses import field

import flet as ft
from flet_notifications.types import Importance

__all__ = ["NotificationChannel"]


@ft.value(kw_only=True)
class NotificationChannel:
    """
    Android 8.0+ notification channel grouping notifications with shared behavior.

    Create it with
    :meth:`flet_notifications.LocalNotifications.create_notification_channel`, then
    pass its :attr:`id` as the notification's `channel_id`. Users manage channel
    preferences independently in Android settings. Sound, vibration, lights, and
    importance cannot be reset by posting another notification or recreating the same
    channel; use a new ID for a different configuration.

    Raises:
        ValueError: If :attr:`id` or :attr:`name` is empty.
    """

    id: str
    """Nonempty, stable channel identifier used when posting notifications."""

    name: str
    """Nonempty, user-visible channel name displayed in Android settings."""

    description: str = field(default_factory=str)
    """User-visible explanation of the notifications delivered through this channel."""

    group_id: str | None = None
    """
    ID of the notification-channel group containing this channel.

    Create the group first with
    :meth:`flet_notifications.LocalNotifications.create_notification_channel_group`.
    This organizes channels in settings; it does not group notifications in the tray.
    """

    importance: Importance = Importance.DEFAULT
    """
    Initial channel importance.

    The user can change it after creation. See :class:`flet_notifications.Importance`
    for the interruption behavior of each level.
    """

    bypass_dnd: bool = False
    """
    Whether the channel should attempt to bypass Do Not Disturb.

    Obtain notification-policy access with
    :meth:`flet_notifications.LocalNotifications.request_notification_policy_access`
    before creating the channel; otherwise Android ignores the request.
    """

    play_sound: bool = True
    """
    Whether notifications in the channel play sound.

    Fixed at channel creation. Use :attr:`sound` to choose a custom sound.
    """

    sound: str | None = None
    """
    Raw Android sound-resource name without an extension, such as `"alert"`.

    Requires :attr:`play_sound`. `None` uses the default notification sound. This
    channel API accepts raw resource names, not file paths or content URIs. Fixed at
    channel creation.
    """

    enable_vibration: bool = True
    """
    Whether notifications in the channel vibrate.

    Requires the Android `VIBRATE` permission. Fixed at channel creation.
    """

    vibration_pattern: list[int] | None = None
    """
    Alternating delay and vibration durations, in milliseconds.

    For example, `[0, 200, 100, 200]` starts immediately and vibrates twice. Requires
    :attr:`enable_vibration`; fixed at channel creation.
    """

    show_badge: bool = True
    """
    Whether notifications may contribute launcher badges.

    Requires support from the launcher and is subject to user settings.
    """

    enable_lights: bool = False
    """
    Whether to use the notification LED on supported devices.

    Fixed at channel creation.
    """

    led_color: ft.ColorValue | None = None
    """
    LED color used when :attr:`enable_lights` is enabled.

    Accepts concrete Flet color names and hexadecimal colors. Theme-dependent colors
    cannot be resolved by this headless service. Fixed at channel creation.
    """

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("channel id is required")
        if not self.name:
            raise ValueError("channel name is required")

    @classmethod
    def from_dict(cls, data: dict) -> "NotificationChannel":
        """
        Construct a channel from a native channel-query result.

        Args:
            data: Mapping returned by the bridge, accepting `groupId` or `group_id`
                for the channel's group and serialized
                :class:`flet_notifications.Importance` values.

        Returns:
            Channel populated from the mapping, with defaults for absent fields.

        Raises:
            ValueError: If the ID or name is empty, or the importance is unknown.
        """
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
