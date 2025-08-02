import asyncio
from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["BrowserContextMenu"]


@control("BrowserContextMenu")
class BrowserContextMenu(Service):
    def __post_init__(self, ref):
        super().__post_init__(ref)
        self.__disabled = False

    async def enable_async(self, timeout: Optional[float] = None):
        await self._invoke_method_async("enable_menu", timeout=timeout)
        self.__disabled = False

    def enable(self, timeout: Optional[float] = None):
        asyncio.create_task(self.enable_async(timeout))

    async def disable_async(self, timeout: Optional[float] = None):
        await self._invoke_method_async("disable_menu", timeout=timeout)
        self.__disabled = True

    def disable(self, timeout: Optional[float] = None):
        asyncio.create_task(self.disable_async(timeout))

    @property
    def disabled(self):
        return self.__disabled
