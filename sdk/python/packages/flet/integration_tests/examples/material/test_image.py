import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_image_for_docs(flet_app_function: ftt.FletTestApp, request):
    # current_dir = Path(__file__).parent
    # assets_dir = current_dir.parents[2] / "assets"
    # assets_dir.mkdir(parents=True, exist_ok=True)
    # sample_src = current_dir / "sample_image.jpg"
    # target = assets_dir / "sample_image.jpg"
    # if sample_src.exists():
    #     shutil.copy(sample_src, target)
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        ft.Image(
            src="sample_image.jpg",
            width=120,
            height=120,
            border_radius=8,
        ),
    )
