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
    Button attached to a notification on Android, iOS, macOS, Windows, or Web.

    Selections are reported through
    :attr:`flet_notifications.LocalNotifications.on_action`, with :attr:`id` in
    :attr:`flet_notifications.NotificationEvent.action_id`.

    For inline replies, set :attr:`input`. Reply text is available in
    :attr:`flet_notifications.NotificationEvent.input`; Windows also returns input
    values in the event's inherited `data` mapping.
    """

    id: str
    """
    Nonempty identifier returned when the action is selected.

    Choose distinct IDs within a notification so handlers can distinguish its buttons.

    Note:
        Windows also uses this ID to identify an associated input.
    """

    title: str
    """
    Nonempty button label displayed by the operating system.

    Note:
        Linux does not support custom action buttons through this extension. On Web,
        browser and operating-system support determine whether buttons appear and how
        many can be shown. See browser [notification action support](https://developer.mozilla.org/en-US/docs/Web/API/Notification/actions#browser_compatibility).
        Keep essential actions available in the app as well.
    """

    destructive: bool = False
    """
    Whether to style the action as destructive.

    This changes presentation, not the action's behavior.

    Note:
        Supported only on iOS/macOS. Android, Windows, and Web ignore this flag.
    """

    foreground: bool = True
    """
    Whether selecting the action brings the app to the foreground.

    On Android and iOS/macOS, `False` allows the background handler to queue the event
    for replay when the service next initializes. Python handlers do not execute inside
    that background isolate.

    Note:
        Supported only on Android and iOS/macOS. Windows actions use dismiss activation
        regardless of this flag. Web ignores this flag; the upstream service worker
        delivers the click to an open app window or opens the app if none is available.
    """

    cancel_notification: bool = True
    """
    Whether to dismiss the notification when this action is selected.

    Note:
        Supported only on Android. This flag is not forwarded on other platforms.
    """

    input: NotificationActionInput | None = None
    """
    Reply input associated with this action.

    Note:
        Supported on Android, iOS, macOS, and Windows. On Web, the action remains a
        regular button; the input configuration is not forwarded. Linux does not
        support custom action inputs through this extension.
    """
