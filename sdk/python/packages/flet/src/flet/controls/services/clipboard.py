from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["Clipboard"]


@control("Clipboard")
class Clipboard(Service):
    async def set(self, value: str) -> None:
        """
        Set clipboard data on a client side (user's web browser or a desktop).

        /// details | Example
            type: example

        ```python
        Example - TBD
        ```
        ///
        """
        await self._invoke_method("set", {"data": value})

    async def get(self) -> Optional[str]:
        """
        Set clipboard data on a client side (user's web browser or a desktop).

        /// details | Example
            type: example

        ```python
        Example - TBD
        ```
        ///
        """
        return await self._invoke_method("get")
