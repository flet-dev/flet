from dataclasses import dataclass, field
from enum import Enum
from typing import Annotated

import flet as ft
from flet.utils.validation import V
from flet_notifications.android import AndroidOptions
from flet_notifications.darwin import DarwinOptions
from flet_notifications.linux import LinuxOptions
from flet_notifications.web import WebOptions
from flet_notifications.windows import WindowsOptions

__all__ = [
    "ActiveNotification",
    "DateTimeComponents",
    "NotificationAction",
    "NotificationActionInput",
    "NotificationOptions",
    "PendingNotification",
    "RepeatInterval",
]


class RepeatInterval(Enum):
    """
    Fixed intervals for :meth:`flet_notifications.Notifications.periodically_show`.

    The first notification is delivered one interval after scheduling. For a particular
    local time, such as 09:00 each day, use
    :class:`flet_notifications.DateTimeComponents` with
    :meth:`flet_notifications.Notifications.schedule` instead.

    Note:
        Supported only on Android, iOS, and macOS.
    """

    EVERY_MINUTE = "everyMinute"
    """Repeats every minute, starting one minute after scheduling."""

    HOURLY = "hourly"
    """Repeats every hour, starting one hour after scheduling."""

    DAILY = "daily"
    """Repeats every day, starting one day after scheduling."""

    WEEKLY = "weekly"
    """Repeats every week, starting one week after scheduling."""


class DateTimeComponents(Enum):
    """
    Calendar components to match when repeating a scheduled notification.

    Used by :meth:`flet_notifications.Notifications.schedule`. The next matching
    date can precede the full date supplied in `when`: matching only the time repeats
    from the next occurrence of that time.

    Note:
        Calendar recurrence is supported only on Android, iOS, and macOS. Windows
        ignores
        these components and schedules a single delivery.
    """

    TIME = "time"
    """Repeats daily at the hour, minute, and second of the scheduled time."""

    DAY_OF_WEEK_AND_TIME = "dayOfWeekAndTime"
    """Repeats weekly on the weekday and at the time of the scheduled date."""

    DAY_OF_MONTH_AND_TIME = "dayOfMonthAndTime"
    """Repeats monthly on the day of the month and at the scheduled time."""

    DATE_AND_TIME = "dateAndTime"
    """Repeats yearly on the month and day and at the time of the scheduled date."""


@ft.value(kw_only=True)
class NotificationActionInput:
    """
    Input collected when a notification action is selected.

    Used by :attr:`flet_notifications.NotificationAction.input`.

    Note:
        Android supports reply choices, free-form text, and MIME-type hints. iOS/macOS
        use a text-input action; Windows uses a separate text box associated with the
        action ID. Linux and Web show the action as a regular button without an input.
    """

    label: str | None = None
    """
    User-visible label describing the input.

    Note:
        On Android, labels the reply input. On iOS/macOS, supplies the text-input button
        title and placeholder; `None` uses the action title for the button. On
        Windows, supplies the text box title and placeholder.
    """

    choices: list[str] = field(default_factory=list)
    """
    Suggested reply strings.

    An empty list provides no predefined choices.

    Note:
        Supported only on Android.
    """

    allow_free_form: bool = True
    """
    Whether to allow the user to type an arbitrary reply.

    Set to `False` with :attr:`choices` to restrict replies to suggestions.

    Note:
        Supported only on Android. Reply inputs on iOS, macOS, and Windows allow
        free-form text.
    """

    allowed_mime_types: list[str] = field(default_factory=list)
    """
    Accepted reply MIME types, such as `"image/png"`.

    An empty list requests no MIME-type-specific input.

    Note:
        The event model exposes text responses, not a dedicated attachment-result field.
        MIME-type filtering is supported only on Android.
    """


