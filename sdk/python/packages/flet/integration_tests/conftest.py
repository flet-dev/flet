from pathlib import Path

import pytest_asyncio

import flet.testing as ftt
from flet.controls.context import (
    _context_page,
    _update_behavior_context_var,
    context,
)


def create_flet_app(request):
    params = getattr(request, "param", {})
    return ftt.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        test_path=request.fspath,
        flet_app_main=params.get("flet_app_main"),
        skip_pump_and_settle=params.get("skip_pump_and_settle", False),
        assets_dir=params.get("assets_dir", Path(__file__).resolve().parent / "assets"),
    )


def _rearm_auto_update():
    """
    Restores the app-wide auto-update default before each test app starts.

    `ft.context.disable_auto_update()` at module scope sets a process-wide
    default, which is the documented way to turn auto-update off for an app.
    That is fine for a normal one-app process, but pytest runs many apps in one
    process and imports every test module during collection - so an example app
    such as `examples/apps/icons_browser` turns auto-update off for every test
    that follows it, making the suite order-dependent.

    Clearing any context-scoped value first ensures the enable lands on the
    app-wide default, which is what a freshly started session inherits.
    """
    _update_behavior_context_var.set(None)
    context.enable_auto_update()


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    """
    Module-scoped Flet app fixture.
    Does not bind `ft.context.page`.
    """
    _rearm_auto_update()
    flet_app = create_flet_app(request)
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest_asyncio.fixture(scope="function")
async def flet_app_function(request):
    """
    Function-scoped Flet app fixture.
    Binds and resets `ft.context.page` per test.
    """
    _rearm_auto_update()

    flet_app = create_flet_app(request)
    await flet_app.start()

    # make page available via ft.context.page
    token = _context_page.set(flet_app.page)
    # Give this test its own UpdateBehavior so a `disable_auto_update()` call
    # made by the test itself does not leak into the shared default.
    context.reset_auto_update()

    try:
        yield flet_app
    finally:
        _context_page.reset(token)  # restore previous context to avoid leakage
        context.disable_components_mode()
        await flet_app.teardown()
