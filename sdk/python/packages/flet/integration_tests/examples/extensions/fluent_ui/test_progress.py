import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.progress.main as progress
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_progress_bar_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=240,
            spacing=16,
            controls=[
                fluent.ProgressBar(value=30),
                fluent.ProgressBar(value=70, color=ft.Colors.GREEN),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_progress_ring_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Row(
            tight=True,
            spacing=16,
            controls=[
                fluent.ProgressRing(value=30),
                fluent.ProgressRing(value=70, color=ft.Colors.GREEN),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_indeterminate_renders(flet_app_function: ftt.FletTestApp):
    # Indeterminate indicators animate forever, so the clock is advanced by a
    # fixed amount instead of waiting for the animations to settle.
    flet_app_function.page.add(fluent.ProgressBar(width=200), fluent.ProgressRing())
    await flet_app_function.tester.pump(duration=ft.Duration(milliseconds=500))


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": progress.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_progress(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "progress_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Advance")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("50% done")).count == 1
    flet_app_function.assert_screenshot(
        "progress",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["progress_initial", "progress"], "progress_flow", duration=1000
    )
