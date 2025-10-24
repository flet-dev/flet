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
            error=ft.Colors.RED,
            error_container=ft.Colors.RED_900,
            inverse_primary=ft.Colors.GREEN_900,
            inverse_surface=ft.Colors.BLACK,
            on_error=ft.Colors.WHITE,
            on_error_container=ft.Colors.WHITE,
            on_inverse_surface=ft.Colors.WHITE,
            on_primary=ft.Colors.YELLOW,
            on_primary_container=ft.Colors.YELLOW,
            on_primary_fixed=ft.Colors.WHITE,
            on_primary_fixed_variant=ft.Colors.WHITE,
            on_secondary=ft.Colors.WHITE,
            on_secondary_container=ft.Colors.WHITE,
            on_secondary_fixed=ft.Colors.WHITE,
            on_secondary_fixed_variant=ft.Colors.WHITE,
            on_surface=ft.Colors.BLACK,
            on_surface_variant=ft.Colors.RED,
            on_tertiary=ft.Colors.WHITE,
            on_tertiary_container=ft.Colors.WHITE,
            on_tertiary_fixed=ft.Colors.WHITE,
            on_tertiary_fixed_variant=ft.Colors.WHITE,
            outline=ft.Colors.BLUE_200,
            outline_variant=ft.Colors.BLUE_400,
            primary=ft.Colors.GREEN,
            primary_container=ft.Colors.GREEN_900,
            primary_fixed=ft.Colors.GREEN_400,
            primary_fixed_dim=ft.Colors.GREEN_700,
            scrim=ft.Colors.BLACK,
            secondary=ft.Colors.BLUE,
            secondary_container=ft.Colors.BLUE_900,
            secondary_fixed=ft.Colors.BLUE_400,
            secondary_fixed_dim=ft.Colors.BLUE_700,
            shadow=ft.Colors.BLACK,
            surface=ft.Colors.ORANGE_400,
            surface_bright=ft.Colors.ORANGE_200,
            surface_container=ft.Colors.ORANGE,
            surface_container_high=ft.Colors.ORANGE_300,
            surface_container_highest=ft.Colors.ORANGE_500,
            surface_container_low=ft.Colors.ORANGE_100,
            surface_container_lowest=ft.Colors.ORANGE_50,
            surface_dim=ft.Colors.ORANGE_600,
            surface_tint=ft.Colors.GREEN,
            tertiary=ft.Colors.RED,
            tertiary_container=ft.Colors.RED_900,
            tertiary_fixed=ft.Colors.RED_400,
            tertiary_fixed_dim=ft.Colors.RED_700,
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
        "color_scheme",
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
