"""flet-notifications: cross-platform local notifications for Flet apps.

Wraps the battle-tested `flutter_local_notifications` Flutter plugin and
exposes it as a native Flet service (`ft.Service`), following the same
extension architecture as `flet-ads` / `flet-yandex-ads`.
"""

from flet_notifications.actions import NotificationAction, NotificationActionInput
from flet_notifications.base import (
    NotificationError,
    NotificationErrorCode,
    NotificationEvent,
    ResponseType,
)
from flet_notifications.channels import NotificationChannel
from flet_notifications.events import (
    ActiveNotification,
    LaunchDetails,
    PendingNotification,
)
from flet_notifications.local_notifications import LocalNotifications
from flet_notifications.options import (
    AndroidOptions,
    DarwinOptions,
    InterruptionLevel,
    LinuxOptions,
    LinuxUrgency,
    NotificationOptions,
    Priority,
    Visibility,
    WebOptions,
    WindowsOptions,
    WindowsScenario,
)
from flet_notifications.styles import (
    AndroidIcon,
    BigPictureStyle,
    BigTextStyle,
    InboxStyle,
    Message,
    MessagingStyle,
    Person,
    Style,
)
from flet_notifications.types import (
    AndroidScheduleMode,
    DateTimeComponents,
    GroupAlertBehavior,
    Importance,
    RepeatInterval,
)

__version__ = "0.1.4"

__all__ = [
    "ActiveNotification",
    "AndroidIcon",
    "AndroidOptions",
    "AndroidScheduleMode",
    "BigPictureStyle",
    "BigTextStyle",
    "DarwinOptions",
    "DateTimeComponents",
    "GroupAlertBehavior",
    "Importance",
    "InboxStyle",
    "InterruptionLevel",
    "LaunchDetails",
    "LinuxOptions",
    "LinuxUrgency",
    "LocalNotifications",
    "Message",
    "MessagingStyle",
    "NotificationAction",
    "NotificationActionInput",
    "NotificationChannel",
    "NotificationError",
    "NotificationErrorCode",
    "NotificationEvent",
    "NotificationOptions",
    "PendingNotification",
    "Person",
    "Priority",
    "RepeatInterval",
    "ResponseType",
    "Style",
    "Visibility",
    "WebOptions",
    "WindowsOptions",
    "WindowsScenario",
]
