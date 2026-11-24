import asyncio

import flet as ft


def test_wait_idle_invokes_the_client_method_with_a_longer_transport_timeout(
    monkeypatch,
):
    calls = []

    async def fake_invoke(self, method_name, arguments=None, timeout=None):
        calls.append((method_name, arguments, timeout))
        return {"status": "idle", "error": None}

    monkeypatch.setattr(ft.FletApp, "_invoke_method", fake_invoke)
    app = ft.FletApp(url="")

    result = asyncio.run(app.wait_idle(idle_ms=250, timeout_ms=12000))

    assert result == {"status": "idle", "error": None}
    assert calls == [
        # The Dart side enforces timeout_ms itself; the transport timeout
        # must outlast it so a "timeout" result isn't lost to a TimeoutError.
        ("wait_idle", {"idle_ms": 250, "timeout_ms": 12000}, 17.0)
    ]
