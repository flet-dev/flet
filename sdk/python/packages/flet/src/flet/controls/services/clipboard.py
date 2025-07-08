import asyncio
from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.controls.types import Number

__all__ = ["Clipboard"]


@control("Clipboard")
class Clipboard(Service):
    def set(self, value: str, timeout: Optional[Number] = None) -> None:
        """
        Get the last text value saved to a clipboard on a client side.
        """
        asyncio.create_task(self.set_async(value, timeout=timeout))

    async def set_async(self, value: str, timeout: Optional[Number] = None) -> None:
        """
        Set clipboard data on a client side (user's web browser or a desktop).

        /// details | Example
            type: example

        ```python
        Example - TBD
        ```
        ///
        """
        await self._invoke_method_async("set", {"data": value}, timeout=timeout)

    async def get_async(self, timeout: Optional[Number] = None) -> Optional[str]:
        """
        Set clipboard data on a client side (user's web browser or a desktop).

        /// details | Example
            type: example

        ```python
        Example - TBD
        ```
        ///
        """
        return await self._invoke_method_async("get", timeout=timeout)
