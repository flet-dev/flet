import random
from pathlib import Path

import pytest

import examples.tutorials.solitaire_declarative.solitaire_final.main as solitaire
import flet as ft
import flet.testing as ftt


def solitaire_main(page: ft.Page):
    random.seed(0)
    page.render(solitaire.App)


@pytest.mark.parametrize(
    "flet_app_function",
    [
        {
            "flet_app_main": solitaire_main,
            "assets_dir": Path(solitaire.__file__).parent / "assets",
        }
    ],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_solitaire_declarative(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(1000, 760)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("New Game")).count == 1

    flet_app_function.assert_screenshot(
        "solitaire_declarative",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
