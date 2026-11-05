import flet_shadcn_ui as shad
import pytest

import examples.extensions.shadcn_ui.select.main as select
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=shad.Select(
            value="banana",
            min_width=180,
            options=[
                shad.SelectOption(value="apple", text="Apple"),
                shad.SelectOption(value="banana", text="Banana"),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": select.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_select(flet_app_function: ftt.FletTestApp):
    # The option list opens in an overlay above the page, so these are
    # full-page screenshots rather than page-controls screenshots.
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(320, 340)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    async def capture(name: str):
        flet_app_function.assert_screenshot(
            name,
            await flet_app_function.page.take_screenshot(
                pixel_ratio=flet_app_function.screenshots_pixel_ratio
            ),
        )

    await capture("select_closed")

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Select a fruit")
    )
    await flet_app_function.tester.pump_and_settle()
    await capture("select_open")

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Banana")
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Selected: banana")).count == 1
    await capture("select")
    flet_app_function.create_gif(
        ["select_closed", "select_open", "select"], "select_flow", duration=1000
    )
