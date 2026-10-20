from enum import Enum

import flet as ft
from flet_notifications.types import (
    AndroidAudioAttributesUsage,
    AndroidNotificationCategory,
    AndroidNotificationFlag,
    Importance,
    LinuxNotificationCategory,
    WindowsNotificationDuration,
    WindowsNotificationSound,
)

__all__ = [
    "AndroidOptions",
    "DarwinOptions",
    "InterruptionLevel",
    "LinuxOptions",
    "LinuxUrgency",
    "NotificationOptions",
    "Priority",
    "Visibility",
    "WebOptions",
    "WindowsOptions",
    "WindowsScenario",
]


class Priority(Enum):
    """
    Notification priority on Android 7.1 and earlier.

    On Android 8.0 and later, channel :class:`~flet_notifications.Importance` determines
    interruption behavior instead. Priority is a presentation hint; it does not override
    the user's notification preferences.
    """

    MIN = "min"
    """Use the lowest priority for information that does not need attention."""

    LOW = "low"
    """Use low priority for non-urgent background information."""

    DEFAULT = "default"
    """Use normal priority for ordinary notifications."""

    HIGH = "high"
    """Use high priority for time-sensitive information."""

    MAX = "max"
    """Use the highest priority for critical, immediate information."""


class Visibility(Enum):
    """
    How much Android notification content may appear on a secure lock screen.

    The user's lock-screen settings may further restrict visibility.
    """

    PUBLIC = "public"
    """Allow the entire notification to appear on any lock screen."""

    PRIVATE = "private"
    """
    Show the notification while concealing sensitive content on secure lockscreens.
    """

    SECRET = "secret"
    """Hide the notification entirely on a secure lock screen."""


class InterruptionLevel(Enum):
    """
    Presentation urgency on iOS 15+ and macOS 12+.

    Set :attr:`flet_notifications.DarwinOptions.interruption_level` to control delivery
    timing and how a notification interacts with system interruption controls. Available
    presentation and sound permissions still apply.
    """

    PASSIVE = "passive"
    """
    Add the notification quietly to the notification list.

    Does not light the screen or play a sound. Appropriate for information the user can
    read later, such as a recommendation or routine status update.
    """

    ACTIVE = "active"
    """
    Present the notification immediately, lighting the screen and allowing sound.

    Uses ordinary notification behavior and respects Focus and notification summary
    settings. Appropriate for updates that merit attention without requiring an
    immediate response.
    """

    TIME_SENSITIVE = "timeSensitive"
    """
    Present time-sensitive information immediately, subject to user settings.

    Can bypass notification summaries and Focus when the user allows time-sensitive
    notifications. Add the Time Sensitive Notifications capability to the iOS app. Use
    for events that need attention now, such as an imminent delivery, rather than
    ordinary updates.
    """

    CRITICAL = "critical"
    """
    Present a critical alert that can sound through mute and Do Not Disturb.

    Requires Apple's approval for the critical-alert entitlement and the user's
    critical-alert authorization. Enable
    :attr:`flet_notifications.LocalNotifications.request_critical_permission` when
    requesting permission. Reserve for urgent health or safety alerts.
    """


class LinuxUrgency(Enum):
    """
    Urgency hint sent to the Linux desktop notification server.

    The server decides how to display notifications and may ignore hints.
    """

    LOW = "low"
    """Use low urgency for information that does not require immediate attention."""

    NORMAL = "normal"
    """Use normal urgency for an ordinary notification."""

    CRITICAL = "critical"
    """
    Use critical urgency for information requiring immediate attention.

    A conforming server should keep critical notifications visible until dismissed, but
    desktop-specific behavior can vary.
    """


class WindowsScenario(Enum):
    """
    Windows toast scenario controlling presentation and default audio.

    Set :attr:`flet_notifications.WindowsOptions.scenario`. Windows applies its own
    version, capability, and user-setting restrictions to each scenario.
    """

    REMINDER = "reminder"
    """
    Request an expanded reminder that remains until manually dismissed.

    Upstream requires an action that activates a background task for this behavior. The
    extension currently creates dismissing actions, so this scenario alone does not
    provide that background-task behavior.
    """

    ALARM = "alarm"
    """
    Show an expanded alarm that remains until dismissed.

    Windows normally loops the alarm sound unless audio options override it.
    """

    INCOMING_CALL = "incomingCall"
    """Use the incoming-call layout with looping call audio by default."""

    URGENT = "urgent"
    """
    Request an urgent notification that may break through Do Not Disturb.

    Requires a Windows version and user settings that permit urgent notifications.
    """


