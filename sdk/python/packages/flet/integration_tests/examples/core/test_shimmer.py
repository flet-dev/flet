import pytest

import flet as ft
import flet.testing as ftt
from examples.controls.shimmer import basic_placeholder, custom_gradient


@pytest.mark.skip(reason="The test is flaky on CI")
@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    page = flet_app_function.page
    page.enable_screenshots = True
    flet_app_function.resize_page(350, 280)
    page.update()
    await flet_app_function.tester.pump_and_settle()
    page.add(
        ft.Shimmer(
            base_color=ft.Colors.with_opacity(0.3, ft.Colors.GREY_400),
            highlight_color=ft.Colors.WHITE,
            content=ft.Column(
                controls=[
                    ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                    ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                    ft.Container(height=80, bgcolor=ft.Colors.GREY_300),
                ],
            ),
        )
    )

    images = []
    for counter in range(10):
        await flet_app_function.tester.pump(100)
        name = f"image_for_docs_{counter}"
        images.append(name)
        flet_app_function.assert_screenshot(
            name,
            await flet_app_function.page.take_screenshot(
                pixel_ratio=flet_app_function.screenshots_pixel_ratio
            ),
        )

    flet_app_function.create_gif(
        image_names=images, output_name="image_for_docs", duration=200
    )


@pytest.mark.skip(reason="The test is flaky on CI")
@pytest.mark.parametrize(
    "flet_app_function",
    [
        {
            "flet_app_main": basic_placeholder.main,
            "skip_pump_and_settle": True,
        }
    ],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic_placeholder(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.controls[0].disabled = True
    flet_app_function.resize_page(500, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.page.controls[0].disabled = False
    flet_app_function.page.update()
    for _ in range(5):
        await flet_app_function.tester.pump(100)
    flet_app_function.assert_screenshot(
        "basic_placeholder",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )


@pytest.mark.skip(reason="The test is flaky on CI")
@pytest.mark.parametrize(
    "flet_app_function",
    [
        {
            "flet_app_main": custom_gradient.main,
            "skip_pump_and_settle": True,
        }
    ],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_custom_gradient(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.enable_screenshots = True
    flet_app_function.page.controls[0].disabled = True
    flet_app_function.resize_page(220, 300)
    flet_app_function.page.update()
    await flet_app_function.tester.pump_and_settle()

    flet_app_function.page.controls[0].disabled = False
    flet_app_function.page.update()
    for _ in range(8):
        await flet_app_function.tester.pump(100)
    flet_app_function.assert_screenshot(
        "custom_gradient",
        await flet_app_function.page.take_screenshot(
            pixel_ratio=flet_app_function.screenshots_pixel_ratio
        ),
    )
