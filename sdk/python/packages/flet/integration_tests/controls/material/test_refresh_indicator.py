import asyncio

import pytest

import flet as ft
import flet.testing as ftt


class _Refresh:
    """Holds an `on_refresh` handler that keeps the refresh going until released."""

    def __init__(self, error: bool = False):
        """
        Args:
            error: Whether the handler raises once released.
        """
        self.error = error
        self.calls = 0
        self.started = asyncio.Event()
        self.released = asyncio.Event()

    async def handle(self, e: ft.Event[ft.RefreshIndicator]):
        """Counts the call, then waits to be released, raising if `error` is set."""
        self.calls += 1
        self.started.set()
        await self.released.wait()
        if self.error:
            raise RuntimeError("Refresh failed")


def _list(count: int = 10) -> ft.ListView:
    """A list of `count` tiles titled "Item 0", "Item 1" and so on."""
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
    """Drags the list down from its first tile, far enough to start a refresh."""
    await flet_app.tester.drag(
        await flet_app.tester.find_by_text("Item 0"), ft.Offset(0, 300)
    )


async def _wait_started(flet_app: ftt.FletTestApp, refresh: _Refresh):
    """
    Pumps frames until the indicator has reached `on_refresh`, then a few more so
    it settles at its refresh position.
    """
    for _ in range(30):
        if refresh.started.is_set():
            break
        await flet_app.tester.pump(duration=ft.Duration(milliseconds=100))
    assert refresh.started.is_set()
    for _ in range(5):
        await flet_app.tester.pump(duration=ft.Duration(milliseconds=100))


async def _assert_refreshing(
    flet_app: ftt.FletTestApp, name: str, screenshot: ft.Screenshot
):
    """Compares a screenshot of the refreshing indicator with the `name` golden."""
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


@ft.component
def _RerenderingApp():
    """An indicator whose `on_refresh` re-renders it, showing a refresh count."""
    count, set_count = ft.use_state(0)

    async def refresh():
        """Bumps the count, which re-renders the app, then works a little longer."""
        set_count(count + 1)
        await asyncio.sleep(0.2)

    return ft.RefreshIndicator(
        width=300,
        height=300,
        content=ft.ListView([ft.Text(f"Pulled {count} times")]),
        on_refresh=refresh,
    )


def _rerendering_main(page: ft.Page):
    """Renders `_RerenderingApp` on the page."""
    page.render(_RerenderingApp)


@pytest.mark.parametrize(
    "flet_app_function", [{"flet_app_main": _rerendering_main}], indirect=True
)
@pytest.mark.asyncio(loop_scope="function")
async def test_hides_after_component_rerender(flet_app_function: ftt.FletTestApp):
    """
    The indicator hides when `on_refresh` re-renders the component. Settling
    the frames times out while it still spins.
    """
    tester = flet_app_function.tester
    indicator = next(
        c
        for c in flet_app_function.page.session.index.values()
        if isinstance(c, ft.RefreshIndicator)
    )

    await indicator.show()
    for _ in range(30):
        if (await tester.find_by_text("Pulled 1 times")).count:
            break
        await tester.pump(duration=ft.Duration(milliseconds=100))
    await asyncio.sleep(0.5)

    await tester.pump_and_settle()
    assert (await tester.find_by_text("Pulled 1 times")).count == 1
