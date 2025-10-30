import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_button_theme(flet_app: ftt.FletTestApp):
    flet_app.page.theme = ft.Theme(
        button_theme=ft.ButtonTheme(
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN,
                shape=ft.BeveledRectangleBorder(
                    radius=5,
                ),
                side=ft.BorderSide(width=5, color=ft.Colors.GREEN_900),
                padding=ft.Padding.all(10),
                # text_style=ft.TextStyle(
                #     size=15,
                #     italic=True,
                #     color=ft.Colors.ORANGE,  # color is not shown on the button text,
                #     #   use style.color instead
                # ),
            ),
        )
    )

    await flet_app.resize_page(400, 600)

    scr_1 = ft.Screenshot(
        ft.Button(content="Button"),
    )
    flet_app.page.add(scr_1)
    # flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )
