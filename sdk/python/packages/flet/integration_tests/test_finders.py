from pathlib import Path

import apps.finders as app
import flet as ft
import flet.testing as ftt
import pytest
import pytest_asyncio


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    flet_app = ftt.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        flet_app_main=app.main,
        test_path=request.fspath,
    )
    await flet_app.start()
    await flet_app.tester.pump_and_settle()
    yield flet_app
    await flet_app.teardown()


@pytest.mark.asyncio(loop_scope="module")
async def test_find_by_text(flet_app: ftt.FletTestApp):
    finder = await flet_app.tester.find_by_text("Hello, world!")
    assert finder.count == 2


@pytest.mark.asyncio(loop_scope="module")
async def test_find_by_text_containing(flet_app: ftt.FletTestApp):
    finder = await flet_app.tester.find_by_text_containing("Hello, world!")
    assert finder.count == 3

    finder = await flet_app.tester.find_by_text_containing("Hello")
    assert finder.count == 4

    finder = await flet_app.tester.find_by_text_containing("(\\s+)world")
    assert finder.count == 3

    finder = await flet_app.tester.find_by_text_containing("world!$")
    assert finder.count == 3


@pytest.mark.asyncio(loop_scope="module")
async def test_find_by_icon(flet_app: ftt.FletTestApp):
    finder = await flet_app.tester.find_by_icon(ft.Icons.ADD_A_PHOTO)
    assert finder.count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_find_by_tooltip(flet_app: ftt.FletTestApp):
    finder = await flet_app.tester.find_by_tooltip("Tooltip1")
    assert finder.count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_find_by_key(flet_app: ftt.FletTestApp):
    finder = await flet_app.tester.find_by_key("value_key_1")
    assert finder.count == 1

    finder = await flet_app.tester.find_by_key(ft.ScrollKey("scroll_key_1"))
    assert finder.count == 1
