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

    await flet_app.resize_page(500, 500)
    flet_app.page.scroll = ft.ScrollMode.HIDDEN

    def swatch(label: str, fill_color: str, text_color: str) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        label,
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color=text_color,
                        text_align=ft.TextAlign.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            ),
            width=100,
            height=72,
            bgcolor=fill_color,
            border_radius=ft.BorderRadius.all(12),
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            padding=10,
        )

    primary_palette = ft.Screenshot(
        ft.Row(
            key=ft.ScrollKey("primary_palette"),
            wrap=True,
            controls=[
                swatch("Primary", ft.Colors.PRIMARY, ft.Colors.ON_PRIMARY),
                swatch(
                    "Primary Ctr",
                    ft.Colors.PRIMARY_CONTAINER,
                    ft.Colors.ON_PRIMARY_CONTAINER,
                ),
                swatch(
                    "Primary Fix", ft.Colors.PRIMARY_FIXED, ft.Colors.ON_PRIMARY_FIXED
                ),
                swatch(
                    "Primary Dim",
                    ft.Colors.PRIMARY_FIXED_DIM,
                    ft.Colors.ON_PRIMARY_FIXED,
                ),
            ],
        )
    )

    secondary_palette = ft.Screenshot(
        ft.Row(
            key=ft.ScrollKey("secondary_palette"),
            wrap=True,
            controls=[
                swatch("Secondary", ft.Colors.SECONDARY, ft.Colors.ON_SECONDARY),
                swatch(
                    "Secondary Ctr",
                    ft.Colors.SECONDARY_CONTAINER,
                    ft.Colors.ON_SECONDARY_CONTAINER,
                ),
                swatch(
                    "Secondary Fix",
                    ft.Colors.SECONDARY_FIXED,
                    ft.Colors.ON_SECONDARY_FIXED,
                ),
                swatch(
                    "Secondary Dim",
                    ft.Colors.SECONDARY_FIXED_DIM,
                    ft.Colors.ON_SECONDARY_FIXED,
                ),
            ],
        )
    )

    tertiary_palette = ft.Screenshot(
        ft.Row(
            key=ft.ScrollKey("tertiary_palette"),
            wrap=True,
            controls=[
                swatch("Tertiary", ft.Colors.TERTIARY, ft.Colors.ON_TERTIARY),
                swatch(
                    "Tertiary Ctr",
                    ft.Colors.TERTIARY_CONTAINER,
                    ft.Colors.ON_TERTIARY_CONTAINER,
                ),
                swatch(
                    "Tertiary Fix",
                    ft.Colors.TERTIARY_FIXED,
                    ft.Colors.ON_TERTIARY_FIXED,
                ),
                swatch(
                    "Tertiary Dim",
                    ft.Colors.TERTIARY_FIXED_DIM,
                    ft.Colors.ON_TERTIARY_FIXED,
                ),
            ],
        )
    )

    surface_palette = ft.Screenshot(
        ft.Row(
            key=ft.ScrollKey("surface_roles"),
            wrap=True,
            controls=[
                swatch("Surface", ft.Colors.SURFACE, ft.Colors.ON_SURFACE),
                swatch("Surface Br", ft.Colors.SURFACE_BRIGHT, ft.Colors.ON_SURFACE),
                swatch("Surface Dim", ft.Colors.SURFACE_DIM, ft.Colors.ON_SURFACE),
                swatch("Surface Tint", ft.Colors.SURFACE_TINT, ft.Colors.ON_SURFACE),
                swatch("Container", ft.Colors.SURFACE_CONTAINER, ft.Colors.ON_SURFACE),
                swatch(
                    "Ctr High", ft.Colors.SURFACE_CONTAINER_HIGH, ft.Colors.ON_SURFACE
                ),
                swatch(
                    "Ctr Highest",
                    ft.Colors.SURFACE_CONTAINER_HIGHEST,
                    ft.Colors.ON_SURFACE,
                ),
                swatch(
                    "Ctr Low", ft.Colors.SURFACE_CONTAINER_LOW, ft.Colors.ON_SURFACE
                ),
                swatch(
                    "Ctr Lowest",
                    ft.Colors.SURFACE_CONTAINER_LOWEST,
                    ft.Colors.ON_SURFACE,
                ),
            ],
        )
    )

    accents_palette = ft.Screenshot(
        ft.Row(
            key=ft.ScrollKey("accents_palette"),
            wrap=True,
            controls=[
                swatch(
                    "Inverse", ft.Colors.INVERSE_SURFACE, ft.Colors.ON_INVERSE_SURFACE
                ),
                swatch(
                    "Inverse Pri",
                    ft.Colors.INVERSE_PRIMARY,
                    ft.Colors.ON_INVERSE_SURFACE,
                ),
                swatch("Scrim", ft.Colors.SCRIM, ft.Colors.ON_INVERSE_SURFACE),
                swatch("Outline", ft.Colors.OUTLINE, ft.Colors.ON_SURFACE_VARIANT),
                swatch("Outline Var", ft.Colors.OUTLINE_VARIANT, ft.Colors.ON_SURFACE),
                swatch("Error", ft.Colors.ERROR, ft.Colors.ON_ERROR),
                swatch(
                    "Error Ctr", ft.Colors.ERROR_CONTAINER, ft.Colors.ON_ERROR_CONTAINER
                ),
            ],
        )
    )

    buttons = ft.Screenshot(
        ft.Row(
            wrap=True,
            controls=[
                ft.FilledButton(
                    "Primary button",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=14),
                        padding=ft.Padding.symmetric(horizontal=24, vertical=12),
                    ),
                ),
                ft.FilledTonalButton(
                    "Tonal secondary",
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=14),
                        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                    ),
                ),
                ft.OutlinedButton(
                    "Surface variant",
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(width=2, color=ft.Colors.OUTLINE),
                        shape=ft.RoundedRectangleBorder(radius=14),
                        padding=ft.Padding.symmetric(horizontal=20, vertical=12),
                    ),
                ),
                ft.TextButton(
                    "Tertiary text",
                    style=ft.ButtonStyle(
                        color=ft.Colors.TERTIARY,
                        overlay_color=ft.Colors.TERTIARY_CONTAINER,
                        shape=ft.RoundedRectangleBorder(radius=14),
                    ),
                ),
                ft.IconButton(
                    icon=ft.Icons.FAVORITE,
                    icon_color=ft.Colors.ON_TERTIARY_CONTAINER,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.TERTIARY_CONTAINER,
                        shape=ft.CircleBorder(),
                        overlay_color=ft.Colors.TERTIARY,
                    ),
                ),
                ft.FloatingActionButton(
                    icon=ft.Icons.ADD,
                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                    foreground_color=ft.Colors.ON_SECONDARY_CONTAINER,
                    shape=ft.CircleBorder(),
                ),
            ],
        )
    )

    themed_card = ft.Screenshot(
        ft.Card(
            key=ft.ScrollKey("themed_card"),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            "Card on surface container",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.ON_SURFACE,
                        ),
                        ft.Text(
                            "Uses outline variant border and shadow color.",
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                        ft.ListTile(
                            title=ft.Text("Selected list tile"),
                            leading=ft.Icon(ft.Icons.PALETTE, color=ft.Colors.PRIMARY),
                            selected=True,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGH,
                            selected_color=ft.Colors.ON_PRIMARY,
                            trailing=ft.Switch(value=True),
                        ),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                padding=10,
            ),
        )
    )

    error_banner = ft.Screenshot(
        ft.Container(
            key=ft.ScrollKey("error_banner"),
            bgcolor=ft.Colors.ERROR_CONTAINER,
            border_radius=ft.BorderRadius.all(10),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ERROR, color=ft.Colors.ON_ERROR_CONTAINER),
                    ft.Text(
                        "Error container background with on-error text.",
                        color=ft.Colors.ON_ERROR_CONTAINER,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
    )

    flet_app.page.add(
        ft.Column(
            controls=[
                buttons,
                primary_palette,
                secondary_palette,
                tertiary_palette,
                surface_palette,
                accents_palette,
                themed_card,
                error_banner,
            ],
        )
    )
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "buttons",
        await buttons.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    await flet_app.page.scroll_to(scroll_key="primary_palette", duration=0)
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "primary_palette",
        await primary_palette.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    await flet_app.page.scroll_to(scroll_key="secondary_palette", duration=0)
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "secondary_palette",
        await secondary_palette.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    await flet_app.page.scroll_to(scroll_key="tertiary_palette", duration=0)
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "tertiary_palette",
        await tertiary_palette.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    await flet_app.page.scroll_to(scroll_key="surface_roles", duration=0)
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "surface_roles",
        await surface_palette.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    await flet_app.page.scroll_to(scroll_key="accents_palette", duration=0)
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "accents_palette",
        await accents_palette.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    await flet_app.page.scroll_to(scroll_key="themed_card", duration=0)
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "themed_card",
        await themed_card.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )

    await flet_app.page.scroll_to(scroll_key="error_banner", duration=0)
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        "error_banner",
        await error_banner.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )
