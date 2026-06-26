import asyncio
import contextlib
import time

import flet.testing as ftt


async def _find_text_when_ready(tester, text: str, timeout: float = 60.0):
    """
    Pump-and-retry (up to `timeout` seconds) until a control with `text` appears.

    On a device the app runs embedded Python over dart_bridge; its cold start
    (interpreter init + `import flet` + running `main()`) can take tens of
    seconds on a slow CI emulator, so the first python-driven frame may land
    well after the device driver's fixed warmup. `pump_and_settle` only settles
    Flutter frames — it can't know a python -> dart round-trip is still in
    flight — so poll rather than assert on the first frame.
    """
    deadline = time.monotonic() + timeout
    while True:
        finder = await tester.find_by_text(text)
        if finder.count >= 1 or time.monotonic() >= deadline:
            return finder
        await asyncio.sleep(0.25)
        with contextlib.suppress(TimeoutError):
            await tester.pump_and_settle()


async def test_counter(flet_app: ftt.FletTestApp):
    tester = flet_app.tester

    # Initial state (wait for the app's first render).
    assert (await _find_text_when_ready(tester, "0")).count == 1

    # Increment once
    await tester.tap(await tester.find_by_key("increment"))
    assert (await _find_text_when_ready(tester, "1")).count == 1

    # Decrement twice -> -1
    await tester.tap(await tester.find_by_key("decrement"))
    await tester.tap(await tester.find_by_key("decrement"))
    assert (await _find_text_when_ready(tester, "-1")).count == 1
