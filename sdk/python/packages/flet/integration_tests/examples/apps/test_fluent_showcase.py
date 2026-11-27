import pytest

import examples.apps.fluent_showcase.main as fluent_showcase
import flet.testing as ftt


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": fluent_showcase.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_fluent_showcase(flet_app_function: ftt.FletTestApp):
    page = flet_app_function.page
    page.enable_screenshots = True
    flet_app_function.resize_page(1360, 900)
    page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "fluent_showcase",
        await page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
