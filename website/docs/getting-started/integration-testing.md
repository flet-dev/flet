---
title: "Integration testing"
---

import TabItem from '@theme/TabItem';
import Tabs from '@theme/Tabs';

Flet lets you write **integration tests** for your app and run them with the
[`flet test`](../cli/flet-test.md) command. Tests drive your app the same way a
user would — finding controls by key or text, tapping buttons, entering text and
asserting the resulting UI — while the app runs **on the target device** exactly
as it ships: a built monolithic app with embedded Python.

Tests are written with [`pytest`](https://docs.pytest.org), so everything you
already know about pytest (fixtures, parametrization, markers, `-k` filtering)
just works.

:::note[Prerequisites]
`flet test` builds and runs your app the same way [`flet build`](../cli/flet-build.md)
does, so the [Flutter SDK and build prerequisites](../publish/index.md) must be
installed. The first run provisions a test host (and downloads the SDK if
needed), which is slow; subsequent runs are cached and fast.
:::

## Where tests live

Put your tests in a `tests/` directory at the **root of your app** — a sibling of
`src/`, not inside it (`src/` is what gets packaged into the on-device app; your
test code stays on the host and drives the app):

```
my_app/
├── pyproject.toml
├── src/
│   └── main.py          # your app
└── tests/
    └── test_main.py     # your tests
```

A new app created with [`flet create`](../cli/flet-create.md) already includes a
`tests/` folder with a sample test and the required pytest configuration in
`pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

## Enabling tests in an existing app

If your app wasn't created with `flet create`, enable testing by editing its
`pyproject.toml`.

**1. Add the test dependencies** to your development dependencies. The
`flet[test]` extra brings in `pytest`, `pytest-asyncio` and the
screenshot-comparison libraries:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```toml
[dependency-groups]
dev = [
    # ...your existing dev dependencies...
    "flet[test]",
]
```
</TabItem>
<TabItem value="pip" label="pip">
```toml
[project.optional-dependencies]
dev = [
    # ...your existing dev dependencies...
    "flet[test]",
]
```
</TabItem>
</Tabs>

**2. Configure pytest.** `asyncio_mode = "auto"` is **required** — it runs each
async test on the same event loop as the `flet_app` fixture:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

**3. Create a `tests/` directory** and add your first test (see
[Writing a test](#writing-a-test) below).

## Writing a test

Test functions are `async` and receive the [`flet_app`][flet.testing.FletTestApp]
fixture, which starts your app and exposes a [tester][flet.testing.Tester] to
drive it. Each test gets a **fresh app instance**, so tests are independent and
can run in any order.

Here is the counter sample (`tests/test_main.py`) that `flet create` generates:

```python title="tests/test_main.py"
import flet.testing as ftt


async def test_increment(flet_app: ftt.FletTestApp):
    tester = flet_app.tester

    await tester.pump_and_settle()

    # Initial state
    assert (await tester.find_by_text("0")).count == 1

    # Tap the increment button (found by its key) and let the UI update
    await tester.tap(await tester.find_by_key("increment"))
    await tester.pump_and_settle()

    # New state
    assert (await tester.find_by_text("1")).count == 1
```

The matching app gives the button a `key` so the test can find it reliably:

```python title="src/main.py"
import flet as ft


def main(page: ft.Page):
    counter = ft.Text("0", size=50, data=0)

    def increment_click(e):
        counter.data += 1
        counter.value = str(counter.data)

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD, key="increment", on_click=increment_click
    )
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Container(content=counter, alignment=ft.Alignment.CENTER),
        )
    )


ft.run(main)
```

:::tip
Give controls you want to test a stable [`key`](../cookbook/control-refs.md) and
find them with [`find_by_key()`][flet.testing.Tester.find_by_key]. It's more
robust than matching on text, which can change with localization or formatting.
:::

## The tester API

[`flet_app.tester`][flet.testing.FletTestApp.tester] finds controls and drives
interactions. **Finder** methods return a [`Finder`][flet.testing.Finder];
**action** methods take a `Finder`; and **pump** methods let the UI advance. All
methods are awaitable.

### Finding controls

| Method | Finds controls by |
| --- | --- |
| [`find_by_key(key)`][flet.testing.Tester.find_by_key] | their `key` |
| [`find_by_text(text)`][flet.testing.Tester.find_by_text] | exact text |
| [`find_by_text_containing(pattern)`][flet.testing.Tester.find_by_text_containing] | a regular-expression match on text |
| [`find_by_icon(icon)`][flet.testing.Tester.find_by_icon] | their icon (e.g. `ft.Icons.ADD`) |
| [`find_by_tooltip(value)`][flet.testing.Tester.find_by_tooltip] | tooltip text |

A [`Finder`][flet.testing.Finder] reports how many controls matched (via
[`count`][flet.testing.Finder.count]) and lets you pick one with
[`first`][flet.testing.Finder.first], [`last`][flet.testing.Finder.last] or
[`at()`][flet.testing.Finder.at]:

```python
finder = await tester.find_by_text("Item")
assert finder.count == 3          # number of matches
await tester.tap(finder.first)    # first match
await tester.tap(finder.last)     # last match
await tester.tap(finder.at(1))    # match at index 1
```

### Interacting

| Method | Action |
| --- | --- |
| [`tap(finder)`][flet.testing.Tester.tap] | tap a control |
| [`long_press(finder)`][flet.testing.Tester.long_press] | long-press a control |
| [`enter_text(finder, text)`][flet.testing.Tester.enter_text] | type text into a field |
| [`mouse_hover(finder)`][flet.testing.Tester.mouse_hover] | hover the mouse over a control |

### Pumping

The UI doesn't update instantly after an interaction. Call
[`pump_and_settle()`][flet.testing.Tester.pump_and_settle] to let the app process
events and render the result before asserting:

```python
await tester.tap(await tester.find_by_key("submit"))
await tester.pump_and_settle()
assert (await tester.find_by_text("Done")).count == 1
```

Use [`pump(duration=...)`][flet.testing.Tester.pump] to advance by a fixed amount
when you don't want to wait for everything to settle.

## Screenshot testing

On **Android and iOS** you can capture a full-screen screenshot of the running
app and compare it against a committed *golden* (reference) image — useful for
catching visual regressions. Full-screen capture is a device feature, so this is
**not available on desktop**.

[`tester.take_screenshot(name)`][flet.testing.Tester.take_screenshot] captures
the screen as PNG bytes, and
[`flet_app.assert_screenshot(name, bytes)`][flet.testing.FletTestApp.assert_screenshot]
compares them against the golden image, failing the test if they differ beyond a
similarity threshold (≈99% by default):

```python
async def test_home_screen(flet_app: ftt.FletTestApp):
    tester = flet_app.tester
    await tester.pump_and_settle()

    flet_app.assert_screenshot("home", await tester.take_screenshot("home"))
