from pathlib import Path

import pytest_asyncio

import flet.testing as ftt


def create_flet_app(request):
    params = getattr(request, "param", {})
    return ftt.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        test_path=request.fspath,
        flet_app_main=params.get("flet_app_main"),
        assets_dir=Path(__file__).resolve().parent / "assets",
    )


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    flet_app = create_flet_app(request)
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()


@pytest_asyncio.fixture(scope="function")
async def flet_app_function(request):
    flet_app = create_flet_app(request)
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()
