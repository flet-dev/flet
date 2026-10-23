import flet as ft
from flet_notifications.types import AndroidAudioAttributesUsage, AndroidImportance

__all__ = ["NotificationChannel"]


@ft.value(kw_only=True)
class NotificationChannel:
    """
    Android notification channel grouping notifications with shared behavior.

    Pass it as :attr:`flet_notifications.AndroidOptions.channel` to create the channel
    when a notification is first posted to it, or create it upfront with
    :meth:`flet_notifications.LocalNotifications.create_notification_channel` and pass
    its :attr:`id` instead. Users manage channel preferences independently in Android
    settings. Sound, vibration, lights, and importance cannot be reset by posting
    another notification or recreating the same channel; use a new ID for a different
    configuration.

    Note:
        Channels exist on Android 8.0+. On earlier versions, the channel's sound,
        vibration, lights, and importance apply to each notification posted with it.

    Raises:
        ValueError: If :attr:`id` or :attr:`name` is empty.
    """

    id: str
    """Nonempty, stable channel identifier used when posting notifications."""

    name: str
    """Nonempty, user-visible channel name displayed in Android settings."""

    description: str | None = None
    """
    User-visible explanation of the notifications delivered through this channel.

    `None` shows no description.
    """

    group_id: str | None = None
    """
    ID of the notification-channel group containing this channel.

    Create the group first with
    :meth:`flet_notifications.LocalNotifications.create_notification_channel_group`.
    This organizes channels in settings; it does not group notifications in the tray.
    """

    importance: AndroidImportance = AndroidImportance.DEFAULT
    """
    Initial channel importance.

    The user can change it after creation. See
    :class:`flet_notifications.AndroidImportance` for the interruption behavior of each
    level.
    """

    bypass_dnd: bool = False
    """
    Whether the channel should attempt to bypass Do Not Disturb.

    Note:
        Obtain notification-policy access with
        :meth:`flet_notifications.LocalNotifications.request_notification_policy_access`
        before creating the channel; otherwise Android ignores the request.
    """

    play_sound: bool = True
    """
    Whether notifications in the channel play sound.

    Note:
        Fixed at channel creation. Use :attr:`sound` to choose a custom sound.
    """

    sound: str | None = None
    """
    Sound resource name or `content://` / `file://` URI on the Android device.

    A raw resource name, such as `"alert"`, refers to a file in the app's
    `res/raw` resources and omits the file extension. Add the file with the
    [`res_dir`](https://flet.dev/docs/publish/android#resources) build setting,
    for example as `raw/alert.mp3`.

    Note:
        Requires :attr:`play_sound`. `None` uses the default notification sound.
        Fixed at channel creation; changing this value does not replace an existing
        channel's sound.

        A `file://` URI of a file in the app's private storage is stored but not
        played, because the system cannot read the file.
    """

    enable_vibration: bool = True
    """
    Whether notifications in the channel vibrate.

    Note:
        Requires the Android `VIBRATE` permission. Fixed at channel creation.
    """

    vibration_pattern: list[int] | None = None
    """
    Alternating delay and vibration durations, in milliseconds.

    Note:
        For example, `[0, 200, 100, 200]` starts immediately and vibrates twice.
        Requires :attr:`enable_vibration`; fixed at channel creation.
    """

    show_badge: bool = True
    """
    Whether notifications may contribute launcher badges.

    Note:
        Requires support from the launcher and is subject to user settings.
    """

    enable_lights: bool = False
    """
    Whether to use the notification LED on supported devices.

    Note:
        Fixed at channel creation.
    """

    led_color: ft.ColorValue | None = None
    """
    LED color used when :attr:`enable_lights` is enabled.

    Note:
        Accepts concrete Flet color names and hexadecimal colors. Theme-dependent colors
        cannot be resolved by this headless service. Fixed at channel creation.
    """

    audio_attributes_usage: AndroidAudioAttributesUsage = (
        AndroidAudioAttributesUsage.NOTIFICATION
    )
    """
    Intended use of the channel's sound.

    Helps Android select audio routing, volume, and interruption policies. It does not
    enable sound when :attr:`play_sound` is `False` or grant access to bypass Do Not
    Disturb.

    Note:
        Fixed at channel creation.
    """

    def __post_init__(self) -> None:
        if not self.id:
            raise ValueError("channel id is required")
        if not self.name:
            raise ValueError("channel name is required")