```

Golden images are **platform-specific** and stored next to your tests, under
`tests/golden/<platform>/<test_file>/<name>.png` — commit them to your repository.

To record the goldens the first time (or update them after an intentional UI
change), run with `-u` (`--update-goldens`). This writes the captured screenshots
as the new reference **instead of** comparing:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet test android --device-id emulator-5554 -u
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet test android --device-id emulator-5554 -u
```
</TabItem>
</Tabs>

:::tip
Render each screenshot on the same device/emulator you record its golden on —
different screen sizes and densities produce different pixels.
:::

## Running tests

### On desktop

From your app directory, run [`flet test`](../cli/flet-test.md). With no
arguments it targets the **current desktop** platform:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet test
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet test
```
</TabItem>
</Tabs>

### On a mobile emulator/simulator or device

First, make sure a device is running. Use
[`flet emulators`](../cli/flet-emulators.md) to list available emulators and
start one, then [`flet devices`](../cli/flet-devices.md) to get the id of a
running device:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet emulators              # list available emulators
uv run flet emulators start <id>   # start an emulator
uv run flet devices                # list running devices and their ids
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet emulators              # list available emulators
flet emulators start <id>   # start an emulator
flet devices                # list running devices and their ids
```
</TabItem>
</Tabs>

Then pass the platform as the first argument and the device id with
`--device-id` (`-d`):

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet test android --device-id emulator-5554
uv run flet test ios --device-id <simulator-id>
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet test android --device-id emulator-5554
flet test ios --device-id <simulator-id>
```
</TabItem>
</Tabs>

### Useful options

| Option | Description |
| --- | --- |
| `[platform]` | `macos`, `linux`, `windows`, `ios`, `android` (defaults to the current desktop) |
| `-d`, `--device-id` | Target device/emulator id (required for `ios`/`android`) |
| `-k <expr>` | Only run tests matching a pytest keyword expression |
| `--tests-dir <dir>` | Directory containing the tests (default: `tests`) |
| `-v` | Verbose — stream the underlying Flutter build/launch output |

### Running specific tests

Use `-k` to run only the tests matching a pytest keyword expression — handy while
iterating on a single test:

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run flet test -k test_screenshot
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
flet test -k test_screenshot
```
</TabItem>
</Tabs>

`-k` accepts the full pytest expression syntax, e.g. `-k screenshot`,
`-k "increment or screenshot"`, or `-k "not slow"`.

When [running with pytest directly](#running-with-pytest-directly) you can also
select a test by its node id:

```bash
uv run pytest tests/test_main.py::test_increment   # a single test
uv run pytest tests/test_main.py                   # one file
```

### Running with pytest directly

Because tests are plain pytest, you can also run them with `pytest`. The Flet
pytest plugin provisions the test host on demand, so this works without running
`flet test` first (it targets the current desktop platform):

<Tabs groupId="uv--pip">
<TabItem value="uv" label="uv">
```bash
uv run pytest
```
</TabItem>
<TabItem value="pip" label="pip">
```bash
pytest
```
</TabItem>
</Tabs>

To see the live build/launch output (and the app's `debugPrint`s) while running
under pytest, enable CLI logging at debug level:

```bash
uv run pytest -s -o log_cli=true -o log_cli_level=DEBUG
```

`pytest` has no options of its own for the device target or goldens, so the
`flet test` options map to environment variables:

| `flet test` option | Environment variable |
| --- | --- |
| `[platform]` | `FLET_TEST_PLATFORM` (e.g. `ios`, `android`) |
| `-d`, `--device-id` | `FLET_TEST_DEVICE` |
| `-u`, `--update-goldens` | `FLET_TEST_GOLDEN=1` |

```bash
# run on an iOS simulator and (re)record golden screenshots
FLET_TEST_PLATFORM=ios FLET_TEST_DEVICE=<simulator-id> FLET_TEST_GOLDEN=1 uv run pytest
```

When unset, `pytest` targets the current desktop platform and compares (rather
than records) screenshots.

:::note[How it works]
`flet test` provisions a Flutter test host from your app (the same pipeline as
`flet build`), embeds your Python code, and runs it on the device. The test code
runs on your computer and drives the on-device app over an independent channel —
so you're testing your app exactly as it ships, including the embedded Python
runtime, not a simulated approximation.
:::
