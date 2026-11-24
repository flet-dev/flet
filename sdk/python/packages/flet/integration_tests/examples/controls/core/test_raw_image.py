import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.core.raw_image.plasma.main import plasma_frame


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    raw_image = ft.RawImage(width=320, height=200)
    screenshot = ft.Screenshot(raw_image)
    flet_app_function.page.add(screenshot)
    await flet_app_function.tester.pump_and_settle()
    # A plasma frame at a fixed timestamp is fully deterministic.
    await raw_image.render(plasma_frame(320, 200, 2.5), premultiplied=True)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        request.node.name,
        await screenshot.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
