import pytest

import flet as ft
import flet.testing as ftt

from examples.controls.row import alignment, vertical_alignment, spacing, wrap


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Row(
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Card(
                    shape=ft.ContinuousRectangleBorder(radius=10),
                    content=ft.Container(
                        padding=5,
                        border_radius=ft.BorderRadius.all(5),
                        bgcolor=ft.Colors.AMBER_100,
                        content=ft.Text(f"Control {i}"),
                    ),
                )
                for i in range(1, 6)
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": alignment.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_alignment(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "alignment",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": vertical_alignment.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_vertical_alignment(flet_app_function: ftt.FletTestApp):
    flet_app_function.assert_screenshot(
        "vertical_alignment",
        await flet_app_function.take_page_controls_screenshot(),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": spacing.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_spacing(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(800, 200)
    flet_app_function.page.update()
    await flet_app_function.tester.tap_at(200, 60)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "spacing1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap_at(300, 60)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "spacing2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap_at(400, 60)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "spacing3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.create_gif(
        ["spacing1", "spacing2", "spacing3"],
        "row_spacing_adjustment",
        duration=1600,
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": wrap.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_wrap(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(800, 400)
    flet_app_function.page.update()
    await flet_app_function.tester.tap_at(600, 60)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "wrap1",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap_at(500, 60)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "wrap2",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    await flet_app_function.tester.tap_at(400, 60)
    await flet_app_function.tester.pump_and_settle()
    flet_app_function.assert_screenshot(
        "wrap3",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
    flet_app_function.create_gif(
        ["wrap1", "wrap2", "wrap3"],
        "wrap_adjustment",
        duration=1600,
    )
