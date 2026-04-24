import pytest

import flet.testing as ftt
from examples.controls.material.auto_complete.basic import main as basic


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": basic.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic_example_opens_suggestions(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(450, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "before_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    text_field = await flet_app_function.tester.find_by_text("One")
    await flet_app_function.tester.tap(text_field)
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        "after_click",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )

    flet_app_function.create_gif(
        ["before_click", "after_click"],
        "auto_complete_basic_flow",
        duration=1000,
    )
