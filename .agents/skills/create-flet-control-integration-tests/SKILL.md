---
name: create-flet-control-integration-tests
description: Use when asked to create or update integration tests for any Flet control in sdk/python/packages/flet/integration_tests, including visual goldens and interactive behavior tests.
---

## When to use

Use this skill when adding, updating, or reviewing integration tests for a Flet control (core, material, cupertino, theme, services, types, or examples).

Use it for:

- visual rendering checks with golden screenshots
- interaction checks (hover, click, input, keyboard)
- control property behavior checks
- regression tests for control bugs

## Test placement

Pick the closest existing suite first:

- Core controls: `sdk/python/packages/flet/integration_tests/controls/core`
- Material controls: `sdk/python/packages/flet/integration_tests/controls/material`
- Cupertino controls: `sdk/python/packages/flet/integration_tests/controls/cupertino`
- Theme tests: `sdk/python/packages/flet/integration_tests/controls/theme`
- Type helpers: `sdk/python/packages/flet/integration_tests/controls/types`
- Services: `sdk/python/packages/flet/integration_tests/controls/services`
- Examples: `sdk/python/packages/flet/integration_tests/examples`

Prefer adding tests to an existing file for the same control. Create a new test file only when no suitable file exists.

### One file per control

Keep all tests for a control in `test_<control>.py`, whatever their scope. Module-scoped (`flet_app`) and function-scoped (`flet_app_function`) tests can share the file; pytest-asyncio runs each on its own event loop.

## Fixture choice

Use fixtures from `integration_tests/conftest.py`:

- `flet_app` (`loop_scope="module"`): the default. One app is shared by every module-scoped test in the file, so use it for tests that only add controls and check them, such as screenshot tests.
- `flet_app_function` (`loop_scope="function"`): launches a separate client for the test. That costs a few seconds per test with a prebuilt test app (`FLET_TEST_APP_BINARY`) and a full app build per test without one. Use it only when a test changes state that would leak into later tests, such as `page.theme_mode`, page-level properties, `ft.context.page` or auto-update behavior.

## Authoring workflow

1. Identify behavior to verify.
2. Build deterministic layout/state:
- set `theme_mode` explicitly when visuals matter
- set fixed sizes/padding/spacing
- avoid random or time-varying content
3. Choose the fixture: `flet_app` unless the test needs a fresh app.
4. Write test using async pytest.
5. Use screenshot assertion for UI behavior, functional assertion for non-visual behavior.
6. Name test so `request.node.name` can be used as screenshot key.
7. Run target test file.
8. If expected visuals changed, regenerate goldens with `FLET_TEST_GOLDEN=1` (or `FLET_TEST_GOLDEN=failed` to overwrite only mismatching ones) and re-run without golden mode.

## Assertion patterns

### Visual control assertion

```python
await flet_app.assert_control_screenshot(
    request.node.name,
    control,
)
```

### Visual full-page assertion

```python
flet_app_function.assert_screenshot(
    request.node.name,
    await flet_app_function.page.take_screenshot(
        pixel_ratio=flet_app_function.screenshots_pixel_ratio
    ),
)
```

### Functional assertion

```python
finder = await flet_app_function.tester.find_by_tooltip("Info tooltip")
assert finder.count == 1
```

## Minimal template

A `test_<control>.py` file with one test of each scope:

```python
import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_<behavior>(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(width=240, height=80, alignment=ft.Alignment.CENTER),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_<other_behavior>(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.add(ft.IconButton(icon=ft.Icons.INFO, tooltip="Info"))
    await flet_app_function.tester.pump_and_settle()

    finder = await flet_app_function.tester.find_by_tooltip("Info")
    assert finder.count == 1
```

## Run commands

Run one test file:

```bash
uv run pytest -s -o log_cli=true -o log_cli_level=INFO packages/flet/integration_tests/controls/core/test_control.py
```

Run a subset:

```bash
uv run pytest -s -o log_cli=true -o log_cli_level=INFO packages/flet/integration_tests/controls/core/test_control.py -k test_visible
```

Generate or update goldens:

```bash
FLET_TEST_GOLDEN=1 uv run pytest -s -o log_cli=true -o log_cli_level=INFO packages/flet/integration_tests/controls/core/test_control.py
```

## Quality checklist

- Test file location matches control area.
- All tests for a control are in one `test_<control>.py` file.
- `flet_app_function` is used only by tests that need a fresh app.
- Screenshot keys are stable (`request.node.name` preferred).
- Visual tests are deterministic (theme/size/content).
- Goldens are updated only for intentional visual changes.
- No unrelated formatting or refactors in the same change.

## References

- `sdk/python/packages/flet/integration_tests/README.md`
- `sdk/python/packages/flet/integration_tests/conftest.py`
- `sdk/python/packages/flet/integration_tests/controls/core/test_control.py`
- `sdk/python/packages/flet/integration_tests/controls/core/test_layout_control.py`
- `sdk/python/packages/flet/integration_tests/examples/core/test_control.py`
- `sdk/python/examples/controls/control`
