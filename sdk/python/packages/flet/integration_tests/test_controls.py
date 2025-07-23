import logging
from pathlib import Path

import flet as ft
import pytest
import pytest_asyncio

logging.basicConfig(level=logging.DEBUG)


@pytest_asyncio.fixture
async def flet_app():
    flet_app = ft.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        tcp_port=9010,
    )
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest.mark.asyncio
async def test_hello(flet_app: ft.FletTestApp):
    print("test_hello")
    flet_app.page.add(ft.Button("Click me"))
    await flet_app.tester.pump_and_settle()
    finder = await flet_app.tester.find_by_text("Click me")
    assert finder.count == 1
