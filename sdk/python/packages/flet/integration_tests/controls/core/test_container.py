import io

import pytest
from PIL import Image, ImageStat

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_container_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            ft.Text("Container"),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_theme_mode_change(flet_app: ftt.FletTestApp):
    """Changing `Container.theme_mode` at runtime restyles its content."""

    async def surface_brightness() -> float:
        image = Image.open(io.BytesIO(await screenshot.capture(pixel_ratio=1)))
        return ImageStat.Stat(image.convert("L")).mean[0]

    container = ft.Container(
        theme_mode=ft.ThemeMode.LIGHT,
        content=ft.Container(bgcolor=ft.Colors.SURFACE, width=120, height=60),
    )
    screenshot = ft.Screenshot(container)
    flet_app.page.clean()
    flet_app.page.add(screenshot)
    await flet_app.tester.pump_and_settle()
    assert await surface_brightness() > 200

    container.theme_mode = ft.ThemeMode.DARK
    container.update()
    await flet_app.tester.pump_and_settle()
    assert await surface_brightness() < 60

    container.theme_mode = ft.ThemeMode.LIGHT
    container.update()
    await flet_app.tester.pump_and_settle()
    assert await surface_brightness() > 200
