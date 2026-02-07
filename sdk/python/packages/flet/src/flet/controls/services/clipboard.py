from typing import Optional

from flet.controls.base_control import control
from flet.controls.exceptions import FletUnimplementedPlatformException
from flet.controls.services.service import Service

__all__ = ["Clipboard"]


@control("Clipboard")
class Clipboard(Service):
    """
    Provides access to the system clipboard.
    """

    async def set(self, value: str) -> None:
        """
        Stores the given data on the clipboard.

        Args:
            value: The string data to be stored on the clipboard.
        """
        await self._invoke_method("set", {"data": value})

    async def get(self) -> Optional[str]:
        """
        Retrieves data from the clipboard.

        Returns:
            The string data retrieved from the clipboard, or `None`
                if the clipboard is empty or does not contain string data.
        """
        return await self._invoke_method("get")

    async def set_image(self, value: bytes) -> None:
        """
        Stores image bytes on the clipboard.

        Note:
            Supported on the following platforms only: Android, iOS, Web.

        Args:
            value: The image data (in bytes) to be stored on the clipboard.
        """
        if not (self.page.web or self.page.platform.is_mobile()):
            raise FletUnimplementedPlatformException(
                "set_image is not supported on this platform"
            )
        await self._invoke_method("set_image", {"data": value})

    async def get_image(self) -> Optional[bytes]:
        """
        Retrieves image data from the clipboard.

        Returns:
            The image data retrieved from the clipboard as bytes, or `None`
                if the clipboard is empty or does not contain image data.
        """
        return await self._invoke_method("get_image")
