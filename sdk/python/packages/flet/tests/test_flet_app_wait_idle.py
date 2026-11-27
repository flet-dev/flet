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


def test_describe_and_act_invoke_the_client_methods(monkeypatch):
    calls = []

    async def fake_invoke(self, method_name, arguments=None, timeout=None):
        calls.append((method_name, arguments, timeout))
        return {"status": "ok"}

    monkeypatch.setattr(ft.FletApp, "_invoke_method", fake_invoke)
    app = ft.FletApp(url="")
    steps = [{"action": "tap", "target": {"text": "Add"}}]

    asyncio.run(app.describe(max_items=20))
    asyncio.run(app.act(steps, pointer="mouse", timeout_ms=4000))

    assert calls[0] == ("describe", {"max_items": 20}, None)
    assert calls[1] == (
        "act",
        {"steps": steps, "pointer": "mouse", "idle_ms": 500, "timeout_ms": 4000},
        34.0,
    )


def test_act_transport_allows_for_each_step_and_the_final_idle_wait(monkeypatch):
    async def transport_timeout(self, method_name, arguments=None, timeout=None):
        return timeout

    monkeypatch.setattr(ft.FletApp, "_invoke_method", transport_timeout)
    app = ft.FletApp(url="")
    waits = [{"action": "wait", "ms": 10_000}] * 4
    assert asyncio.run(app.act(waits)) > 4 * 10 + 5

    taps = [{"action": "long_press", "target": {"id": i}} for i in range(4)]
    # Three dependent targets can each take the full 20 seconds to appear.
    assert asyncio.run(app.act(taps, timeout_ms=20_000)) > 3 * 20 + 4 * 0.6 + 20
