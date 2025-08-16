from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service
from flet.controls.types import Number

__all__ = ["Clipboard"]


@control("Clipboard")
class Clipboard(Service):
    async def set(self, value: str, timeout: Optional[Number] = None) -> None:
        """
        Set clipboard data on a client side (user's web browser or a desktop).

        /// details | Example
            type: example

        ```python
        Example - TBD
        ```
        ///
        """
        await self._invoke_method("set", {"data": value}, timeout=timeout)

    async def get(self, timeout: Optional[Number] = None) -> Optional[str]:
        """
        Set clipboard data on a client side (user's web browser or a desktop).

        /// details | Example
            type: example

        ```python
        Example - TBD
        ```
        ///
        """
        return await self._invoke_method("get", timeout=timeout)
