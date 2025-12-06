from typing import Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["Clipboard"]


@control("Clipboard")
class Clipboard(Service):
    """
    Provides access to the system clipboard.
    """

    async def set(self, value: str) -> None:
        """
        Stores the given clipboard data on the clipboard.
        """
        await self._invoke_method("set", {"data": value})

    async def get(self) -> Optional[str]:
        """
        Retrieves data from the clipboard.
        """
        return await self._invoke_method("get")
