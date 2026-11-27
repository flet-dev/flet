import flet_fluent_ui as fluent
import pytest

import examples.extensions.fluent_ui.breadcrumb_bar.main as breadcrumb_bar
import flet as ft
import flet.testing as ftt


async def _capture(app: ftt.FletTestApp, name: str):
    app.assert_screenshot(
        name,
        await app.page.take_screenshot(pixel_ratio=app.screenshots_pixel_ratio),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Column(
            width=320,
            controls=[
                fluent.BreadcrumbBar(
                    items=[
                        fluent.BreadcrumbItem("Home"),
                        fluent.BreadcrumbItem("Documents"),
                        fluent.BreadcrumbItem("Design"),
                    ]
                )
            ],
        ),
    )


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": breadcrumb_bar.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_breadcrumb_bar(flet_app_function: ftt.FletTestApp):
    tester = flet_app_function.tester
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(400, 160)
    flet_app_function.page.update()
    await tester.pump_and_settle()
    await _capture(flet_app_function, "breadcrumb_bar_initial")

    await tester.tap(await tester.find_by_text("Home"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Invoices")).count == 0
    await _capture(flet_app_function, "breadcrumb_bar_home")

    await tester.tap(await tester.find_by_text("Pictures"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Holidays")).count == 1
    await _capture(flet_app_function, "breadcrumb_bar")
    flet_app_function.create_gif(
        ["breadcrumb_bar_initial", "breadcrumb_bar_home", "breadcrumb_bar"],
        "breadcrumb_bar_flow",
        duration=1000,
    )
