import pytest

import examples.apps.declarative.tic_tac_toe.main as tic_tac_toe
import flet as ft
import flet.testing as ftt


def tic_tac_toe_main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.render(tic_tac_toe.Game)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": tic_tac_toe_main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_declarative_tic_tac_toe(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(230 * 1.5, 230)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    for square_key in ["square_0", "square_1", "square_4", "square_8"]:
        square = await flet_app_function.tester.find_by_key(square_key)
        assert square.count == 1
        await flet_app_function.tester.tap(square)
        await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Next player: X")).count == 1
    assert (await flet_app_function.tester.find_by_text("Go to move #4")).count == 1

    flet_app_function.assert_screenshot(
        "declarative_tic_tac_toe",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