@ft.value(kw_only=True)
class AndroidOptions:
    """
    Android-specific notification and channel settings.

    On Android 8.0+, importance, sound, vibration, lights, and badge settings belong to
    the channel. Reusing a channel ID does not replace its established behavior or the
    user's choices. Create a
    :class:`~flet_notifications.NotificationChannel` before posting when you need a
    custom channel name or group.
    """

    channel_id: str | None = None
    """
    Channel ID to use when the method's `channel_id` is omitted.

    The bridge creates a missing channel with the name `"Notifications"`.
    """

    channel_description: str | None = None
    """
    User-visible explanation of the channel on Android 8.0+.

    Used when creating the channel.
    """

    channel_bypass_dnd: bool | None = None
    """
    Whether a newly created channel may bypass Do Not Disturb.

    Obtain notification-policy access with
    :meth:`flet_notifications.LocalNotifications.request_notification_policy_access`
    before creating a channel with this enabled.
    """

    audio_attributes_usage: AndroidAudioAttributesUsage | None = None
    """
    Intended use of the notification sound.

    Helps Android select audio routing, volume, and interruption policies. On Android
    8.0+, this is used when creating a channel; an existing channel keeps its audio
    configuration. It does not enable sound when :attr:`play_sound` is `False` nor grant
    access to bypass Do Not Disturb.
    """

    icon: str | None = None
    """
    Bundled drawable resource name for this notification's small icon.

    Supply the resource name without a file extension, such as `"ic_stat_notify"`.
    `None` uses :attr:`flet_notifications.LocalNotifications.default_icon`.

    Include the drawable in the Android app. Use a white silhouette on a transparent
    background, with resources sized for the supported screen densities. Android
    Studio's
    [notification icon wizard](https://developer.android.com/studio/write/create-app-icons#create-notification)
    generates the appropriate drawable variants. Android uses the icon's alpha channel
    to determine its visible shape; an opaque background can appear as a solid block.
    """

    importance: Importance | None = None
    """
    Importance used when creating the channel on Android 8.0+.

    Existing channels keep their importance; the user may change it in system settings.
    """

    priority: Priority | None = None
    """
    Priority used on Android 7.1 and earlier.

    On Android 8.0+, configure :attr:`importance` instead.
    """

    play_sound: bool | None = None
    """
    Whether to play a notification sound.

    On Android 8.0+, this is fixed when the channel is first created. See :attr:`sound`
    and :attr:`silent`.
    """

    sound: str | None = None
    """
    Sound resource name or `content://` / `file://` URI on the Android device.

    A raw resource name, such as `"alert"`, omits the file extension. When
    :attr:`play_sound` is enabled and this is `None`, Android uses the default
    notification sound. Immutable for an existing channel on Android 8.0+.
    """

    enable_vibration: bool | None = None
    """
    Whether to vibrate.

    Requires the Android `VIBRATE` permission. On Android 8.0+, the setting belongs to
    the channel and cannot be changed by subsequent notifications.
    """

    vibration_pattern: list[int] | None = None
    """
    Alternating delay and vibration durations, in milliseconds.

    For example, `[0, 200, 100, 200]` starts immediately, vibrates for 200 ms, pauses
    for 100 ms, then vibrates for 200 ms. Requires :attr:`enable_vibration`. On Android
    8.0+, fixed at channel creation.
    """

    channel_show_badge: bool | None = None
    """
    Whether the channel's notifications may contribute launcher badges.

    The launcher must support notification badges.
    """

    auto_cancel: bool | None = None
    """Whether tapping the notification automatically dismisses it."""

    ongoing: bool | None = None
    """
    Whether to mark the notification as an ongoing activity.

    Android controls whether the user can dismiss ongoing notifications; this does not
    start a foreground service.
    """

    silent: bool | None = None
    """
    Whether to suppress sound and vibration for this notification.

    This is a per-notification setting, distinct from changing the channel's sound and
    vibration configuration.
    """

    color: ft.ColorValue | None = None
    """
    Android notification accent color.

    Accepts Flet color names and hexadecimal colors. Theme-dependent colors, such as
    `ft.Colors.PRIMARY`, cannot be resolved by this headless service.
    """

    colorized: bool | None = None
    """
    Whether to use :attr:`color` for the notification background.

    When disabled, the color accents the app icon. Android usually restricts background
    coloring to foreground-service notifications.
    """

    large_icon: str | None = None
    """
    Drawable resource name or absolute device file path for the large icon.

    Paths beginning with `/` or containing a backslash are treated as file paths; other
    strings are drawable names. Content URIs are not supported by this field. For richer
    image sources, see :class:`~flet_notifications.AndroidIcon`.
    """

    only_alert_once: bool | None = None
    """
    Whether sound, vibration, and ticker alert only on the first display.

    Enable when repeatedly updating the same notification, such as a progress
    notification, without alerting on each update.
    """

    show_when: bool | None = None
    """
    Whether to display the notification timestamp.

    Set :attr:`when` to override the displayed time.
    """

    when: int | None = None
    """
    Displayed timestamp as milliseconds since the Unix epoch in UTC.

    When `None`, uses the notification's posting time. This does not schedule delivery;
    use :meth:`flet_notifications.LocalNotifications.schedule` for that.
    """

    uses_chronometer: bool | None = None
    """
    Whether to show elapsed time from :attr:`when` instead of a timestamp.

    Android updates the minutes and seconds automatically, which is useful for ongoing
    calls or timers.
    """

    chronometer_count_down: bool | None = None
    """
    Whether the chronometer counts down rather than up on Android 7.0+.

    Requires :attr:`uses_chronometer` to be enabled.
    """

    sub_text: str | None = None
    """
    Supplementary information displayed in the notification template.

    Android 7.0+ places this in the header. Earlier versions use the same line as the
    progress bar, so avoid using both on those versions.
    """

    number: int | None = None
    """
    Notification count displayed by launchers that support badge numbers.

    Ignored when the launcher does not support this feature.
    """

    visibility: Visibility | None = None
    """
    How much content may appear on a secure lock screen.

    `None` leaves the choice to Android. See :class:`flet_notifications.Visibility`.
    """

    timeout_after: int | None = None
    """
    Milliseconds after posting before Android cancels the notification.

    `None` does not request automatic cancellation after a timeout.
    """

    category: AndroidNotificationCategory | None = None
    """
    Semantic category used by Android to rank and filter notifications.

    See :class:`~flet_notifications.AndroidNotificationCategory` for the supported
    categories. This does not change the notification channel's importance.
    """

    full_screen_intent: bool | None = None
    """
    Whether to request full-screen presentation when the notification arrives.

    Requires Android manifest configuration and, on Android 14+, full-screen-intent
    access. See
    :meth:`flet_notifications.LocalNotifications.request_full_screen_intent_permission`.
    Android may show a heads-up notification instead. A full-screen launch is reported
    through :attr:`flet_notifications.LocalNotifications.on_tap`.
    """

    shortcut_id: str | None = None
    """
    ID of a published, long-lived sharing shortcut linked to the notification.

    On Android 11+, this can help a messaging notification appear in the conversation
    section. This extension does not create the shortcut.
    """

    additional_flags: AndroidNotificationFlag | int | None = None
    """
    Additional native Android notification flags, combined using `|`.

    For example, combine :attr:`flet_notifications.AndroidNotificationFlag.INSISTENT`
    and :attr:`flet_notifications.AndroidNotificationFlag.NO_CLEAR` to request repeating
    audio and retention when the user presses Clear all. Android may restrict the
    effect of individual flags.

    A raw integer bitmask is also accepted for Android flags not represented by
    :class:`flet_notifications.AndroidNotificationFlag`. Combine integer flag values
    using `|` in the same way. See Android's
    [notification flags](https://developer.android.com/reference/android/app/Notification#flags)
    for their meanings and restrictions.

    Flags are added after the notification is built. `None` or
    :attr:`flet_notifications.AndroidNotificationFlag.NONE` adds no flags and does not
    clear flags set by other options. Prefer dedicated options such as :attr:`ongoing`
    and :attr:`auto_cancel` when available.
    """

    ticker: str | None = None
    """Ticker text sent to Android accessibility services."""

    tag: str | None = None
    """
    Additional identifier for immediately displayed Android notifications.

    The same `(tag, id)` pair replaces a visible notification. Pass the tag to
    :meth:`flet_notifications.LocalNotifications.cancel` to remove it. Scheduled alarms
    use only the notification ID, not this pair.
    """

    enable_lights: bool | None = None
    """
    Whether to enable the notification LED on devices that provide one.

    On Android 8.0+, this belongs to the channel.
    """

    led_color: ft.ColorValue | None = None
    """
    Color of the notification LED when :attr:`enable_lights` is enabled.

    On Android 8.0+, fixed at channel creation. Accepts concrete Flet colors;
    theme-dependent colors cannot be resolved by this headless service. Before Android
    8.0, also set :attr:`led_on_ms` and :attr:`led_off_ms`.
    """

    led_on_ms: int | None = None
    """LED on-time in milliseconds, used only before Android 8.0."""

    led_off_ms: int | None = None
    """LED off-time in milliseconds, used only before Android 8.0."""


