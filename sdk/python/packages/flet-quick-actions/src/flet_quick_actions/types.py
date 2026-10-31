from dataclasses import dataclass
from typing import Optional

__all__ = ["ShortcutItem"]


@dataclass
class ShortcutItem:
    """
    A single home-screen quick action.

    Corresponds to Flutter's ``ShortcutItem`` class. Matches the official
    example at
    https://pub.dev/packages/quick_actions#example.
    """

    type: str
    """
    App-specific identifier for the action.

    Delivered back to :attr:`QuickActions.on_action` when the user taps the
    shortcut. Must be unique within the app.
    """

    localized_title: str
    """
    User-visible title shown in the quick-actions menu.

    Shown on both Android (as the shortcut's short label) and iOS.
    """

    localized_subtitle: Optional[str] = None
    """
    Optional user-visible subtitle.

    **iOS only.** Android ignores this field. The official example uses it,
    e.g. ``'Action one subtitle'``.
    """

    icon: Optional[str] = None
    """
    Optional icon name.

    Platform caveats (from the official example):

    * **iOS** - must be the name of an **image asset** in the app bundle
      (e.g. ``"AppIcon"``). A system symbol name also works in recent
      versions of the plugin.
    * **Android** - must be the name of a **drawable resource** (e.g.
      ``"ic_launcher"``). The launcher picks the icon; the string is not
      the file path but the resource name.

    Tip:
        In a real project, give the image the **same name on both
        platforms** so the same ``icon`` string works everywhere.
    """
