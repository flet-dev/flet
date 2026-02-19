from typing import Optional

from flet.controls.base_control import control
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.service import Service
from flet.controls.types import PagePlatform

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

        Args:
            value: The image data (in bytes) to be stored on the clipboard.

        Raises:
            FletUnsupportedPlatformException: If called on platforms other than the
                following: Android, iOS, Web.
        """
        if not (self.page.web or self.page.platform.is_mobile()):
            raise FletUnsupportedPlatformException(
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

    async def set_files(self, files: list[str]) -> bool:
        """
        Stores file references on the clipboard.

        Args:
            files: A list of file paths.

        Returns:
            `True` if the operation succeeded, otherwise `False`.

        Raises:
            FletUnsupportedPlatformException: If called on platforms other than the
                following: macOS, Windows, Linux.
        """
        if self.page.web or not self.page.platform.is_desktop():
            raise FletUnsupportedPlatformException(
                "set_files is supported on desktop platforms only"
            )
        return await self._invoke_method("set_files", {"files": files})

    async def get_files(self) -> list[str]:
        """
        Retrieves file references from the clipboard.

        Returns:
            A list of file references available in the clipboard.
            On Android these are typically content URIs.

        Raises:
            FletUnsupportedPlatformException: If called on platforms other than the
                following: Android, macOS, Windows, Linux.
        """
        if self.page.web or (
            not self.page.platform.is_desktop()
            and self.page.platform != PagePlatform.ANDROID
        ):
            raise FletUnsupportedPlatformException(
                "get_files is supported on desktop and Android platforms only"
            )
        return await self._invoke_method("get_files")
