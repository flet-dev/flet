import flet.testing as ftt


async def test_increment(flet_app: ftt.FletTestApp):
    """Counter sample: tap the FAB and assert the counter goes 0 -> 1.

    The `flet_app` fixture is provided automatically by the flet pytest plugin.
    Run with `flet test` (or `uv run pytest`) from the project directory.
    """
    tester = flet_app.tester

    await tester.pump_and_settle()

    # Initial state
    assert (await tester.find_by_text("0")).count == 1

    # Tap the increment button (found by its key) and let the UI settle
    await tester.tap(await tester.find_by_key("increment"))
    await tester.pump_and_settle()

    # New state
    assert (await tester.find_by_text("1")).count == 1
