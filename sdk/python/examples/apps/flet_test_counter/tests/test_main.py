import asyncio

import flet.testing as ftt


async def _find_text_when_ready(tester, text: str, attempts: int = 40):
    """
    Pump-and-retry until a control with `text` appears.

    On a device the app runs embedded Python over dart_bridge; its cold start
    (interpreter init + `import flet` + running `main()`) can take several
    seconds on a slow emulator, so the first python-driven frame may land after
    the device driver's fixed warmup. `pump_and_settle` only settles Flutter
    frames — it can't know a python -> dart round-trip is still in flight — so
    poll rather than assert on the first frame.
    """
    finder = await tester.find_by_text(text)
    for _ in range(attempts):
        if finder.count >= 1:
            break
        await asyncio.sleep(0.25)
        await tester.pump_and_settle()
        finder = await tester.find_by_text(text)
    return finder


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
