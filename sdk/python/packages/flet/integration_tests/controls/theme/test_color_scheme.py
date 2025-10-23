import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_color_scheme(flet_app: ftt.FletTestApp):
    flet_app.page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.Colors.GREEN,
            on_primary=ft.Colors.YELLOW,
            primary_container=ft.Colors.GREEN_900,
            on_primary_container=ft.Colors.YELLOW,
            secondary=ft.Colors.BLUE,
            on_secondary=ft.Colors.WHITE,
            secondary_container=ft.Colors.BLUE_900,
            on_secondary_container=ft.Colors.WHITE,
            tertiary=ft.Colors.RED,
            on_tertiary=ft.Colors.WHITE,
            tertiary_container=ft.Colors.RED_900,
            on_tertiary_container=ft.Colors.WHITE,
            error=ft.Colors.RED,
            on_error=ft.Colors.WHITE,
            error_container=ft.Colors.RED_900,
            on_error_container=ft.Colors.WHITE,
            surface=ft.Colors.ORANGE_400,
            on_surface=ft.Colors.BLACK,
            on_surface_variant=ft.Colors.RED,
            outline=ft.Colors.BLUE_200,
            outline_variant=ft.Colors.BLUE_400,
            shadow=ft.Colors.BLACK,
            scrim=ft.Colors.BLACK,
            inverse_surface=ft.Colors.BLACK,
            on_inverse_surface=ft.Colors.WHITE,
            inverse_primary=ft.Colors.GREEN_900,
            surface_tint=ft.Colors.GREEN,
            on_primary_fixed=ft.Colors.WHITE,
            on_secondary_fixed=ft.Colors.WHITE,
            on_tertiary_fixed=ft.Colors.WHITE,
            on_primary_fixed_variant=ft.Colors.WHITE,
            on_secondary_fixed_variant=ft.Colors.WHITE,
            on_tertiary_fixed_variant=ft.Colors.WHITE,
        )
    )

    flet_app.page.enable_screenshots = True
    flet_app.page.window.width = 400
    flet_app.page.window.height = 600
    flet_app.page.add(
        ft.FilledButton("Primary button"),
        ft.FilledTonalButton("Secondary button"),
        ft.Container(
            ft.Text("Container surface", color=ft.Colors.ON_SURFACE_VARIANT, size=20),
            width=200,
            height=100,
            bgcolor=ft.Colors.SURFACE,
        ),
    )
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "cupertino_action_sheet_basic",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
