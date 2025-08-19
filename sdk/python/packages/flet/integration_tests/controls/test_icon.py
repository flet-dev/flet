import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_icon_basic(flet_app: ftt.FletTestApp, request):
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
