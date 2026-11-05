import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt

SWATCH_SIZE = 40

SURFACE_ROLES = [
    ft.Colors.SURFACE,
    ft.Colors.SURFACE_DIM,
    ft.Colors.SURFACE_BRIGHT,
    ft.Colors.SURFACE_CONTAINER_LOWEST,
    ft.Colors.SURFACE_CONTAINER_LOW,
    ft.Colors.SURFACE_CONTAINER,
    ft.Colors.SURFACE_CONTAINER_HIGH,
    ft.Colors.SURFACE_CONTAINER_HIGHEST,
    ft.Colors.ON_SURFACE,
    ft.Colors.ON_SURFACE_VARIANT,
    ft.Colors.OUTLINE,
    ft.Colors.OUTLINE_VARIANT,
    ft.Colors.INVERSE_SURFACE,
    ft.Colors.ON_INVERSE_SURFACE,
]


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


def _sample_ui() -> ft.Container:
    return ft.Container(
        width=SWATCH_SIZE * len(SURFACE_ROLES),
        bgcolor=ft.Colors.SURFACE,
        padding=16,
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Text("Surfaces", size=20, weight=ft.FontWeight.BOLD),
                ft.Card(
                    content=ft.Container(
                        padding=12,
                        content=ft.Column(
                            spacing=4,
                            controls=[
                                ft.Text("Card", weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    "On a surface container.",
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                ),
                            ],
                        ),
                    ),
                ),
                ft.TextField(label="Filled", filled=True, value="Text"),
                ft.TextField(label="Outlined", value="Text"),
                ft.Row(
                    controls=[
                        ft.Chip(label="Chip", on_click=lambda: None),
                        ft.FilledButton("Filled"),
                        ft.OutlinedButton("Outlined"),
                    ],
                ),
                ft.NavigationBar(
                    destinations=[
                        ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                        ft.NavigationBarDestination(
                            icon=ft.Icons.SEARCH, label="Search"
                        ),
                    ],
                ),
            ],
        ),
    )


@pytest.mark.parametrize(
    "surfaces, theme_mode",
    [
        (None, ft.ThemeMode.LIGHT),
        (None, ft.ThemeMode.DARK),
        (ft.ThemeSurfaces.TONAL, ft.ThemeMode.LIGHT),
        (ft.ThemeSurfaces.TONAL, ft.ThemeMode.DARK),
    ],
    ids=["neutral_light", "neutral_dark", "tonal_light", "tonal_dark"],
)
@pytest.mark.asyncio(loop_scope="function")
async def test_surfaces(
    flet_app: ftt.FletTestApp,
    surfaces: ft.ThemeSurfaces,
    theme_mode: ft.ThemeMode,
    request,
):
    flet_app.page.theme = ft.Theme(surfaces=surfaces)
    flet_app.page.dark_theme = ft.Theme(surfaces=surfaces)
    flet_app.page.theme_mode = theme_mode
    flet_app.resize_page(700, 700)

    swatches = ft.Row(
        spacing=0,
        controls=[
            ft.Container(width=SWATCH_SIZE, height=SWATCH_SIZE, bgcolor=role)
            for role in SURFACE_ROLES
        ],
    )
    sample = ft.Screenshot(ft.Column(spacing=0, controls=[swatches, _sample_ui()]))
    flet_app.page.add(sample)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        request.node.callspec.id,
        await sample.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )
