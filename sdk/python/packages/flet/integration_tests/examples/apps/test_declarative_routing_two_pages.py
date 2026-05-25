import pytest

import examples.apps.declarative.routing_two_pages.main as routing_two_pages
import flet as ft
import flet.testing as ftt


def routing_two_pages_main(page: ft.Page):
    page.render_views(routing_two_pages.RoutingExample)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": routing_two_pages_main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_declarative_routing_two_pages(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(500, 420)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Visit Store")).count == 1
    assert (await flet_app_function.tester.find_by_text("Do something")).count == 1

    flet_app_function.assert_screenshot(
        "declarative_routing_two_pages",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