@ft.value(kw_only=True)
class DarwinOptions:
    """
    Notification content and foreground presentation on iOS and macOS.

    Presentation flags set to `None` inherit the plugin's initialization defaults, which
    this extension leaves enabled. They affect presentation when the app is in the
    foreground; they do not grant notification permission.
    """

    sound: str | None = None
    """
    Name of a notification sound file in the app bundle.

    Requires :attr:`present_sound`. With sound presentation enabled, `None` uses the
    default notification sound. Apple limits supported file formats and custom-sound
    duration.
    """

    badge_number: int | None = None
    """
    Number to apply to the application icon badge.

    Use `0` to clear the badge, a positive number to set it, or `None` to leave it
    unchanged. Requires badge authorization.
    """

    subtitle: str | None = None
    """Secondary description displayed between the title and body."""

    thread_identifier: str | None = None
    """
    Identifier used to group related notifications in Notification Center.

    Notifications with the same identifier belong to the same thread.
    """

    interruption_level: InterruptionLevel | None = None
    """
    Delivery urgency on iOS 15+ and macOS 12+.

    See :class:`flet_notifications.InterruptionLevel` for presentation behavior and
    capability requirements. `None` leaves the level to the system.
    """

    critical_sound_volume: float | None = None
    """
    Volume of a critical-alert sound, from `0.0` to `1.0`.

    Used only for critical alerts on iOS 12+ and macOS 10.14+. Requires the
    critical-alert entitlement and authorization; see
    :attr:`flet_notifications.InterruptionLevel.CRITICAL`.
    """

    attachments: list[str] | None = None
    """
    Local device file paths of media to attach to the notification.

    Supported on iOS 10+ and macOS 10.14+. Files must be accessible to the app and use a
    media format accepted by Apple's notification framework. These are device paths, not
    URLs or paths on the Python server.
    """

    present_alert: bool | None = None
    """
    Whether to display a foreground alert using the older presentation option.

    On newer systems, use :attr:`present_banner` and :attr:`present_list`. `None`
    inherits the enabled initialization default.
    """

    present_badge: bool | None = None
    """
    Whether to apply the badge while the app is in the foreground.

    `None` inherits the enabled initialization default. Set the badge value with
    :attr:`badge_number`; badge authorization is still required.
    """

    present_sound: bool | None = None
    """
    Whether to play sound while the app is in the foreground.

    `None` inherits the enabled initialization default. With `False` and no custom
    :attr:`sound`, upstream also suppresses background notification sound. An explicit
    unrecognized sound name falls back to the system sound.
    """

    present_banner: bool | None = None
    """
    Whether to show a foreground banner on iOS 14+ and macOS 11+.

    `None` inherits the enabled initialization default.
    """

    present_list: bool | None = None
    """
    Whether to add a foreground notification to Notification Center.

    Applies on iOS 14+ and macOS 11+. `None` inherits the enabled initialization
    default.
    """


