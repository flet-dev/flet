import pytest

import flet.testing as ftt
from examples.controls.datatable2.column_widths import main as column_widths
from examples.controls.datatable2.empty_state import main as empty_state


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": empty_state.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_empty_state(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(500, 200)
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "empty_state",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": column_widths.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_column_widths(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(640, 260)
    flet_app_function.page.update()

    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "column_widths",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
