import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt
import flet_local_auth as auth
from flet.controls.exceptions import FletUnsupportedPlatformException


@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_unsupported_platform_raises(flet_app: ftt.FletTestApp):
    if not (flet_app.page.web or flet_app.page.platform == ft.PagePlatform.LINUX):
        pytest.skip("Linux or web only")

    with pytest.raises(FletUnsupportedPlatformException):
        auth.LocalAuthentication()


@pytest.mark.asyncio(loop_scope="function")
async def test_device_capabilities(flet_app: ftt.FletTestApp):
    if flet_app.page.web or flet_app.page.platform == ft.PagePlatform.LINUX:
        pytest.skip("Native mobile/desktop only")

    local_auth = auth.LocalAuthentication()

    supported = await local_auth.is_device_supported()
    assert isinstance(supported, bool)

    can_check = await local_auth.can_check_biometrics()
    assert isinstance(can_check, bool)

    biometrics = await local_auth.get_available_biometrics()
    assert isinstance(biometrics, list)
    assert all(isinstance(item, auth.BiometricType) for item in biometrics)
