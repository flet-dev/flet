from enum import Enum
from typing import Annotated

import flet as ft
from flet.utils.validation import V

__all__ = [
    "DarwinInterruptionLevel",
    "DarwinOptions",
]


class DarwinInterruptionLevel(Enum):
    """
    Presentation urgency on iOS 15+ and macOS 12+.

    Set :attr:`flet_notifications.DarwinOptions.interruption_level` to control delivery
    timing and how a notification interacts with system interruption controls. Available
    presentation and sound permissions still apply.
    """

    PASSIVE = "passive"
    """
    Adds the notification quietly to the notification list.

    Does not light the screen or play a sound. Appropriate for information the user can
    read later, such as a recommendation or routine status update.
    """

    ACTIVE = "active"
    """
    Presents the notification immediately, lighting the screen and allowing sound.

    Uses ordinary notification behavior and respects Focus and notification summary
    settings. Appropriate for updates that merit attention without requiring an
    immediate response.
    """

    TIME_SENSITIVE = "timeSensitive"
    """
    Presents time-sensitive information immediately, subject to user settings.

    Can bypass notification summaries and Focus when the user allows time-sensitive
    notifications. Add the Time Sensitive Notifications capability to the iOS app. Use
    for events that need attention now, such as an imminent delivery, rather than
    ordinary updates.
    """

    CRITICAL = "critical"
    """
    Presents a critical alert that can sound through mute and Do Not Disturb.

    Reserve for urgent health or safety alerts. Requires:

    - Apple's approval of the critical-alert entitlement for the app, which Apple
      grants on request to apps such as medical, health, and public-safety apps.
      Once approved, enable the capability on the app's App ID.
    - The [entitlement](https://flet.dev/docs/publish/ios#entitlements) in the app,
      declared in `pyproject.toml`:

      ```toml
      [tool.flet.ios.entitlement]
      "com.apple.developer.usernotifications.critical-alerts" = true
      ```

      Use `[tool.flet.macos.entitlement]` for macOS.
    - The user's critical-alert authorization, requested with `critical=True` in
      :meth:`flet_notifications.Notifications.request_permissions`.
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

    badge_number: Annotated[int | None, V.ge(0)] = None
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

    interruption_level: DarwinInterruptionLevel | None = None
    """
    Delivery urgency on iOS 15+ and macOS 12+.

    Note:
        See :class:`flet_notifications.DarwinInterruptionLevel` for presentation
        behavior and capability requirements. `None` leaves the level to the system.
    """

    critical_sound_volume: Annotated[float | None, V.between(0.0, 1.0)] = None
    """
    Volume of a critical-alert sound, from `0.0` to `1.0`.

    Note:
        Used only for critical alerts on iOS 12+ and macOS 10.14+. Requires the
        critical-alert entitlement and authorization; see
        :attr:`flet_notifications.DarwinInterruptionLevel.CRITICAL`.
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
