import os
import re

import flet.testing as ftt


async def test_counter(flet_app: ftt.FletTestApp):
    tester = flet_app.tester

    await tester.pump_and_settle()

    # The app displays the embedded Python version it was built against. CI pins
    # it per matrix leg (EXPECTED_PYTHON_VERSION, e.g. "3.14"); assert the app
    # reports that major.minor. Without the env var (e.g. a local run) just
    # assert some version is shown.
    expected = os.getenv("EXPECTED_PYTHON_VERSION")
    if expected:
        pattern = rf"Python {re.escape(expected)}\."
    else:
        pattern = r"Python \d+\.\d+\.\d+"
    assert (await tester.find_by_text_containing(pattern)).count == 1

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
