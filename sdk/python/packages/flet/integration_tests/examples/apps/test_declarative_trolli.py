import sys
from pathlib import Path

import pytest

import flet as ft
import flet.testing as ftt

TROLLI_DIR = Path(__file__).resolve().parents[5] / "examples/apps/declarative/trolli"
sys.path.insert(0, str(TROLLI_DIR))

import main as trolli  # noqa: E402


def trolli_main(page: ft.Page):
    page.render(trolli.App)


@pytest.mark.parametrize(
    "flet_app_function",
    [
        {
            "flet_app_main": trolli_main,
            "assets_dir": Path(trolli.__file__).parent / "assets",
        }
    ],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_declarative_trolli(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(1100, 1100 * 0.625)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    board = await flet_app_function.tester.find_by_text("My First Board")
    assert board.count >= 1
    await flet_app_function.tester.tap(board.at(0))
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("To Do")).count == 1
    assert (await flet_app_function.tester.find_by_text("Doing")).count == 1
    assert (await flet_app_function.tester.find_by_text("Done")).count == 1
    assert (
        await flet_app_function.tester.find_by_text("Drag cards between lists")
    ).count == 1

    flet_app_function.assert_screenshot(
        "declarative_trolli",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