@ft.value(kw_only=True)
class LinuxOptions:
    """
    Hints for a Linux freedesktop notification server.

    Feature support varies by desktop and notification daemon. Unsupported hints may be
    ignored. This extension does not expose server-capability queries.
    """

    icon: str | None = None
    """
    Theme icon name or absolute device file path.

    The bridge also recognizes a `file://` prefix as a file-icon source; theme names
    such as `"dialog-information"` use the desktop's installed icon theme.
    """

    sound: str | None = None
    """Name of a sound from the desktop sound theme, such as `"message"`."""

    category: LinuxNotificationCategory | None = None
    """
    Category hint used by the server to classify the notification.

    See :class:`~flet_notifications.LinuxNotificationCategory`. The notification
    server determines the presentation and may ignore this hint.
    """

    urgency: LinuxUrgency | None = None
    """Urgency hint."""

    timeout_ms: int | None = None
    """
    Requested time to keep the notification visible, in milliseconds.

    `None` or `-1` uses the server's default; `0` requests no expiry. The server can
    ignore this hint or apply its own policy, especially for critical notifications.
    """

    resident: bool | None = None
    """
    Whether to retain the notification after an action is invoked.

    The user or application must remove resident notifications; requires persistence
    support from the notification server.
    """

    transient: bool | None = None
    """
    Whether to bypass notification history or persistence.

    Requires support from the desktop notification server.
    """

    suppress_sound: bool | None = None
    """
    Whether to ask the server to suppress notification sounds.

    Useful when the application plays its own sound.
    """

    action_key_as_icon_name: bool | None = None
    """
    Whether to interpret action identifiers as desktop icon names.

    Requires server support. The bridge currently adds no custom Linux actions, so this
    has no effect on its action buttons.
    """


