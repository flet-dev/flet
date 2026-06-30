"""
Pytest plugin that exposes Flet integration-testing fixtures.

Registered as a ``pytest11`` entry point in flet's ``pyproject.toml`` so that any
test under a Flet app's ``tests/`` directory gets the ``flet_app`` /
``flet_app_function`` fixtures with zero conftest boilerplate.

Because a ``pytest11`` plugin is auto-loaded in *every* pytest run wherever
``flet`` is installed, this module must stay lightweight: it lives at the flet
top level (not under ``flet.testing``) so loading it does not pull in
``FletTestApp`` (numpy/Pillow/scikit-image). It imports nothing heavy at module
load time — ``flet.testing`` and ``flet_cli`` are imported lazily inside the
fixtures. ``pytest_asyncio`` is imported defensively — if it is missing, the
plugin loads as a no-op so it never breaks unrelated projects' pytest runs.
"""

import os
from pathlib import Path

try:
    import pytest_asyncio

    _HAS_ASYNCIO = True
except ImportError:  # pragma: no cover - plugin degrades to a no-op
    _HAS_ASYNCIO = False


def _is_device_mode() -> bool:
    # Device mode (app under test runs on-device with embedded Python) is the
    # default for `flet test` / `uv run pytest`. The Flet repo's own host-mode
    # tests opt out by setting FLET_TEST_DEVICE_MODE=0 (and override these
    # fixtures from their conftest anyway).
    return os.environ.get("FLET_TEST_DEVICE_MODE", "1").lower() not in (
        "0",
        "false",
        "no",
        "",
    )


def _import_app_main(app_path: str, module_name: str):
    """Import the user's app `main` callable from `app_path/<module_name>.py`."""
    import importlib
    import sys

    app_path = str(Path(app_path).resolve())
    if app_path not in sys.path:
        sys.path.insert(0, app_path)
    module = importlib.import_module(module_name)
    return module.main


def _resolve_flutter_test_host(device_mode: bool):
    """Return the Flutter test host dir, provisioning it on demand if needed."""
    host = os.environ.get("FLET_TEST_FLUTTER_APP_DIR")
    if host:
        return host
    if not device_mode:
        raise RuntimeError(
            "FLET_TEST_FLUTTER_APP_DIR is not set. Run tests with `flet test`, "
            "or set the environment variable to a Flutter test host directory."
        )
    # Lazily provision a built test host via flet-cli (cached by input hash).
    # The target platform/device come from FLET_TEST_PLATFORM / FLET_TEST_DEVICE
    # so `uv run pytest` can target a mobile emulator/device too (defaults to the
    # current desktop platform when unset).
    try:
        from flet_cli.commands.test_host import provision_test_host
    except ImportError as e:
        raise RuntimeError(
            "Provisioning a Flutter test host requires flet-cli. Install it "
            "with `pip install flet-cli` or run your tests with `flet test`."
        ) from e
    return str(
        provision_test_host(
            project_dir=os.getcwd(),
            platform_name=os.environ.get("FLET_TEST_PLATFORM"),
            device_id=os.environ.get("FLET_TEST_DEVICE"),
        )
    )


def _create_flet_app(request):
    import flet.testing as ftt

    params = getattr(request, "param", {})
    device_mode = _is_device_mode()
    flutter_app_dir = _resolve_flutter_test_host(device_mode)

    flet_app_main = params.get("flet_app_main")
    if not device_mode and flet_app_main is None:
        app_path = os.environ.get("FLET_TEST_APP_PATH")
        if app_path:
            module_name = os.environ.get("FLET_TEST_APP_MODULE", "main")
            flet_app_main = _import_app_main(app_path, module_name)

    assets_dir = params.get("assets_dir") or os.environ.get("FLET_TEST_ASSETS_DIR")

    return ftt.FletTestApp(
        flutter_app_dir=flutter_app_dir,
        device_mode=device_mode,
        flet_app_main=flet_app_main,
        test_path=request.fspath,
        skip_pump_and_settle=params.get("skip_pump_and_settle", False),
        assets_dir=assets_dir,
    )


if _HAS_ASYNCIO:

    @pytest_asyncio.fixture
    async def flet_app(request):
        """
        Function-scoped Flet app fixture: each test gets a fresh, isolated app.

        Does not bind `ft.context.page`. Use `flet_app.tester` to drive the UI.
        Function scope keeps the fixture on the same event loop as the test (the
        default with `asyncio_mode = "auto"`), which is required so the tester
        transport is serviced while the test awaits.
        """
        app = _create_flet_app(request)
        await app.start()
        yield app
        await app.teardown()

    @pytest_asyncio.fixture(scope="function")
    async def flet_app_function(request):
        """
        Function-scoped Flet app fixture.

        Binds and resets `ft.context.page` per test (host mode). In device mode
        the bound page is the tester session, not the on-device app page.
        """
        from flet.controls.context import _context_page, context

        app = _create_flet_app(request)
        await app.start()

        token = _context_page.set(app.page)
        context.reset_auto_update()

        try:
            yield app
        finally:
            _context_page.reset(token)
            context.disable_components_mode()
            await app.teardown()
