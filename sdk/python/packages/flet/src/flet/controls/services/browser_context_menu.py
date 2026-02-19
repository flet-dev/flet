from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["BrowserContextMenu"]


@control("BrowserContextMenu")
class BrowserContextMenu(Service):
    """
    Controls the browser's context menu on the web platform.

    The context menu is the menu that appears on right clicking or selecting
    text in the browser, for example.

    On web, by default, the browser's context menu is enabled and
    Flet's context menus are hidden.

    On all non-web platforms, this does nothing.
    """

    def __post_init__(self, ref):
        super().__post_init__(ref)
        self.__disabled = False

    async def enable(self):
        """
        Enable the browser's context menu.

        By default, when the app starts, the browser's context menu is already enabled.
        """
        await self._invoke_method("enable_menu")
        self.__disabled = False

    async def disable(self):
        """
        Disable the browser's context menu.

        By default, when the app starts, the browser's context menu is
        already enabled.
        """
        await self._invoke_method("disable_menu")
        self.__disabled = True

    @property
    def disabled(self):
        """
        Whether browser context menu disabling is currently requested.

        This flag is managed by this service instance:
        - initialized to `False`;
        - set to `True` after [`disable()`][(c).disable];
        - set to `False` after [`enable()`][(c).enable].

        Note:
            On non-web platforms, browser context menu control is not applicable,
            but this property still reflects the last requested state.
        """
        return self.__disabled
