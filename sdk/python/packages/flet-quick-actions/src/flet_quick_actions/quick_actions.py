from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet_quick_actions.types import ShortcutItem

import flet as ft

__all__ = ["QuickActions"]


@control("QuickActions")
class QuickActions(Service):
    """
    A service for managing the app's home-screen quick actions.

    Quick actions are the shortcuts that appear when the user long-presses
    the app icon (App Shortcuts on Android, Home Screen Quick Actions on
    iOS). Matches the official example at
    https://pub.dev/packages/quick_actions#example.

    Danger:
        Platform support

        **Android** and **iOS** only. On other platforms every method is a
        no-op and :attr:`on_action` never fires.

    Note:
        Set :attr:`on_action` **before** appending this service to
        ``page.services`` so the cold-start action (the one that launched
        the app) is not lost. If you cannot guarantee that ordering, call
        :meth:`get_pending_action` after setup — see its docstring.

    See also:

    * Flutter's `quick_actions
      <https://pub.dev/packages/quick_actions>`_ package.
    """

    on_action: Optional[ft.EventHandler[ft.ControlEvent]] = None
    """
    Fired when the user launches the app via a quick action.

    ``e.data`` is the ``type`` string of the tapped :class:`ShortcutItem`.
    """

    async def set_shortcuts(self, shortcuts: list[ShortcutItem]) -> None:
        """
        Replace the current quick-action list with ``shortcuts``.

        Call this once after the app starts, and again whenever the available
        actions change (e.g. after login). This method awaits the underlying
        platform call when it returns, the shortcuts are already visible
        to the OS.

        Mirrors ``QuickActions.setShortcutItems()`` in the official example.
        """
        await self._invoke_method(
            "set_shortcuts",
            {
                "shortcuts": [
                    {
                        "type": s.type,
                        "localized_title": s.localized_title,
                        "localized_subtitle": s.localized_subtitle,
                        "icon": s.icon,
                    }
                    for s in shortcuts
                ]
            },
        )

    async def clear_shortcuts(self) -> None:
        """Remove all quick actions from the home screen."""
        await self._invoke_method("clear_shortcuts")

    async def get_pending_action(self) -> Optional[str]:
        """
        Return (and clear) the action that launched the app, if any.

        Only needed for the **cold-start** case: the app was launched by
        tapping a quick action, and the Dart callback fired before Python
        attached :attr:`on_action`. The action is buffered on the Dart side
        and returned once by this method.

        Returns:
            The shortcut ``type`` that launched the app, or ``None`` if the
            app was launched normally.

        Typical usage call after setup from an async task:

        ```python
        async def setup():
            qa = QuickActions()
            qa.on_action = handler
            # Pick up cold-start action, if any.
            action = await qa.get_pending_action()
            if action:
                handler(ft.ControlEvent(control=qa, name="action", data=action))
        """
        return await self._invoke_method("get_pending_action")
