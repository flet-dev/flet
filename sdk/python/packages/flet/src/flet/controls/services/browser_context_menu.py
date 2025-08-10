from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["BrowserContextMenu"]


@control("BrowserContextMenu")
class BrowserContextMenu(Service):
    def __post_init__(self, ref):
        super().__post_init__(ref)
        self.__disabled = False

    async def enable(self, timeout: Optional[float] = None):
        await self._invoke_method("enable_menu", timeout=timeout)
        self.__disabled = False

    async def disable(self, timeout: Optional[float] = None):
        await self._invoke_method("disable_menu", timeout=timeout)
        self.__disabled = True

    @property
    def disabled(self):
        return self.__disabled
