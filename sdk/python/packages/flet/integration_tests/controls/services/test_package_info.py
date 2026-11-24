import datetime

import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method.
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_package_info(flet_app: ftt.FletTestApp):
    info = await flet_app.page.get_package_info()

    assert isinstance(info, ft.PackageInfo)
    for value in (
        info.app_name,
        info.package_name,
        info.version,
        info.build_number,
        info.build_signature,
    ):
        assert isinstance(value, str)
    assert info.installer_store is None or isinstance(info.installer_store, str)
    for time in (info.install_time, info.update_time):
        assert time is None or isinstance(time, datetime.datetime)

    if not flet_app.page.web:
        # Describes the Flet client app running the test.
        assert info.version
        assert info.package_name
