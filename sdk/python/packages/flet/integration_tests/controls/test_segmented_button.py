import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_segmented_button_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.SegmentedButton(
            selected_icon=ft.Icon(ft.Icons.CHECK_SHARP),
            selected=["1"],
            allow_empty_selection=True,
            allow_multiple_selection=True,
            segments=[
                ft.Segment(
                    value="1",
                    label=ft.Text("1"),
                    icon=ft.Icon(ft.Icons.LOOKS_ONE),
                ),
                ft.Segment(
                    value="2",
                    label=ft.Text("2"),
                    icon=ft.Icon(ft.Icons.LOOKS_TWO),
                ),
                ft.Segment(
                    value="3",
                    label=ft.Text("3"),
                    icon=ft.Icon(ft.Icons.LOOKS_3),
                ),
                ft.Segment(
                    value="4",
                    label=ft.Text("4"),
                    icon=ft.Icon(ft.Icons.LOOKS_4),
                ),
            ],
        ),
    )
