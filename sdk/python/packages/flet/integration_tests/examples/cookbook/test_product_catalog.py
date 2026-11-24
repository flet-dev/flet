import pytest

import examples.cookbook.create_flet_app.product_catalog.main as product_catalog
import flet as ft
import flet.testing as ftt


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": product_catalog.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_product_catalog(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app_function.page.enable_screenshots = True
    flet_app_function.resize_page(420, 420)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Catalog")).count == 1
    assert (await flet_app_function.tester.find_by_text("Desk Lamp")).count == 1
    assert (await flet_app_function.tester.find_by_text("Wireless Mouse")).count == 1
    assert (await flet_app_function.tester.find_by_text("Notebook")).count == 1
    assert (await flet_app_function.tester.find_by_text("SALE")).count == 1
    assert (await flet_app_function.tester.find_by_text("Buy")).count == 3

    flet_app_function.assert_screenshot(
        "product_catalog",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
