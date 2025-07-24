import logging
from pathlib import Path

import apps.hello_world as app
import flet as ft
import pytest
import pytest_asyncio

logging.basicConfig(level=logging.DEBUG)


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    flet_app = ft.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        flet_app_main=app.main,
        test_path=request.fspath,
    )
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest.mark.asyncio(loop_scope="module")
async def test_app(flet_app: ft.FletTestApp):
    await flet_app.tester.pump_and_settle()
    finder = await flet_app.tester.find_by_text("Hello, world!")
    assert finder.count == 1
    # bytes = await flet_app.tester.take_screenshot("scr1")
    # p = Path(get_current_script_dir(), "scr_1.png")
    # print(p)
    # with open(p, "wb") as f:
    #     f.write(bytes)


@pytest.mark.asyncio(loop_scope="module")
async def test_1(flet_app: ft.FletTestApp):
    print("Test 1")


@pytest.mark.asyncio(loop_scope="module")
async def test_2(flet_app: ft.FletTestApp):
    print("Test 2")
