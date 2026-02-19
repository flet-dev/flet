import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt
from flet.controls.exceptions import FletUnsupportedPlatformException


# Create a new flet_app instance for each test method.
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_storage_paths(flet_app: ftt.FletTestApp):
    paths = ft.StoragePaths()

    if flet_app.page.web:
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_application_cache_directory()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_application_documents_directory()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_application_support_directory()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_downloads_directory()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_temporary_directory()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_console_log_filename()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_library_directory()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_external_cache_directories()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_external_storage_directories()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_external_storage_directory()
        return

    cache_dir = await paths.get_application_cache_directory()
    documents_dir = await paths.get_application_documents_directory()
    support_dir = await paths.get_application_support_directory()
    temporary_dir = await paths.get_temporary_directory()
    console_log_filename = await paths.get_console_log_filename()
    downloads_dir = await paths.get_downloads_directory()

    assert isinstance(cache_dir, str) and cache_dir
    assert isinstance(documents_dir, str) and documents_dir
    assert isinstance(support_dir, str) and support_dir
    assert isinstance(temporary_dir, str) and temporary_dir
    assert isinstance(console_log_filename, str) and console_log_filename
    assert console_log_filename.endswith("console.log")
    assert downloads_dir is None or isinstance(downloads_dir, str)

    # library directory
    if flet_app.page.platform.is_apple():
        library_dir = await paths.get_library_directory()
        assert isinstance(library_dir, str) and library_dir
    else:
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_library_directory()

    # external storage directories
    if flet_app.page.platform == ft.PagePlatform.ANDROID:
        external_cache_dirs = await paths.get_external_cache_directories()
        external_storage_dirs = await paths.get_external_storage_directories()
        external_storage_dir = await paths.get_external_storage_directory()

        assert external_cache_dirs is None or all(
            isinstance(path, str) and path for path in external_cache_dirs
        )
        assert external_storage_dirs is None or all(
            isinstance(path, str) and path for path in external_storage_dirs
        )
        assert external_storage_dir is None or isinstance(external_storage_dir, str)
    else:
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_external_cache_directories()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_external_storage_directories()
        with pytest.raises(FletUnsupportedPlatformException):
            await paths.get_external_storage_directory()
