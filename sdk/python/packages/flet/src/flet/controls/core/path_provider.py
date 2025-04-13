from typing import List, Optional

from flet.controls.control import Service, control

__all__ = ["PathProvider"]


@control("PathProvider")
class PathProvider(Service):
    application_cache_directory: str = None
    application_documents_directory: str = None
    application_support_directory: str = None
    downloads_directory: Optional[str] = None
    external_cache_directories: Optional[List[str]] = None
    external_storage_directories: Optional[List[str]] = None
    library_directory: str = None
    external_cache_directory: Optional[str] = None
    temporary_directory: str = None
