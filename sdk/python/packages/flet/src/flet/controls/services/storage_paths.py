from typing import List, Optional

from flet.controls.base_control import control
from flet.controls.services.service import Service

__all__ = ["StoragePaths"]


@control("StoragePaths")
class StoragePaths(Service):
    application_cache_directory: str = ""
    application_documents_directory: str = ""
    application_support_directory: str = ""
    downloads_directory: Optional[str] = None
    external_cache_directories: Optional[List[str]] = None
    external_storage_directories: Optional[List[str]] = None
    library_directory: str = ""
    external_cache_directory: Optional[str] = None
    temporary_directory: str = ""
    console_log_filename: str = ""
