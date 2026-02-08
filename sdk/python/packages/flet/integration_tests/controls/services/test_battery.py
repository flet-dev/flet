import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method.
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_battery(flet_app: ftt.FletTestApp):
    battery = ft.Battery()

    level = await battery.get_battery_level()
    state = await battery.get_battery_state()
    save_mode = await battery.is_in_battery_save_mode()

    assert level is None or isinstance(level, int)
    if isinstance(level, int):
        assert 0 <= level <= 100
    assert isinstance(state, ft.BatteryState)
    assert isinstance(save_mode, bool)