@ft.value(kw_only=True)
class WindowsOptions:
    """
    Presentation settings for Windows toast notifications.

    URI and file values refer to resources available on the Windows device, not files on
    the Python server. Windows version and packaging determine which toast features are
    available.
    """

    header: str | None = None
    """
    Header text used to group Windows notifications.

    The bridge uses a fixed header ID (`"header"`) and empty activation arguments; this
    field supplies only the visible title.
    """

    audio: WindowsNotificationSound | None = None
    """
    Windows system notification sound, or silence.

    See :class:`~flet_notifications.WindowsNotificationSound`. Custom audio URIs
    and arbitrary `ms-winsoundevent` names are not supported by this bridge.
    """

    duration: WindowsNotificationDuration | None = None
    """
    Requested toast display duration.

    See :class:`~flet_notifications.WindowsNotificationDuration`. The scenario
    and Windows settings can influence the actual duration.
    """

    scenario: WindowsScenario | None = None
    """
    Toast scenario controlling layout and default audio; see \
    :class:`flet_notifications.WindowsScenario`.
    """

    timestamp: int | None = None
    """
    Timestamp displayed on the toast, in milliseconds since the Unix epoch.

    Overrides the displayed time without changing when the notification is delivered.
    `None` uses the system's posting time.
    """

    subtitle: str | None = None
    """Additional text line displayed below the notification body."""

    images: list[str] | None = None
    """
    Image URI strings to include in the toast.

    Use URIs accessible to Windows, such as `file:///C:/images/status.png`. The bridge
    uses default image placement and empty alternative text.
    """

    bindings: dict[str, str] | None = None
    """
    Substitution values for named bindings in Windows toast content.

    Keys identify bindings and values provide the text to substitute. These values do
    not create additional rows or progress bars by themselves.
    """


@ft.value(kw_only=True)
class WebOptions:
    """
    Browser Notification API options reserved by the Python API.

    Note:
        The Dart bridge currently creates default web notification details and does not
        forward any fields in this class. Setting these options has no effect. Browser
        defaults apply.
    """

    direction: str | None = None
    """Text direction (`"auto"`, `"ltr"`, or `"rtl"`); currently not forwarded."""

    badge_url: str | None = None
    """URL of a compact badge image; currently not forwarded."""

    icon_url: str | None = None
    """URL of the notification icon; currently not forwarded."""

    image_url: str | None = None
    """URL of a larger notification image; currently not forwarded."""

    lang: str | None = None
    """BCP 47 language tag, such as `"en-GB"`; currently not forwarded."""

    require_interaction: bool | None = None
    """Whether to remain visible until user interaction; currently not forwarded."""

    is_silent: bool | None = None
    """Whether to suppress sound and vibration; currently not forwarded."""

    renotify: bool | None = None
    """
    Whether replacing a notification alerts the user again; currently not forwarded.
    """

    timestamp: int | None = None
    """Event timestamp in Unix epoch milliseconds; currently not forwarded."""


@ft.value(kw_only=True)
class NotificationOptions:
    """
    Platform-specific details for a notification.

    Pass this object to :meth:`flet_notifications.LocalNotifications.show`,
    :meth:`flet_notifications.LocalNotifications.schedule`, or
    :meth:`flet_notifications.LocalNotifications.periodically_show`. Only the current
    platform's entry is used. Unset entries use the bridge defaults. Common arguments
    such as title, actions, style, progress, and grouping are passed directly to those
    methods.

    Example:
        ```python
        import flet_notifications as ftn

        options = ftn.NotificationOptions(
            android=ftn.AndroidOptions(silent=True),
            iOS=ftn.DarwinOptions(interruption_level=ftn.InterruptionLevel.PASSIVE),
        )
        await notifications.show(id=1, title="Background update", options=options)
        ```
    """

    android: AndroidOptions | None = None
    """Details used when running on Android."""

    iOS: DarwinOptions | None = None
    """Details used when running on iOS."""

    macOS: DarwinOptions | None = None
    """Details used when running on macOS."""

    linux: LinuxOptions | None = None
    """Details used when running on Linux."""

    windows: WindowsOptions | None = None
    """Details used when running on Windows."""

    web: WebOptions | None = None
    """Reserved browser details; currently not forwarded by the bridge."""
