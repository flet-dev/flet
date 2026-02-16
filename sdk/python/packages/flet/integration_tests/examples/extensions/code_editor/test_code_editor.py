import pytest

import flet.testing as ftt
from examples.controls.code_editor import example_1, example_2, example_3


@pytest.mark.parametrize(
    "flet_app_function, screenshot_name, page_size",
    [
        ({"flet_app_main": example_1.main}, "image_for_docs", (700, 500)),
        ({"flet_app_main": example_1.main}, "example_1", (700, 500)),
        ({"flet_app_main": example_2.main}, "example_2", (700, 500)),
        ({"flet_app_main": example_3.main}, "example_3", (700, 500)),
    ],
    indirect=["flet_app_function"],
)
@pytest.mark.asyncio(loop_scope="function")
async def test_images_for_docs(
    flet_app_function: ftt.FletTestApp,
    screenshot_name: str,
    page_size: tuple[int, int],
):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(*page_size)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.assert_screenshot(
        screenshot_name,
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
