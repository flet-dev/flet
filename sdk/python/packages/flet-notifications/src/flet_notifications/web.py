from datetime import datetime
from enum import Enum

import flet as ft

__all__ = [
    "WebDirection",
    "WebOptions",
]


class WebDirection(Enum):
    """
    Text direction for a browser notification.

    Note:
        Used by :attr:`flet_notifications.WebOptions.direction`. Browsers may ignore
        this hint; it does not translate the notification's content.
    """

    AUTO = "auto"
    """Uses the browser's language-setting behavior to choose the text direction."""

    LEFT_TO_RIGHT = "leftToRight"
    """Requests left-to-right text layout."""

    RIGHT_TO_LEFT = "rightToLeft"
    """Requests right-to-left text layout."""


@ft.value(kw_only=True)
class WebOptions:
    """
    Browser-specific presentation options for
    :meth:`flet_notifications.Notifications.show`.

    Note:
        Individual options may be ignored depending on the browser and operating system.
        Notification permission is still required. Image URLs must be accessible to the
        browser; local Python file paths are not resolved or uploaded by these options.

    See the browser [notification
    options](https://developer.mozilla.org/en-US/docs/Web/API/ServiceWorkerRegistration/showNotification#parameters)
    for platform support and restrictions.
    """

    direction: WebDirection | None = None
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

    silent: bool | None = None
    """
    Whether to suppress notification sound and vibration.

    `False` permits alerting but does not override browser or system sound settings.
    """

    renotify: bool | None = None
    """
    Whether replacing a notification should alert the user again.

    Call :meth:`flet_notifications.Notifications.show` with the same `id` to
    replace a notification. The backend uses that ID as the browser notification tag.
    Sound can still be suppressed by :attr:`silent` or user settings.
    """

    timestamp: datetime | None = None
    """
    Time associated with the notification's event.

    Can represent an earlier event, such as a message received while offline. This is
    display metadata; it does not schedule notification delivery.

    Timezone-aware values preserve their instant. A naive datetime is interpreted in
    the Python host's local timezone.
    """
