"""Action buttons and inline-reply inputs for notifications."""

from dataclasses import field

import flet as ft


@ft.value(kw_only=True)
class NotificationActionInput:
    """Inline-reply input attached to a notification action.

    Maps to `AndroidNotificationActionInput` on Android, the text variant of
    `DarwinNotificationAction` on iOS/macOS and `WindowsInput` on Windows.
    """

    label: str = ""  # placeholder / button title over the text field
    choices: list[str] = field(default_factory=list)  # quick-reply suggestions
    allow_free_form_input: bool = True
    allowed_mime_types: list[str] = field(default_factory=list)


@ft.value(kw_only=True)
class NotificationAction:
    """A button shown on a notification.

    When the button is pressed, `on_action` fires with `action_id == id`.
    If `input` is set, the OS shows an inline-reply field and the typed text
    arrives as `NotificationEvent.input`.
    """

    id: str
    title: str
    destructive: bool = False  # iOS/macOS: render as destructive
    foreground: bool = True  # bring the app to the foreground on press
    cancel_notification: bool = True  # Android: dismiss the notification
    input: NotificationActionInput | None = None
