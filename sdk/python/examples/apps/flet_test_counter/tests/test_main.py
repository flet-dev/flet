import flet.testing as ftt


async def test_counter(flet_app: ftt.FletTestApp):
    tester = flet_app.tester

    await tester.pump_and_settle()

    # Initial state
    assert (await tester.find_by_text("0")).count == 1

    # Increment once
    await tester.tap(await tester.find_by_key("increment"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("1")).count == 1

    # Decrement twice -> -1
    await tester.tap(await tester.find_by_key("decrement"))
    await tester.tap(await tester.find_by_key("decrement"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("-1")).count == 1
