from datetime import datetime
from enum import Enum
from typing import Annotated

import flet as ft
from flet.utils.validation import V

__all__ = [
    "WindowsNotificationDuration",
    "WindowsNotificationSound",
    "WindowsOptions",
    "WindowsProgress",
    "WindowsScenario",
]


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


class WindowsNotificationDuration(Enum):
    """
    How long Windows should display a toast notification.

    Set :attr:`flet_notifications.WindowsOptions.duration`. The scenario and
    Windows settings can influence how long a notification remains visible.
    """

    SHORT = "short"
    """Request the shorter toast display duration."""

    LONG = "long"
    """Request the longer toast display duration."""


class WindowsNotificationSound(Enum):
    """
    Sound choices for Windows notifications.

    Note:
        Set :attr:`flet_notifications.WindowsOptions.audio`. These members select
        Windows system sounds or silence. Custom sound URIs are not supported.
    """

    DEFAULT = "default"
    """Play the standard Windows notification sound."""

    IM = "im"
    """Play the Windows instant-message notification sound."""

    MAIL = "mail"
    """Play the Windows email notification sound."""

    REMINDER = "reminder"
    """Play the Windows reminder notification sound."""

    SMS = "sms"
    """Play the Windows text-message notification sound."""

    SILENT = "silent"
    """Disable audio for this toast."""


@ft.value(kw_only=True)
class WindowsProgress:
    """
    Progress bar shown in a Windows toast notification.

    Set it as :attr:`flet_notifications.WindowsOptions.progress`. To advance the bar
    without popping the toast up again, call
    :meth:`flet_notifications.Notifications.update_windows_progress`.
    """

    status: Annotated[str, V.non_empty()]
    """Text describing the activity, such as `"Downloading..."`."""

    value: Annotated[int, V.ge(0), V.le_field("max")] = 0
    """Current progress, between `0` and :attr:`max`."""

    max: Annotated[int, V.gt(0)] = 100
    """Value at which the progress bar is full."""

    indeterminate: bool = False
    """
    Whether to show ongoing activity without a known completion amount.

    When `True`, :attr:`value` and :attr:`max` are ignored.
    """

    title: str | None = None
    """Title shown above the progress bar."""

    label: str | None = None
    """
    Text shown instead of the percentage, such as `"3/10"` for discrete progress.
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

    progress: WindowsProgress | None = None
    """Progress bar shown in the toast."""

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
