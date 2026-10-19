from dataclasses import field

import flet as ft

__all__ = ["NotificationAction", "NotificationActionInput"]


@ft.value(kw_only=True)
class NotificationActionInput:
    """
    Input collected when a notification action is selected.

    Used by :attr:`flet_notifications.NotificationAction.input`. Android supports reply
    choices, free-form text, and MIME-type hints. iOS/macOS use a text-input action;
    Windows uses a separate text box associated with the action ID. The bridge does not
    forward custom action inputs on Linux or Web.
    """

    label: str = ""
    """
    User-visible label describing the input.

    On Android, labels the reply input. On iOS/macOS, supplies the text-input button
    title and placeholder; an empty label uses the action title for the button. On
    Windows, supplies the text box title and placeholder.
    """

    choices: list[str] = field(default_factory=list)
    """
    Suggested reply strings offered by Android.

    An empty list provides no predefined choices. Not forwarded on other platforms.
    """

    allow_free_form_input: bool = True
    """
    Whether Android lets the user type an arbitrary reply.

    Set to `False` with :attr:`choices` to restrict Android replies to suggestions. This
    flag is not forwarded on iOS/macOS or Windows.
    """

    allowed_mime_types: list[str] = field(default_factory=list)
    """
    MIME types accepted by Android's remote input, such as `"image/png"`.

    An empty list requests no MIME-type-specific input. The event model exposes text
    responses; it does not provide a dedicated attachment-result field. Not forwarded on
    other platforms.
    """


@ft.value(kw_only=True)
class NotificationAction:
    """
    Button attached to a notification on Android, iOS, macOS, or Windows.

    Selections are reported through
    :attr:`flet_notifications.LocalNotifications.on_action`, with :attr:`id` in
    :attr:`flet_notifications.NotificationEvent.action_id`. The bridge does not
    currently forward custom action buttons to Linux or Web.

    For inline replies, set :attr:`input`. Reply text is available in
    :attr:`flet_notifications.NotificationEvent.input`; Windows also returns input
    values in the event's inherited `data` mapping.
    """

    id: str
    """
    Nonempty identifier returned when the action is selected.

    Choose distinct IDs within a notification so handlers can distinguish its buttons.
    Windows also uses this ID to identify an associated input.
    """

    title: str
    """Nonempty button label displayed by the operating system."""

    destructive: bool = False
    """
    Whether iOS/macOS should style the action as destructive.

    This changes presentation, not the action's behavior;
    Android and Windows ignore the flag.
    """

    foreground: bool = True
    """
    Whether selecting the action brings the app to the foreground.

    Used on Android and iOS/macOS. With `False`, those platforms may run the background
    handler, which queues the event for replay when the service next initializes. Python
    handlers do not execute inside that background isolate. Windows actions currently
    use dismiss activation regardless of this flag.
    """

    cancel_notification: bool = True
    """
    Whether Android dismisses the notification when this action is selected.

    Not forwarded on other platforms.
    """

    input: NotificationActionInput | None = None
    """Optional reply input associated with this action."""
