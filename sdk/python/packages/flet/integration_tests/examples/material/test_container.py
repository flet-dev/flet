import pytest

import flet.testing as ftt
from examples.controls.container import (
    nested_themes_1,
    nested_themes_2,
    size_aware,
)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": size_aware.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_size_aware(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(260, 210)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "size_aware",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": nested_themes_1.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_nested_themes_1(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "nested_themes_1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": nested_themes_2.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_nested_themes_2(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(650, 350)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "nested_themes_2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
