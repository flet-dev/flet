import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_cupertino_sliding_segmented_button_basic(
    flet_app: ftt.FletTestApp, request
):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.CupertinoSlidingSegmentedButton(
            controls=[
                ft.Text("One"),
                ft.Text("Two"),
                ft.Text("Ten"),
            ],
        ),
    )