@ft.value(kw_only=True)
class NotificationAction:
    """
    Button attached to a notification.

    Selections are reported through
    :attr:`flet_notifications.Notifications.on_action`, with :attr:`id` in
    :attr:`flet_notifications.NotificationActionEvent.action_id`.

    For inline replies, set :attr:`input`. Reply text is available in
    :attr:`flet_notifications.NotificationActionEvent.input`.

    Note:
        Windows also returns input values in the event's inherited `data` mapping.
    """

    id: Annotated[str, V.non_empty()]
    """
    Nonempty identifier returned when the action is selected.

    Choose distinct IDs within a notification so handlers can distinguish its buttons.

    Note:
        Windows also uses this ID to identify an associated input.
    """

    title: Annotated[str, V.non_empty()]
    """
    Nonempty button label displayed by the operating system.

    Note:
        On Linux, the desktop's notification server decides whether buttons appear. On
        Web, browser and operating-system support determine whether buttons appear and
        how many can be shown. See browser [notification action support](https://developer.mozilla.org/en-US/docs/Web/API/Notification/actions#browser_compatibility).
        Keep essential actions available in the app as well.
    """

    destructive: bool = False
    """
    Whether to style the action as destructive.

    This changes presentation, not the action's behavior.

    Note:
        Supported only on iOS and macOS.
    """

    foreground: bool = True
    """
    Whether selecting the action brings the app to the foreground.

    Note:
        Supported only on Android, iOS, and macOS. With `False`, those platforms may
        queue the event for replay when the service next initializes. Python handlers
        do not execute inside the background isolate.

        Windows actions use dismiss activation regardless of this flag. Linux ignores
        this flag and reports the action only while the app is running. Web ignores this
        flag; the upstream service worker delivers the click to an open app window or
        opens the app if none is available.
    """

    require_authentication: bool = False
    """
    Whether the user must unlock the device before the action runs.

    Use it for actions with consequences, such as deleting or paying.

    Note:
        Supported only on iOS and macOS.
    """

    cancel_notification: bool = True
    """
    Whether to dismiss the notification when this action is selected.

    Note:
        Supported only on Android.
    """

    input: NotificationActionInput | None = None
    """
    Reply input associated with this action.

    Note:
        Supported only on Android, iOS, macOS, and Windows. On Linux and Web, the action
        remains a regular button without a reply input.
    """


@dataclass
class PendingNotification:
    """
    Notification scheduled for future delivery.

    Returned by
    :meth:`flet_notifications.Notifications.get_pending`. This is a
    query snapshot, not an editable schedule; changing its fields does not update or
    cancel the native request. Unavailable values are `None`.
    """

    id: int
    """Identifier supplied when scheduling the notification."""

    title: str | None = None
    """Scheduled notification title, or `None` when unavailable."""

    body: str | None = None
    """Scheduled body text, or `None` when unavailable."""

    payload: str | None = None
    """Application payload stored with the scheduled notification, if any."""


@dataclass
class ActiveNotification:
    """
    Snapshot of a delivered notification that has not been removed.

    Returned by :meth:`flet_notifications.Notifications.get_active`.
    Availability of individual fields depends on the platform; unavailable values are
    `None`. Modifying this object does not change the notification.
    """

    id: int | None = None
    """Native notification identifier, or `None` when unavailable."""

    channel_id: str | None = None
    """Android notification-channel ID, or `None` when unavailable."""

    group_key: str | None = None
    """
    Android :attr:`flet_notifications.AndroidGroup.key`, or `None` when unavailable.
    """

    tag: str | None = None
    """Android notification tag, or `None` when unavailable."""

    title: str | None = None
    """Displayed title, or `None` when unavailable."""

    body: str | None = None
    """Displayed body text, or `None` when unavailable."""

    payload: str | None = None
    """Application payload when returned by the platform, otherwise `None`."""

    big_text: str | None = None
    """Expanded Android big-text content, or `None` when unavailable."""


@ft.value(kw_only=True)
class NotificationOptions:
    """
    Platform-specific details for a notification.

    Pass this object to :meth:`flet_notifications.Notifications.show`,
    :meth:`flet_notifications.Notifications.schedule`, or
    :meth:`flet_notifications.Notifications.periodically_show`. Only the current
    platform's entry is used. Unset entries use the bridge defaults. Cross-platform
    content such as title, body, payload, and actions is passed directly to those
    methods.

    Example:
        ```python
        import flet_notifications as ftn

        options = ftn.NotificationOptions(
            android=ftn.AndroidOptions(silent=True),
            ios=ftn.DarwinOptions(
                interruption_level=ftn.DarwinInterruptionLevel.PASSIVE
            ),
        )
        await notifications.show(id=1, title="Background update", options=options)
        ```
    """

    android: AndroidOptions | None = None
    """Details used when running on Android."""

    ios: DarwinOptions | None = None
    """Details used when running on iOS."""

    macos: DarwinOptions | None = None
    """Details used when running on macOS."""

    linux: LinuxOptions | None = None
    """Details used when running on Linux."""

    windows: WindowsOptions | None = None
    """Details used when running on Windows."""

    web: WebOptions | None = None
    """Details used when running in a web browser."""
