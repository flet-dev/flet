import asyncio
from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.controls.types import OptionalNumber

__all__ = ["Clipboard"]


@control("Clipboard")
class Clipboard(Service):
    def set(self, value: str, timeout: OptionalNumber = None) -> None:
        asyncio.create_task(self.set_async(value, timeout=timeout))

    async def set_async(self, value: str, timeout: OptionalNumber = None) -> None:
        await self._invoke_method_async("set", {"data": value}, timeout=timeout)

    async def get_async(self, timeout: OptionalNumber = None) -> Optional[str]:
        return await self._invoke_method_async("get", timeout=timeout)
