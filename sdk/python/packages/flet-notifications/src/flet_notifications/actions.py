from dataclasses import field

import flet as ft

__all__ = ["NotificationAction", "NotificationActionInput"]


@ft.value(kw_only=True)
class NotificationActionInput:
    """
    Input collected when a notification action is selected.

    Used by :attr:`flet_notifications.NotificationAction.input`.

    Note:
        Android supports reply choices, free-form text, and MIME-type hints. iOS/macOS
        use a text-input action; Windows uses a separate text box associated with the
        action ID. Custom action inputs are not supported on Linux or Web.
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

    allow_free_form_input: bool = True
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
    Button attached to a notification on Android, iOS, macOS, Windows, or Web.

    Selections are reported through
    :attr:`flet_notifications.Notifications.on_action`, with :attr:`id` in
    :attr:`flet_notifications.NotificationActionEvent.action_id`.

    For inline replies, set :attr:`input`. Reply text is available in
    :attr:`flet_notifications.NotificationActionEvent.input`.

    Note:
        Windows also returns input values in the event's inherited `data` mapping.
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
        Supported only on iOS and macOS.
    """

    foreground: bool = True
    """
    Whether selecting the action brings the app to the foreground.

    Note:
        Supported only on Android, iOS, and macOS. With `False`, those platforms may
        queue the event for replay when the service next initializes. Python handlers
        do not execute inside the background isolate.

        Windows actions use dismiss activation regardless of this flag. Web ignores this
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
        Supported only on Android, iOS, macOS, and Windows. On Web, the action remains a
        regular button without a reply input.
    """
