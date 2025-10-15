import pytest

import flet as ft
import flet.canvas as cv
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        cv.Canvas(
            width=160,
            height=160,
            shapes=[
                cv.Rect(
                    0,
                    0,
                    160,
                    160,
                    paint=ft.Paint(
                        color=ft.Colors.BLUE_100,
                        style=ft.PaintingStyle.FILL,
                    ),
                ),
                cv.Circle(
                    80,
                    80,
                    50,
                    paint=ft.Paint(
                        color=ft.Colors.BLUE_400,
                        style=ft.PaintingStyle.FILL,
                    ),
                ),
            ],
        ),
    )
