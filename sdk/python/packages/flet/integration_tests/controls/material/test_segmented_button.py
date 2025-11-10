import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.SegmentedButton(
            selected=["1"],
            segments=[
                ft.Segment(
                    value="1",
                    label="1",
                    icon=ft.Icons.LOOKS_ONE,
                ),
                ft.Segment(
                    value="2",
                    label=ft.Text("2"),
                    icon=ft.Icon(ft.Icons.LOOKS_TWO),
                ),
                ft.Segment(
                    value="3",
                    label=ft.Text("3"),
                ),
                ft.Segment(
                    value="4",
                    icon=ft.Icons.LOOKS_4,
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp):
    flet_app.page.theme = ft.Theme(
        segmented_button_theme=ft.SegmentedButtonTheme(
            selected_icon=ft.Icons.HOME,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE, shape=ft.BeveledRectangleBorder()
            ),
        )
    )
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 600)

    scr_1 = ft.Screenshot(
        ft.SegmentedButton(
            selected=["1"],
            segments=[
                ft.Segment(
                    value="1",
                    label="1",
                    icon=ft.Icons.LOOKS_ONE,
                ),
                ft.Segment(
                    value="2",
                    label=ft.Text("2"),
                    icon=ft.Icon(ft.Icons.LOOKS_TWO),
                ),
                ft.Segment(
                    value="3",
                    label=ft.Text("3"),
                ),
                ft.Segment(
                    value="4",
                    icon=ft.Icons.LOOKS_4,
                ),
            ],
        ),
        key="sb",
    )
    flet_app.page.add(scr_1)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )
