import logging
from pathlib import Path

import flet as ft
import pytest
import pytest_asyncio

logging.basicConfig(level=logging.DEBUG)


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    flet_app = ft.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        test_path=request.fspath,
    )
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest.mark.asyncio(loop_scope="module")
async def test_button_1(flet_app: ft.FletTestApp, request):
    flet_app.page.add(scr := ft.Screenshot(ft.Button("Click me")))
    await flet_app.tester.pump_and_settle()
    button = await flet_app.tester.find_by_text("Click me")
    assert button.count == 1
    await flet_app.tester.mouse_hover(button)
    flet_app.assert_screenshot(request.node.name, await scr.capture_async())


@pytest.mark.asyncio(loop_scope="module")
async def test_button_2(flet_app: ft.FletTestApp, request):
    flet_app.page.add(scr := ft.Screenshot(ft.Button("Something else!")))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(request.node.name, await scr.capture_async())
