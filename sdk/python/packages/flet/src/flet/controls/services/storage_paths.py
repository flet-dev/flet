from typing import Optional

from flet.controls.base_control import control
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.service import Service
from flet.controls.types import PagePlatform

__all__ = ["StoragePaths"]


@control("StoragePaths")
class StoragePaths(Service):
    """
    Provides access to commonly used storage paths on the device.

    Note:
        Its methods are not supported in web mode.
    """

    async def get_application_cache_directory(self) -> str:
        """Returns the path to the application-specific cache directory.

        If this directory does not exist, it is created automatically.

        Returns:
            The path to a directory where the application may place cache files.

        Raises:
            FletUnsupportedPlatformException: If called on the web platform.
        """
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_application_cache_directory is not supported in web mode"
            )
        return await self._invoke_method("get_application_cache_directory")

    async def get_application_documents_directory(self) -> str:
        """Returns the path to a directory for user-generated data.

        This directory is intended for data that cannot be recreated by your application.

        For non-user-generated data, consider using:

        - [`get_application_support_directory()`][(c).get_application_support_directory]
        - [`get_application_cache_directory()`][(c).get_application_cache_directory]
        - [`get_external_storage_directory()`][(c).get_external_storage_directory]

        Raises:
            FletUnsupportedPlatformException: If called on the web platform.

        Returns:
            The path to the application documents directory.
        """  # noqa: E501
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_application_documents_directory is not supported in web mode"
            )
        return await self._invoke_method("get_application_documents_directory")

    async def get_application_support_directory(self) -> str:
        """Returns the path to a directory for application support files.

        This directory is created automatically if it does not exist.
        Use this for files not exposed to the user. Do not use for user data files.

        Raises:
            FletUnsupportedPlatformException: If called on the web platform.

        Returns:
            The path to the application support directory.
        """
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_application_support_directory is not supported in web mode"
            )
        return await self._invoke_method("get_application_support_directory")

    async def get_downloads_directory(self) -> Optional[str]:
        """Returns the path to the downloads directory.

        The returned directory may not exist; clients should verify and create it
        if necessary.

        Raises:
            FletUnsupportedPlatformException: If called on the web platform.

        Returns:
            The path to the downloads directory, or None if unavailable.
        """
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_downloads_directory is not supported in web mode"
            )
        return await self._invoke_method("get_downloads_directory")

    async def get_external_cache_directories(self) -> Optional[list[str]]:
        """Returns paths to external cache directories.

        These directories are typically on external storage (e.g., SD cards).
        Multiple directories may be available on some devices.

        Raises:
            FletUnsupportedPlatformException: If called on the web or
                non-Android platforms.

        Returns:
            A List of external cache directory paths, or `None` if unavailable.
        """
        if self.page.web or self.page.platform != PagePlatform.ANDROID:
            raise FletUnsupportedPlatformException(
                "get_external_cache_directories is supported only on Android"
            )
        return await self._invoke_method("get_external_cache_directories")

    async def get_external_storage_directories(self) -> Optional[list[str]]:
        """Returns paths to external storage directories.

        These directories are typically on external storage (e.g., SD cards).
        Multiple directories may be available on some devices.

        Raises:
            FletUnsupportedPlatformException: If called on the web or
                non-Android platforms.

        Returns:
            A List of external storage directory paths, or `None` if unavailable.
        """
        if self.page.web or self.page.platform != PagePlatform.ANDROID:
            raise FletUnsupportedPlatformException(
                "get_external_storage_directories is supported only on Android"
            )
        return await self._invoke_method("get_external_storage_directories")

    async def get_library_directory(self) -> str:
        """Returns the path to the library directory.

        This directory is for persistent, backed-up files not visible to the user
        (e.g., sqlite.db).

        Raises:
            FletUnsupportedPlatformException: If called on the web or
                non-Apple platforms.

        Returns:
            The path to the library directory.
        """
        if self.page.web or not self.page.platform.is_apple():
            raise FletUnsupportedPlatformException(
                "get_library_directory is supported only on iOS and macOS"
            )
        return await self._invoke_method("get_library_directory")

    async def get_external_storage_directory(self) -> Optional[str]:
        """Returns the path to the top-level external storage directory.

        Raises:
            FletUnsupportedPlatformException: If called on the web or
                non-Android platforms.

        Returns:
            The path to the external storage directory, or `None` if unavailable.
        """
        if self.page.web or self.page.platform != PagePlatform.ANDROID:
            raise FletUnsupportedPlatformException(
                "get_external_storage_directory is supported only on Android"
            )
        return await self._invoke_method("get_external_storage_directory")

    async def get_temporary_directory(self) -> str:
        """Returns the path to the temporary directory.

        This directory is not backed up and is suitable for storing caches
        of downloaded files.
        Files may be cleared at any time.
        The caller is responsible for managing files within this directory.

        Raises:
            FletUnsupportedPlatformException: If called on the web platform.

        Returns:
            The path to the temporary directory.
        """
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_temporary_directory is not supported in web mode"
            )
        return await self._invoke_method("get_temporary_directory")

    async def get_console_log_filename(self) -> str:
        """Returns the path to a `console.log` file for debugging.

        This file is located in the
        [application cache directory][flet.StoragePaths.get_application_cache_directory].

        Raises:
            FletUnsupportedPlatformException: If called on the web platform.

        Returns:
            The path to the console log file.
        """  # noqa: E501
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_console_log_filename is not supported in web mode"
            )
        return await self._invoke_method("get_console_log_filename")
