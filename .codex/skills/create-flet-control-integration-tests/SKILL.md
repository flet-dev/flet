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
- Example apps: `sdk/python/packages/flet/integration_tests/examples/apps`

Prefer adding tests to an existing file for the same control. Create a new `test_<control>.py` only when no suitable file exists.

## Fixture choice

Use fixtures from `integration_tests/conftest.py`:

- `flet_app` (`loop_scope="module"`): best for stable visual tests and bulk screenshot tests.
- `flet_app_function` (`loop_scope="function"`): best for isolated interactive tests and context-bound behavior.

## Authoring workflow

1. Identify behavior to verify.
2. Build deterministic layout/state:
- set `theme_mode` explicitly when visuals matter
- set fixed sizes/padding/spacing
- avoid random or time-varying content
3. Write test using async pytest.
4. Use screenshot assertion for UI behavior, functional assertion for non-visual behavior.
5. Name test so `request.node.name` can be used as screenshot key.
6. Run target test file.
7. If expected visuals changed, regenerate goldens with `FLET_TEST_GOLDEN=1` and re-run without golden mode.

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

## Minimal templates

### Template: golden visual test

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
```

### Template: interaction test

```python
import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_<behavior>(flet_app_function: ftt.FletTestApp):
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
- Fixture scope matches test intent.
- Screenshot keys are stable (`request.node.name` preferred).
- Visual tests are deterministic (theme/size/content).
- Goldens are updated only for intentional visual changes.
- No unrelated formatting or refactors in the same change.

## References

- `sdk/python/packages/flet/integration_tests/README.md`
- `sdk/python/packages/flet/integration_tests/conftest.py`
- `sdk/python/packages/flet/integration_tests/controls/core/test_control.py`
- `sdk/python/packages/flet/integration_tests/controls/core/test_layout_control.py`
- `sdk/python/packages/flet/integration_tests/controls/core/test_tooltip.py`
- `sdk/python/packages/flet/integration_tests/examples/apps/test_expand.py`
