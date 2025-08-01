import os
import sys
from pathlib import Path

import flet as ft
import flet.testing as ftt
import pytest
import pytest_asyncio

examples_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
print("examples_dir:", examples_dir)
sys.path.append(examples_dir)

from examples.controls.checkbox import basic as example1


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    flet_app = ftt.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../../client").resolve(),
        flet_app_main=example1.main,
        test_path=request.fspath,
    )
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest.mark.asyncio(loop_scope="module")
async def test_basic_checkbox(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Checkbox(),
    )

@pytest.mark.asyncio(loop_scope="module")
async def test_checkbox_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app.page.theme = ft.Theme(
        checkbox_theme=ft.CheckboxTheme(check_color=ft.Colors.RED))
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Checkbox(value=True),
    )

@pytest.mark.asyncio(loop_scope="module")
async def test_example1(flet_app: ftt.FletTestApp, request):
    tester = flet_app.tester
    await tester.pump_and_settle()
    checkbox_text = await tester.find_by_text("Unchecked by default checkbox")
    assert checkbox_text.count == 1

    # tap open dialog
    # dialog_btn = await tester.find_by_key(123)
    # assert dialog_btn.count == 1
    # await tester.tap(dialog_btn)
    # await tester.pump_and_settle()
    # action_sheet = await tester.find_by_key(456)
    # assert action_sheet.count == 1
