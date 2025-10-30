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
        ft.Column(
            [  # material
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.ABC, color=ft.Colors.PINK),
                        ft.Icon(
                            ft.Icons.AUDIOTRACK, color=ft.Colors.GREEN_400, size=30
                        ),
                        ft.Icon(ft.Icons.AC_UNIT, color=ft.Colors.BLUE, size=50),
                        ft.Icon(ft.Icons.SETTINGS, color="#c1c1c1"),
                        ft.Icon(ft.Icons.ALARM, size=40),
                    ]
                ),
                # cupertino
                ft.Row(
                    controls=[
                        ft.Icon(ft.CupertinoIcons.AIRPLANE, color=ft.Colors.PINK),
                        ft.Icon(
                            icon=ft.CupertinoIcons.CUBE_BOX,
                            color=ft.Colors.GREEN_400,
                            size=30,
                        ),
                        ft.Icon(
                            icon=ft.CupertinoIcons.ARCHIVEBOX,
                            color=ft.Colors.BLUE,
                            size=50,
                        ),
                        ft.Icon(icon=ft.CupertinoIcons.BAG, color="#c1c1c1"),
                        ft.Icon(ft.CupertinoIcons.ALARM, size=40),
                    ]
                ),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theme(flet_app: ftt.FletTestApp):
    flet_app.page.theme = ft.Theme(
        icon_theme=ft.IconTheme(
            color=ft.Colors.GREEN_900,
            size=100,
            apply_text_scaling=True,  # doesn't show on screenshot
            fill=0.5,  # doesn't show on screenshow
            opacity=0.5,
            optical_size=48,  # doesn't show pon screenshot
            grade=-10,  # doesn't show on screenshot
            weight=10,  # doesn't show on screenshot
            shadows=ft.BoxShadow(color=ft.Colors.YELLOW, blur_radius=10),
        )
    )
    flet_app.page.enable_screenshots = True
    await flet_app.resize_page(400, 600)

    scr_1 = ft.Screenshot(
        ft.Column(
            [  # material
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.ABC,
                            fill=0,
                            # color=ft.Colors.PINK,
                            apply_text_scaling=False,
                            opacity=0.1,
                            optical_size=200,
                        ),
                        ft.Icon(
                            ft.Icons.AUDIOTRACK,
                            color=ft.Colors.GREEN_400,
                            size=30,
                            shadows=[
                                ft.BoxShadow(color=ft.Colors.YELLOW, blur_radius=10),
                                ft.BoxShadow(color=ft.Colors.RED, blur_radius=5),
                            ],
                        ),
                        ft.Icon(
                            ft.Icons.AC_UNIT,
                            color=ft.Colors.BLUE,
                            size=50,
                        ),
                        ft.Icon(
                            ft.Icons.SETTINGS,
                            color="#c1c1c1",
                        ),
                        ft.Icon(
                            ft.Icons.ALARM,
                            size=40,
                        ),
                    ]
                ),
                # cupertino
                ft.Row(
                    controls=[
                        ft.Icon(
                            ft.CupertinoIcons.AIRPLANE,
                            # color=ft.Colors.PINK,
                        ),
                        ft.Icon(
                            icon=ft.CupertinoIcons.CUBE_BOX,
                            color=ft.Colors.GREEN_400,
                            size=30,
                        ),
                        ft.Icon(
                            icon=ft.CupertinoIcons.ARCHIVEBOX,
                            color=ft.Colors.BLUE,
                            size=50,
                        ),
                        ft.Icon(
                            icon=ft.CupertinoIcons.BAG,
                            color="#c1c1c1",
                        ),
                        ft.Icon(
                            ft.CupertinoIcons.ALARM,
                            size=40,
                        ),
                    ]
                ),
            ]
        ),
    )
    flet_app.page.add(scr_1)
    await flet_app.tester.pump_and_settle()

    flet_app.assert_screenshot(
        "theme_1",
        await scr_1.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )
