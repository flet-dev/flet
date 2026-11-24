import asyncio
import importlib
import logging

import pytest

app = importlib.import_module("flet.app")


@pytest.mark.parametrize("entrypoint", ["run", "run_async"])
@pytest.mark.parametrize("level", ["info", "debug"])
@pytest.mark.parametrize("configured", [False, True])
@pytest.mark.parametrize("headless_linux", [False, True])
def test_startup_logging_respects_env_and_existing_setup(
    monkeypatch, entrypoint, level, configured, headless_linux
):
    root = logging.getLogger()
    handler = logging.NullHandler()
    monkeypatch.setattr(root, "handlers", [handler] if configured else [])
    monkeypatch.setattr(root, "level", logging.ERROR if configured else logging.WARNING)
    monkeypatch.setenv("FLET_LOG_LEVEL", level)
    monkeypatch.delenv("FLET_DART_BRIDGE_PORT", raising=False)
    monkeypatch.delenv("FLET_FORCE_WEB_SERVER", raising=False)
    monkeypatch.setattr(app, "is_pyodide", lambda: False)
    monkeypatch.setattr(app, "is_embedded", lambda: True)
    monkeypatch.setattr(app, "is_linux_server", lambda: headless_linux)

    class ServerStartup(Exception):
        pass

    async def start_server(**kwargs):
        raise ServerStartup

    monkeypatch.setattr(app, "__run_socket_server", start_server)
    # Headless Linux selects the web transport even in embedded mode.
    # Neither transport may start a real server in this logging test.
    monkeypatch.setattr(app, "__run_web_server", start_server)
    try:
        with pytest.raises(ServerStartup):
            if entrypoint == "run":
                app.run(lambda page: None)
            else:
                asyncio.run(app.run_async(lambda page: None))

        assert root.level == (
            logging.ERROR if configured else logging.getLevelName(level.upper())
        )
        assert len(root.handlers) == 1
        if configured:
            assert root.handlers == [handler]
    finally:
        for active_handler in root.handlers:
            active_handler.close()
