import pytest

import flet.testing as ftt
from examples.controls.layout_control import flip, matrix4_transform


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": flip.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_flip(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(380, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "flip_initial",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    toggle_x = await flet_app_function.tester.find_by_text("Toggle X")
    await flet_app_function.tester.tap(toggle_x)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "flip_after_x",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    toggle_y = await flet_app_function.tester.find_by_text("Toggle Y")
    await flet_app_function.tester.tap(toggle_y)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "flip_after_y",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": matrix4_transform.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_matrix4_transform(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(780, 360)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "matrix4_transform",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
