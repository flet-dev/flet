from pathlib import Path

import pytest_asyncio

import flet.testing as ftt


@pytest_asyncio.fixture(scope="module")
async def flet_app(request):
    params = getattr(request, "param", {})
    flet_app = ftt.FletTestApp(
        flutter_app_dir=(Path(__file__).parent / "../../../../../client").resolve(),
        test_path=request.fspath,
        flet_app_main=params.get("flet_app_main"),
        assets_dir=Path(__file__).resolve().parent / "assets",
    )
    await flet_app.start()
    yield flet_app
    await flet_app.teardown()
