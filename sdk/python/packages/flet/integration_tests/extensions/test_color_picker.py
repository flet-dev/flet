import pytest

import flet.testing as ftt
from flet_color_picker import ColorPicker


@pytest.mark.asyncio(loop_scope="module")
async def test_color_picker_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ColorPicker(
            picker_color="#ff0000",
            color_picker_width=320,
        ),
    )
