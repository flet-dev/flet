import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


@pytest.mark.asyncio(loop_scope="function")
async def test_zoom_reports_the_transform_still_applied(flet_app: ftt.FletTestApp):
    events: list[ft.InteractiveViewerTransformEvent] = []

    def on_transform(e: ft.InteractiveViewerTransformEvent):
        events.append(e)

    flet_app.page.add(
        viewer := ft.InteractiveViewer(
            width=200,
            height=200,
            min_scale=0.5,
            max_scale=4,
            boundary_margin=100,
            interaction_update_interval=0,
            on_transform_changed=on_transform,
            content=ft.Container(width=200, height=200, bgcolor=ft.Colors.BLUE),
        )
    )
    await flet_app.tester.pump_and_settle()

    await viewer.zoom(2)
    await flet_app.tester.pump_and_settle()

    transform = await viewer.get_transform()
    assert transform.scale == pytest.approx(2)
    assert events
    last = events[-1]
    assert last.scale == pytest.approx(transform.scale)
    assert last.translation_x == pytest.approx(transform.translation_x)
    assert last.translation_y == pytest.approx(transform.translation_y)
    assert last.translation_z == pytest.approx(transform.translation_z)
    assert last.matrix == pytest.approx(transform.matrix)
    assert await viewer.get_scale() == pytest.approx(transform.scale)
