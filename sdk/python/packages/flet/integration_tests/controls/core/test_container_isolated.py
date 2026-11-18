import io

import pytest
from PIL import Image, ImageStat

import flet as ft
import flet.testing as ftt

# Colors are checked by sampling pixels rather than against goldens: golden
# comparison is structural (SSIM) and barely reacts to a uniform color change.


async def mean_rgb(screenshot: ft.Screenshot) -> tuple[float, float, float]:
    image = Image.open(io.BytesIO(await screenshot.capture(pixel_ratio=1)))
    r, g, b = ImageStat.Stat(image.convert("RGB")).mean
    return r, g, b


async def update_and_settle(flet_app: ftt.FletTestApp, control: ft.Control):
    control.update()
    await flet_app.tester.pump_and_settle()


@pytest.mark.asyncio(loop_scope="function")
async def test_theme_mode_change(flet_app_function: ftt.FletTestApp):
    """Setting, changing and clearing `Container.theme_mode` at runtime."""
    flet_app = flet_app_function

    async def brightness() -> float:
        return sum(await mean_rgb(screenshot)) / 3

    container = ft.Container(
        content=ft.Container(bgcolor=ft.Colors.SURFACE, width=120, height=60),
    )
    screenshot = ft.Screenshot(container)
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app.page.add(screenshot)
    await flet_app.tester.pump_and_settle()
    assert await brightness() > 200

    container.theme_mode = ft.ThemeMode.DARK
    await update_and_settle(flet_app, container)
    assert await brightness() < 60

    container.theme_mode = ft.ThemeMode.LIGHT
    await update_and_settle(flet_app, container)
    assert await brightness() > 200

    container.theme_mode = ft.ThemeMode.DARK
    await update_and_settle(flet_app, container)
    assert await brightness() < 60

    container.theme_mode = None
    await update_and_settle(flet_app, container)
    assert await brightness() > 200


@pytest.mark.asyncio(loop_scope="function")
async def test_theme_change(flet_app_function: ftt.FletTestApp):
    """Setting, changing and clearing `Container.theme`/`dark_theme` at runtime."""
    flet_app = flet_app_function

    container = ft.Container(
        theme_mode=ft.ThemeMode.LIGHT,
        content=ft.Container(bgcolor=ft.Colors.PRIMARY, width=120, height=60),
    )
    screenshot = ft.Screenshot(container)
    flet_app.page.add(screenshot)
    await flet_app.tester.pump_and_settle()
    r, g, b = await mean_rgb(screenshot)
    assert b > r, "default seed (blue)"

    container.theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
    await update_and_settle(flet_app, container)
    r, g, b = await mean_rgb(screenshot)
    assert r > g and r > b, "theme set"

    container.theme.color_scheme_seed = ft.Colors.GREEN
    await update_and_settle(flet_app, container)
    r, g, b = await mean_rgb(screenshot)
    assert g > r and g > b, "theme changed"

    container.theme_mode = ft.ThemeMode.DARK
    container.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
    await update_and_settle(flet_app, container)
    r, g, b = await mean_rgb(screenshot)
    assert r > g and r > b, "dark_theme set"

    container.theme_mode = ft.ThemeMode.LIGHT
    container.theme = None
    container.dark_theme = None
    await update_and_settle(flet_app, container)
    r, g, b = await mean_rgb(screenshot)
    assert b > r, "themes cleared"


@pytest.mark.asyncio(loop_scope="function")
async def test_theme_change_keeps_content_state(flet_app_function: ftt.FletTestApp):
    """Adding or removing a `Container`'s theme keeps the state of its content."""
    flet_app = flet_app_function

    async def assert_scrolled():
        await flet_app.tester.pump_and_settle()
        assert (await flet_app.tester.find_by_text("Item 0")).count == 0
        assert (await flet_app.tester.find_by_text("Item 50")).count == 1

    list_view = ft.ListView(
        controls=[ft.Text(f"Item {i}") for i in range(100)],
        item_extent=40,
        height=200,
    )
    container = ft.Container(content=list_view)
    flet_app.page.add(container)
    await flet_app.tester.pump_and_settle()
    await list_view.scroll_to(offset=2000)
    await assert_scrolled()

    container.theme_mode = ft.ThemeMode.DARK
    container.update()
    await assert_scrolled()

    container.theme_mode = None
    container.update()
    await assert_scrolled()

    container.theme = ft.Theme(color_scheme_seed=ft.Colors.RED)
    container.update()
    await assert_scrolled()
