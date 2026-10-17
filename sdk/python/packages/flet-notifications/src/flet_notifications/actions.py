"""Action buttons and inline-reply inputs for notifications."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class NotificationActionInput:
    """Inline-reply input attached to a notification action.

    Maps to `AndroidNotificationActionInput` on Android, the text variant of
    `DarwinNotificationAction` on iOS/macOS and `WindowsInput` on Windows.
    """

    label: str = ""  # placeholder / button title over the text field
    choices: list[str] = field(default_factory=list)  # quick-reply suggestions
    allow_free_form_input: bool = True
    allowed_mime_types: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "choices": list(self.choices),
            "allow_free_form_input": self.allow_free_form_input,
            "allowed_mime_types": list(self.allowed_mime_types),
        }


@dataclass(kw_only=True)
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

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "destructive": self.destructive,
            "foreground": self.foreground,
            "cancel_notification": self.cancel_notification,
            "input": self.input.to_dict() if self.input else None,
        }
