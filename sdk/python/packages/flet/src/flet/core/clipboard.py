import asyncio
from typing import Optional

from flet.core.control import Service, control

__all__ = ["Clipboard"]


@control("Clipboard")
class Clipboard(Service):
    def set(self, value: str, timeout: Optional[float] = None) -> None:
        asyncio.create_task(self.set_async(value, timeout=timeout))

    async def set_async(self, value: str, timeout: Optional[float] = None) -> None:
        await self._invoke_method_async("set", {"data": value}, timeout=timeout)

    async def get_async(self, timeout: Optional[float] = None) -> Optional[str]:
        return await self._invoke_method_async("get", timeout=timeout)
