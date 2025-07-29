import logging
import os
from pathlib import Path

import flet as ft
import flet.testing as ftt
import pytest
import pytest_asyncio

logging.basicConfig(level=logging.DEBUG)

pixel_ratio = float(os.getenv("FLET_TEST_SCREENSHOTS_PIXEL_RATIO", "2.0"))


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    flet_app = ftt.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../../client").resolve(),
        test_path=request.fspath,
    )
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest.mark.asyncio(loop_scope="module")
async def test_basic_textfield(flet_app: ftt.FletTestApp, request):
    flet_app.page.add(txt := ft.TextField(key=ft.ScreenshotKey("scr1")))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.screenshot.capture_async(
            screenshot_key=txt.key, pixel_ratio=pixel_ratio
        ),
    )
