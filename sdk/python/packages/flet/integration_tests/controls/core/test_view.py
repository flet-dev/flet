import asyncio

import pytest
import pytest_asyncio

import flet as ft
import flet.testing as ftt


# Create a new flet_app instance for each test method
@pytest_asyncio.fixture(scope="function", autouse=True)
def flet_app(flet_app_function):
    return flet_app_function


async def _wait_for(flet_app: ftt.FletTestApp, condition, timeout: float = 5.0):
    """Pumps frames until `condition()` holds, as events reach Python later."""
    loop = asyncio.get_running_loop()
    deadline = loop.time() + timeout
    while not condition() and loop.time() < deadline:
        await flet_app.tester.pump(duration=ft.Duration(milliseconds=100))
        await asyncio.sleep(0.05)
    return condition()


@pytest.mark.asyncio(loop_scope="function")
async def test_on_size_change(flet_app: ftt.FletTestApp):
    """`View.on_size_change` reports the view's size when shown and after a resize."""
    sizes = []

    flet_app.resize_page(600, 450)
    flet_app.page.views.clear()
    flet_app.page.views.append(
        ft.View(
            route="/",
            size_change_interval=0,
            on_size_change=lambda e: sizes.append((e.width, e.height)),
            controls=[ft.Text("View")],
        )
    )
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    assert await _wait_for(flet_app, lambda: len(sizes) > 0), (
        "on_size_change didn't fire when the view was shown"
    )
    assert sizes[-1] == (pytest.approx(600), pytest.approx(450))

    width, height = sizes[-1]
    flet_app.page.window.width -= 100
    flet_app.page.window.height -= 50
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    expected = (pytest.approx(width - 100), pytest.approx(height - 50))
    assert await _wait_for(flet_app, lambda: sizes[-1] == expected), (
        f"on_size_change didn't report the new size, got {sizes}"
    )
