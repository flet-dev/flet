import flet_shadcn_ui as shad
import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_renders_without_theme(flet_app_function: ftt.FletTestApp):
    # Guards the ShadTheme fallback: shadcn widgets throw without a ShadTheme
    # ancestor, and there is no Theme wrapper here.
    flet_app_function.page.add(shad.Button("No theme wrapper"))
    await flet_app_function.tester.pump_and_settle()

    finder = await flet_app_function.tester.find_by_text("No theme wrapper")
    assert finder.count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_button_click(flet_app_function: ftt.FletTestApp):
    clicks = []
    flet_app_function.page.add(
        shad.Button("Click me", on_click=lambda e: clicks.append(e))
    )
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Click me")
    )
    await flet_app_function.tester.pump_and_settle()

    assert len(clicks) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_disabled_button_does_not_click(flet_app_function: ftt.FletTestApp):
    clicks = []
    flet_app_function.page.add(
        shad.Button("Disabled", disabled=True, on_click=lambda e: clicks.append(e))
    )
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Disabled")
    )
    await flet_app_function.tester.pump_and_settle()

    assert clicks == []


@pytest.mark.asyncio(loop_scope="function")
async def test_input_change(flet_app_function: ftt.FletTestApp):
    changes = []
    input = shad.Input(
        key="input", placeholder="Type here", on_change=lambda e: changes.append(e)
    )
    flet_app_function.page.add(input)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.enter_text(
        await flet_app_function.tester.find_by_key("input"), "hello"
    )
    await flet_app_function.tester.pump_and_settle()

    assert input.value == "hello"
    assert changes and changes[-1].data == "hello"


@pytest.mark.asyncio(loop_scope="function")
async def test_input_value_from_python(flet_app_function: ftt.FletTestApp):
    input = shad.Input()
    flet_app_function.page.add(input)
    await flet_app_function.tester.pump_and_settle()

    input.value = "set from python"
    input.update()
    await flet_app_function.tester.pump_and_settle()

    finder = await flet_app_function.tester.find_by_text("set from python")
    assert finder.count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_checkbox_toggle(flet_app_function: ftt.FletTestApp):
    changes = []
    checkbox = shad.Checkbox(label="Toggle me", on_change=lambda e: changes.append(e))
    flet_app_function.page.add(checkbox)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Toggle me")
    )
    await flet_app_function.tester.pump_and_settle()

    assert checkbox.value is True
    assert len(changes) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_switch_toggle(flet_app_function: ftt.FletTestApp):
    changes = []
    switch = shad.Switch(label="Toggle me", on_change=lambda e: changes.append(e))
    flet_app_function.page.add(switch)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Toggle me")
    )
    await flet_app_function.tester.pump_and_settle()

    assert switch.value is True
    assert len(changes) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_lucide_icon_renders(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.add(ft.Icon(shad.LucideIcons.HOUSE))
    await flet_app_function.tester.pump_and_settle()

    finder = await flet_app_function.tester.find_by_icon(shad.LucideIcons.HOUSE)
    assert finder.count == 1
