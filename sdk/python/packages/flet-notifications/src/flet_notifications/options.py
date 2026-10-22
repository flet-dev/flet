from datetime import datetime
from enum import Enum

import flet as ft
from flet_notifications.channels import NotificationChannel
from flet_notifications.styles import Style
from flet_notifications.types import (
    AndroidNotificationCategory,
    AndroidNotificationFlag,
    GroupAlertBehavior,
    LinuxNotificationCategory,
    WebNotificationDirection,
    WindowsNotificationDuration,
    WindowsNotificationSound,
)

__all__ = [
    "AndroidGroup",
    "AndroidOptions",
    "AndroidProgress",
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

    Note:
        On Android 8.0 and later, channel :class:`~flet_notifications.Importance`
        determines interruption behavior instead. Priority is a presentation hint; it
        does not override the user's notification preferences.
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

    Note:
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

    Note:
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

    Note:
        Windows normally loops the alarm sound unless audio options override it.
    """

    INCOMING_CALL = "incomingCall"
    """Use the incoming-call layout with looping call audio by default."""

    URGENT = "urgent"
    """
    Request an urgent notification that may break through Do Not Disturb.

    Note:
        Requires a Windows version and user settings that permit urgent notifications.
    """


@ft.value(kw_only=True)
class AndroidProgress:
    """
    Progress bar shown in an Android notification.

    Set it as :attr:`flet_notifications.AndroidOptions.progress`. To advance the bar,
    show the notification again with the same ID and an updated :attr:`value`;
    combine with :attr:`flet_notifications.AndroidOptions.only_alert_once` to avoid
    alerting on each update.
    """

    value: int = 0
    """Current progress, between `0` and :attr:`max`."""

    max: int = 100
    """Value at which the progress bar is full."""

    indeterminate: bool = False
    """
    Whether to show ongoing activity without a known completion amount.

    When `True`, :attr:`value` and :attr:`max` are ignored.
    """


@ft.value(kw_only=True)
class AndroidGroup:
    """
    Group of related notifications bundled together in the Android notification tray.

    Set it as :attr:`flet_notifications.AndroidOptions.group`. Notifications sharing a
    :attr:`key` are bundled; one of them can act as the group's summary. This is
    distinct from a notification-channel group and from Apple threads (see
    :attr:`flet_notifications.DarwinOptions.thread_identifier`).
    """

    key: str
    """Identifier shared by every notification in the group."""

    summary: bool = False
    """Whether this notification summarizes the other notifications in the group."""

    alert_behavior: GroupAlertBehavior = GroupAlertBehavior.ALL
    """
    Which members of the group may sound or vibrate.

    Apply the same behavior to the group's children and summary for consistent results.
    """


@ft.value(kw_only=True)
class AndroidOptions:
    """
    Android-specific notification settings.

    Importance, sound, vibration, lights, and badge behavior belong to the
    notification's :attr:`channel`; see
    :class:`~flet_notifications.NotificationChannel`.
    """

    channel: NotificationChannel | str | None = None
    """
    Channel the notification is posted to.

    Pass a :class:`~flet_notifications.NotificationChannel` to create the channel on
    first use, or the ID of a channel created earlier with
    :meth:`flet_notifications.LocalNotifications.create_notification_channel`. A
    missing channel referenced only by ID is created with the name `"Notifications"`
    and default settings. `None` uses the extension's default channel.

    Note:
        Before Android 8.0, which has no channels, the channel's sound, vibration,
        lights, and importance apply to the individual notification.
    """

    style: Style | None = None
    """
    Expanded layout of the notification; see :class:`~flet_notifications.Style`.

    `None` uses the standard layout.
    """

    progress: AndroidProgress | None = None
    """
    Progress bar shown in the notification.

    `None` shows no progress bar.
    """

    group: AndroidGroup | None = None
    """
    Group this notification belongs to.

    `None` leaves the notification ungrouped.
    """

    icon: str | None = None
    """
    Bundled drawable resource name for this notification's small icon.

    Supply the resource name without a file extension, such as `"ic_stat_notify"`.
    `None` uses :attr:`flet_notifications.LocalNotifications.default_icon`.

    Include the drawable in the Android app.

    Note:
        Use a white silhouette on a transparent background, with resources sized for
        the supported screen densities. Android Studio's
        [notification icon wizard](https://developer.android.com/studio/write/create-app-icons#create-notification)
        generates the appropriate drawable variants. Android uses the icon's alpha
        channel to determine its visible shape; an opaque background can appear as a
        solid block.
    """

    priority: Priority | None = None
    """
    Notification priority.

    Note:
        Used on Android 7.1 and earlier. On Android 8.0+, the :attr:`channel`'s
        :attr:`~flet_notifications.NotificationChannel.importance` applies instead.
    """

    auto_cancel: bool | None = None
    """Whether tapping the notification automatically dismisses it."""

    ongoing: bool | None = None
    """
    Whether to mark the notification as an ongoing activity.

    Note:
        Android controls whether the user can dismiss ongoing notifications; this does
        not start a foreground service.
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

    Note:
        When disabled, the color accents the app icon. Android usually restricts
        background coloring to foreground-service notifications.
    """

    large_icon: str | None = None
    """
    Drawable resource name or absolute device file path for the large icon.

    Paths beginning with `/` or containing a backslash are treated as file paths;
    other strings are drawable names.

    Note:
        Content URIs are not supported by this field. For richer image sources, see
        :class:`~flet_notifications.AndroidIcon`.
    """

    only_alert_once: bool | None = None
    """
    Whether sound, vibration, and ticker alert only on the first display.

    Enable when repeatedly updating the same notification, such as a progress
    notification, without alerting on each update.
    """

    show_timestamp: bool | None = None
    """
    Whether to display the notification timestamp.

    Set :attr:`timestamp` to override the displayed time.
    """

    timestamp: datetime | None = None
    """
    Time displayed on the notification.

    When `None`, uses the notification's posting time. This does not schedule delivery;
    use :meth:`flet_notifications.LocalNotifications.schedule` for that.

    Timezone-aware values preserve their instant. A naive datetime is interpreted in
    the Python host's local timezone.
    """

    uses_chronometer: bool | None = None
    """
    Whether to show elapsed time from :attr:`timestamp` instead of a timestamp.

    Android updates the minutes and seconds automatically, which is useful for ongoing
    calls or timers.
    """

    chronometer_count_down: bool | None = None
    """
    Whether the chronometer counts down rather than up.

    Note:
        Supported only on Android 7.0+. Requires :attr:`uses_chronometer` to be enabled.
    """

    sub_text: str | None = None
    """
    Supplementary information displayed in the notification template.

    Note:
        Android 7.0+ places this in the header. Earlier versions use the same line as
        the progress bar, so avoid using both on those versions.
    """

    number: int | None = None
    """
    Notification count displayed by launchers that support badge numbers.

    Note:
        Ignored when the launcher does not support this feature.
    """

    visibility: Visibility | None = None
    """
    How much content may appear on a secure lock screen.

    `None` leaves the choice to Android. See :class:`flet_notifications.Visibility`.
    """

    timeout_after: ft.DurationValue | None = None
    """
    Time after posting before Android cancels the notification.

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

    Note:
        Requires Android manifest configuration and, on Android 14+, full-screen-intent
        access. See
        :meth:`flet_notifications.LocalNotifications.request_full_screen_intent_permission`.
        Android may show a heads-up notification instead. A full-screen launch is
        reported through :attr:`flet_notifications.LocalNotifications.on_tap`.
    """

    shortcut_id: str | None = None
    """
    ID of a published, long-lived sharing shortcut linked to the notification.

    Note:
        On Android 11+, this can help a messaging notification appear in the
        conversation section. This extension does not create the shortcut.
    """

    additional_flags: AndroidNotificationFlag | int | None = None
    """
    Additional native Android notification flags, combined using `|`.

    For example, combine :attr:`flet_notifications.AndroidNotificationFlag.INSISTENT`
    and :attr:`flet_notifications.AndroidNotificationFlag.NO_CLEAR` to request repeating
    audio and retention when the user presses Clear all.

    Note:
        Android may restrict the effect of individual flags.

    A raw integer bitmask is also accepted for Android flags not represented by
    :class:`flet_notifications.AndroidNotificationFlag`. Combine integer flag values
    using `|` in the same way. See Android's [notification
    flags](https://developer.android.com/reference/android/app/Notification#flags) for
    their meanings and restrictions.

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

    led_on_duration: ft.DurationValue | None = None
    """
    Time the notification LED remains on during each blink.

    Note:
        Used only before Android 8.0, together with the :attr:`channel`'s
        :attr:`~flet_notifications.NotificationChannel.led_color`. On newer versions,
        the device controls the blinking pattern.
    """

    led_off_duration: ft.DurationValue | None = None
    """
    Time the notification LED remains off between blinks.

    Note:
        Used only before Android 8.0, together with the :attr:`channel`'s
        :attr:`~flet_notifications.NotificationChannel.led_color`. On newer versions,
        the device controls the blinking pattern.
    """


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

    Note:
        Requires :attr:`present_sound`. With sound presentation enabled, `None` uses the
        default notification sound. Apple limits supported file formats and custom-sound
        duration.
    """

    badge_number: int | None = None
    """
    Number to apply to the application icon badge.

    Use `0` to clear the badge, a positive number to set it, or `None` to leave it
    unchanged.

    Note:
        Requires badge authorization.
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

    Note:
        See :class:`flet_notifications.InterruptionLevel` for presentation behavior and
        capability requirements. `None` leaves the level to the system.
    """

    critical_sound_volume: float | None = None
    """
    Volume of a critical-alert sound, from `0.0` to `1.0`.

    Note:
        Used only for critical alerts on iOS 12+ and macOS 10.14+. Requires the
        critical-alert entitlement and authorization; see
        :attr:`flet_notifications.InterruptionLevel.CRITICAL`.
    """

    attachments: list[str] | None = None
    """
    Local device file paths of media to attach to the notification.

    Note:
        Supported only on iOS 10+ and macOS 10.14+. Files must be accessible to the app
        and use a media format accepted by Apple's notification framework. These are
        device paths, not URLs or paths on the Python server.
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
    Whether to show a foreground banner.

    `None` inherits the enabled initialization default.

    Note:
        Supported only on iOS 14+ and macOS 11+.
    """

    present_list: bool | None = None
    """
    Whether to add a foreground notification to Notification Center.

    `None` inherits the enabled initialization default.

    Note:
        Supported only on iOS 14+ and macOS 11+.
    """


@ft.value(kw_only=True)
class LinuxOptions:
    """
    Hints for a Linux freedesktop notification server.

    Note:
        Feature support varies by desktop and notification daemon. Unsupported hints may
        be ignored. This extension does not expose server-capability queries.
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

    Note:
        See :class:`~flet_notifications.LinuxNotificationCategory`. The notification
        server determines the presentation and may ignore this hint.
    """

    urgency: LinuxUrgency | None = None
    """Urgency hint."""

    timeout: ft.DurationValue | None = None
    """
    Requested time to keep the notification visible.

    Integer values are interpreted as milliseconds. `None` or `-1` uses the notification
    server's timeout; `0` requests no expiry.

    Note:
        The server can ignore this hint or apply its own policy, especially for critical
        notifications.
    """

    resident: bool | None = None
    """
    Whether to retain the notification after an action is invoked.

    Note:
        The user or application must remove resident notifications; requires persistence
        support from the notification server.
    """

    transient: bool | None = None
    """
    Whether to bypass notification history or persistence.

    Note:
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

    Note:
        Custom notification action buttons are not supported on Linux, so this setting
        has no effect.
    """


@ft.value(kw_only=True)
class WindowsOptions:
    """
    Presentation settings for Windows toast notifications.

    Note:
        URI and file values refer to resources available on the Windows device, not
        files on the Python server. Windows version and packaging determine which toast
        features are available.
    """

    header: str | None = None
    """
    Header text used to group Windows notifications.

    Sets the visible title of a header with the fixed ID `"header"` and no activation
    arguments.
    """

    audio: WindowsNotificationSound | None = None
    """
    Windows system notification sound, or silence.

    See :class:`~flet_notifications.WindowsNotificationSound`. Custom audio URIs and
    arbitrary `ms-winsoundevent` names are not supported.
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

    timestamp: datetime | None = None
    """
    Time displayed on the toast.

    Overrides the displayed time without changing when the notification is delivered.
    `None` uses the system's posting time.

    Timezone-aware values preserve their instant. A naive datetime is interpreted in
    the Python host's local timezone.
    """

    subtitle: str | None = None
    """Additional text line displayed below the notification body."""

    images: list[str] | None = None
    """
    Image URI strings to include in the toast.

    Use URIs accessible to Windows, such as `file:///C:/images/status.png`. Images use
    default placement and empty alternative text.
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
    Browser-specific presentation options for
    :meth:`flet_notifications.LocalNotifications.show`.

    Note:
        Individual options may be ignored depending on the browser and operating system.
        Notification permission is still required. Image URLs must be accessible to the
        browser; local Python file paths are not resolved or uploaded by these options.

    See the browser [notification
    options](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/showNotification#parameters)
    for platform support and restrictions.
    """

    direction: WebNotificationDirection | None = None
    """
    Requested text direction.

    The browser may ignore this hint.
    """

    badge_url: str | None = None
    """
    URL of a compact image used where the full notification icon will not fit.

    Some platforms mask this image to a monochrome silhouette.
    """

    icon_url: str | None = None
    """URL of an image displayed alongside the notification's title and body."""

    image_url: str | None = None
    """URL of a larger image displayed within the notification's content."""

    lang: str | None = None
    """
    BCP 47 language tag for the content, such as `"en-GB"` or `"ja-JP"`.

    This labels the language; it does not translate the title or body.
    """

    require_interaction: bool | None = None
    """
    Request that the notification remain visible until clicked or dismissed.

    The browser and operating system determine whether this request is honored.
    """

    is_silent: bool | None = None
    """
    Whether to suppress notification sound and vibration.

    `False` permits alerting but does not override browser or system sound settings.
    """

    renotify: bool | None = None
    """
    Whether replacing a notification should alert the user again.

    Call :meth:`flet_notifications.LocalNotifications.show` with the same `id` to
    replace a notification. The backend uses that ID as the browser notification tag.
    Sound can still be suppressed by :attr:`is_silent` or user settings.
    """

    timestamp: datetime | None = None
    """
    Time associated with the notification's event.

    Can represent an earlier event, such as a message received while offline. This is
    display metadata; it does not schedule notification delivery.

    Timezone-aware values preserve their instant. A naive datetime is interpreted in
    the Python host's local timezone.
    """


@ft.value(kw_only=True)
class NotificationOptions:
    """
    Platform-specific details for a notification.

    Pass this object to :meth:`flet_notifications.LocalNotifications.show`,
    :meth:`flet_notifications.LocalNotifications.schedule`, or
    :meth:`flet_notifications.LocalNotifications.periodically_show`. Only the current
    platform's entry is used. Unset entries use the bridge defaults. Cross-platform
    content such as title, body, payload, and actions is passed directly to those
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
    """Details used when running in a web browser."""
