import pytest

import examples.controls.core.container.nested_themes_1.main as nested_themes_1
import examples.controls.core.container.nested_themes_2.main as nested_themes_2
import examples.controls.core.container.size_aware.main as size_aware
import flet.testing as ftt


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
