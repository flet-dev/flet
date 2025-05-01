from typing import List, Optional

from flet.controls.base_control import control
from flet.controls.exceptions import FletUnsupportedPlatformException
from flet.controls.services.service import Service
from flet.controls.types import PagePlatform

__all__ = ["StoragePaths"]


@control("StoragePaths")
class StoragePaths(Service):
    async def get_application_cache_directory_async(self) -> str:
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_application_cache_directory is not supported on web"
            )
        return await self._invoke_method_async("get_application_cache_directory")

    async def get_application_documents_directory_async(self) -> str:
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_application_documents_directory is not supported on web"
            )
        return await self._invoke_method_async("get_application_documents_directory")

    async def get_application_support_directory_async(self) -> str:
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_application_support_directory is not supported on web"
            )
        return await self._invoke_method_async("get_application_support_directory")

    async def get_downloads_directory_async(self) -> Optional[str]:
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_downloads_directory is not supported on web"
            )
        return await self._invoke_method_async("get_downloads_directory")

    async def get_external_cache_directories_async(self) -> Optional[List[str]]:
        if self.page.web or self.page.platform != PagePlatform.ANDROID:
            raise FletUnsupportedPlatformException(
                "get_external_cache_directories is supported only on Android"
            )
        return await self._invoke_method_async("get_external_cache_directories")

    async def get_external_storage_directories_async(self) -> Optional[List[str]]:
        if self.page.web or self.page.platform != PagePlatform.ANDROID:
            raise FletUnsupportedPlatformException(
                "get_external_storage_directories is supported only on Android"
            )
        return await self._invoke_method_async("get_external_storage_directories")

    async def get_library_directory_async(self) -> str:
        if self.page.web or not self.page.platform.is_apple():
            raise FletUnsupportedPlatformException(
                "get_library_directory is supported only on iOS and macOS"
            )
        return await self._invoke_method_async("get_library_directory")

    async def get_external_cache_directory_async(self) -> Optional[str]:
        if self.page.web or self.page.platform != PagePlatform.ANDROID:
            raise FletUnsupportedPlatformException(
                "get_external_cache_directory is supported only on Android"
            )
        return await self._invoke_method_async("get_external_cache_directory")

    async def get_temporary_directory_async(self) -> str:
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_temporary_directory is not supported on web"
            )
        return await self._invoke_method_async("get_temporary_directory")

    async def get_console_log_filename_async(self) -> str:
        if self.page.web:
            raise FletUnsupportedPlatformException(
                "get_console_log_filename is not supported on web"
            )
        return await self._invoke_method_async("get_console_log_filename")
