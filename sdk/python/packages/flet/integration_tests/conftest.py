from pathlib import Path

import pytest_asyncio

import flet.testing as ftt
from flet.controls.context import _context_page, context


def create_flet_app(request):
    params = getattr(request, "param", {})
    return ftt.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        test_path=request.fspath,
        flet_app_main=params.get("flet_app_main"),
        skip_pump_and_settle=params.get("skip_pump_and_settle", False),
        assets_dir=Path(__file__).resolve().parent / "assets",
    )


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    """
    Module-scoped Flet app fixture.
    Does not bind `ft.context.page`.
    """
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
    flet_app = create_flet_app(request)
    await flet_app.start()

    # make page available via ft.context.page
    token = _context_page.set(flet_app.page)
    context.reset_auto_update()

    try:
        yield flet_app
    finally:
        _context_page.reset(token)  # restore previous context to avoid leakage
        await flet_app.teardown()
