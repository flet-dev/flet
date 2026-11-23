import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.text_box.main as text_box
import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=260,
            controls=[
                fluent.TextBox(placeholder="Placeholder"),
                fluent.TextBox(value="With value"),
                fluent.TextBox(placeholder="Search", suffix=fluent.FluentIcons.SEARCH),
                fluent.TextBox(placeholder="Disabled", disabled=True),
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": text_box.main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_text_box(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.update()
    scr = await flet_app_function.wrap_page_controls_in_screenshot(
        bgcolor=ft.Colors.SURFACE
    )
    flet_app_function.assert_screenshot(
        "text_box_initial",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )

    await flet_app_function.tester.enter_text(
        await flet_app_function.tester.find_by_key("name"), "Ada"
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Hello, Ada!")).count == 1
    flet_app_function.assert_screenshot(
        "text_box",
        await scr.capture(pixel_ratio=flet_app_function.screenshots_pixel_ratio),
    )
    flet_app_function.create_gif(
        ["text_box_initial", "text_box"], "text_box_flow", duration=1000
    )
