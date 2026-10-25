import asyncio

import pytest

import flet as ft
import flet.testing as ftt


class _Refresh:
    """Holds an `on_refresh` handler that keeps the refresh going until released."""

    def __init__(self, error: bool = False):
        self.error = error
        self.calls = 0
        self.started = asyncio.Event()
        self.released = asyncio.Event()

    async def handle(self, e: ft.Event[ft.RefreshIndicator]):
        self.calls += 1
        self.started.set()
        await self.released.wait()
        if self.error:
            raise RuntimeError("Refresh failed")


def _list(count: int = 10) -> ft.ListView:
    return ft.ListView(controls=[ft.ListTile(title=f"Item {i}") for i in range(count)])


async def _add(flet_app: ftt.FletTestApp, indicator: ft.RefreshIndicator):
    """Shows `indicator` alone on the page and returns its screenshot host."""
    flet_app.page.clean()
    await flet_app.tester.pump_and_settle()
    screenshot = ft.Screenshot(indicator)
    flet_app.page.add(screenshot)
    await flet_app.tester.pump_and_settle()
    return screenshot


async def _pull(flet_app: ftt.FletTestApp):
    await flet_app.tester.drag(
        await flet_app.tester.find_by_text("Item 0"), ft.Offset(0, 300)
    )


async def _wait_started(flet_app: ftt.FletTestApp, refresh: _Refresh):
    """Pumps frames until the indicator has reached `on_refresh`."""
    for _ in range(30):
        if refresh.started.is_set():
            break
        await flet_app.tester.pump(duration=ft.Duration(milliseconds=100))
    assert refresh.started.is_set()
    # let the indicator finish settling at its refresh position
    for _ in range(5):
        await flet_app.tester.pump(duration=ft.Duration(milliseconds=100))


async def _assert_refreshing(
    flet_app: ftt.FletTestApp, name: str, screenshot: ft.Screenshot
):
    flet_app.assert_screenshot(
        name,
        await screenshot.capture(pixel_ratio=flet_app.screenshots_pixel_ratio),
    )


async def _release(flet_app: ftt.FletTestApp, refresh: _Refresh):
    """Ends the refresh; settling only completes once the spinner is gone."""
    refresh.released.set()
    await flet_app.tester.pump_and_settle()


@pytest.mark.asyncio(loop_scope="module")
async def test_pull(flet_app: ftt.FletTestApp):
    """Pulling the content down calls `on_refresh`."""
    refresh = _Refresh()
    await _add(
        flet_app,
        ft.RefreshIndicator(
            width=300, height=300, content=_list(), on_refresh=refresh.handle
        ),
    )

    await _pull(flet_app)
    await _wait_started(flet_app, refresh)

    await _release(flet_app, refresh)
    assert refresh.calls == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_pull_short_list(flet_app: ftt.FletTestApp):
    """Content too short to scroll can still be pulled."""
    refresh = _Refresh()
    await _add(
        flet_app,
        ft.RefreshIndicator(
            width=300, height=300, content=_list(1), on_refresh=refresh.handle
        ),
    )

    await _pull(flet_app)
    await _wait_started(flet_app, refresh)

    await _release(flet_app, refresh)
    assert refresh.calls == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_show(flet_app: ftt.FletTestApp, request):
    """`show()` calls `on_refresh` and shows the indicator without a pull."""
    refresh = _Refresh()
    indicator = ft.RefreshIndicator(
        width=300, height=300, content=_list(), on_refresh=refresh.handle
    )
    screenshot = await _add(flet_app, indicator)

    await indicator.show()
    await _wait_started(flet_app, refresh)
    await _assert_refreshing(flet_app, request.node.name, screenshot)

    await _release(flet_app, refresh)
    assert refresh.calls == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_style(flet_app: ftt.FletTestApp, request):
    """The indicator is drawn with `color`, `bgcolor`, `stroke_width` and
    `elevation`."""
    refresh = _Refresh()
    indicator = ft.RefreshIndicator(
        width=300,
        height=300,
        content=_list(),
        on_refresh=refresh.handle,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE,
        stroke_width=5,
        elevation=10,
    )
    screenshot = await _add(flet_app, indicator)

    await indicator.show()
    await _wait_started(flet_app, refresh)
    await _assert_refreshing(flet_app, request.node.name, screenshot)

    await _release(flet_app, refresh)


@pytest.mark.asyncio(loop_scope="module")
async def test_displacement_and_edge_offset(flet_app: ftt.FletTestApp, request):
    """The indicator rests `displacement` below `edge_offset`."""
    refresh = _Refresh()
    indicator = ft.RefreshIndicator(
        width=300,
        height=300,
        content=_list(),
        on_refresh=refresh.handle,
        displacement=100,
        edge_offset=50,
    )
    screenshot = await _add(flet_app, indicator)

    await indicator.show()
    await _wait_started(flet_app, refresh)
    await _assert_refreshing(flet_app, request.node.name, screenshot)

    await _release(flet_app, refresh)


@pytest.mark.asyncio(loop_scope="module")
async def test_hides_when_handler_raises(flet_app: ftt.FletTestApp):
    """The indicator hides even when `on_refresh` raises."""
    refresh = _Refresh(error=True)
    indicator = ft.RefreshIndicator(
        width=300, height=300, content=_list(), on_refresh=refresh.handle
    )
    await _add(flet_app, indicator)

    await indicator.show()
    await _wait_started(flet_app, refresh)

    await _release(flet_app, refresh)
    assert refresh.calls == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_show_without_handler(flet_app: ftt.FletTestApp):
    """Without `on_refresh`, `show()` ends the refresh at once."""
    indicator = ft.RefreshIndicator(width=300, height=300, content=_list())
    await _add(flet_app, indicator)

    await indicator.show()
    await flet_app.tester.pump_and_settle()
