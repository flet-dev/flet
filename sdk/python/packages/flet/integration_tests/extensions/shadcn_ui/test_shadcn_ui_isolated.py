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


@pytest.mark.asyncio(loop_scope="function")
async def test_badge_click(flet_app_function: ftt.FletTestApp):
    clicks = []
    flet_app_function.page.add(shad.Badge("Tag", on_click=lambda e: clicks.append(e)))
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Tag")
    )
    await flet_app_function.tester.pump_and_settle()

    assert len(clicks) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_icon_button_click(flet_app_function: ftt.FletTestApp):
    clicks = []
    flet_app_function.page.add(
        shad.IconButton(
            icon=shad.LucideIcons.ROCKET, on_click=lambda e: clicks.append(e)
        )
    )
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_icon(shad.LucideIcons.ROCKET)
    )
    await flet_app_function.tester.pump_and_settle()

    assert len(clicks) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_breadcrumb_item_click(flet_app_function: ftt.FletTestApp):
    clicks = []
    flet_app_function.page.add(
        shad.Breadcrumb(
            items=[
                shad.BreadcrumbItem("Home", on_click=lambda e: clicks.append(e)),
                shad.BreadcrumbItem("Current"),
            ]
        )
    )
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Home")
    )
    await flet_app_function.tester.pump_and_settle()

    assert len(clicks) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_indeterminate_progress_renders(flet_app_function: ftt.FletTestApp):
    # Indeterminate progress animates forever, so pump a fixed duration
    # instead of pump_and_settle.
    flet_app_function.page.add(shad.Progress(width=200), ft.Text("Loading"))
    await flet_app_function.tester.pump(duration=ft.Duration(milliseconds=500))

    finder = await flet_app_function.tester.find_by_text("Loading")
    assert finder.count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_avatar_falls_back_to_placeholder(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.add(
        shad.Avatar(src="https://invalid.flet.dev/missing.png", placeholder="FB")
    )
    for _ in range(10):
        await flet_app_function.tester.pump(duration=ft.Duration(milliseconds=300))

    finder = await flet_app_function.tester.find_by_text("FB")
    assert finder.count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_textarea_change(flet_app_function: ftt.FletTestApp):
    changes = []
    textarea = shad.Textarea(key="ta", on_change=lambda e: changes.append(e.data))
    flet_app_function.page.add(textarea)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.enter_text(
        await flet_app_function.tester.find_by_key("ta"), "hello"
    )
    await flet_app_function.tester.pump_and_settle()

    assert textarea.value == "hello"
    assert changes[-1] == "hello"


@pytest.mark.asyncio(loop_scope="function")
async def test_slider_drag_changes_value(flet_app_function: ftt.FletTestApp):
    ends = []
    slider = shad.Slider(
        key="s",
        width=200,
        value=0.5,
        on_change_end=lambda e: ends.append(e.data),
    )
    flet_app_function.page.add(slider)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.drag(
        await flet_app_function.tester.find_by_key("s"), ft.Offset(50, 0)
    )
    await flet_app_function.tester.pump_and_settle()

    assert slider.value > 0.5
    assert len(ends) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_radio_group_select_and_set(flet_app_function: ftt.FletTestApp):
    changes = []
    group = shad.RadioGroup(
        value="a",
        on_change=lambda e: changes.append(e.data),
        items=[shad.Radio(value="a", label="A"), shad.Radio(value="b", label="B")],
    )
    flet_app_function.page.add(group)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(await flet_app_function.tester.find_by_text("B"))
    await flet_app_function.tester.pump_and_settle()
    assert group.value == "b"
    assert changes == ["b"]

    # Setting the value from Python must not be reported back as a change.
    group.value = "a"
    group.update()
    await flet_app_function.tester.pump_and_settle()
    assert changes == ["b"]


@pytest.mark.asyncio(loop_scope="function")
async def test_select_choose_option(flet_app_function: ftt.FletTestApp):
    changes = []
    select = shad.Select(
        placeholder="Pick",
        on_change=lambda e: changes.append(e.data),
        options=[
            shad.SelectOption(value="x", text="Option X"),
            shad.SelectOption(value="y", text="Option Y"),
        ],
    )
    flet_app_function.page.add(select)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Pick")
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Option Y")
    )
    await flet_app_function.tester.pump_and_settle()

    assert select.value == "y"
    assert changes == ["y"]
    assert (await flet_app_function.tester.find_by_text("Option Y")).count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_input_otp_set_value(flet_app_function: ftt.FletTestApp):
    otp = shad.InputOTP(length=4)
    flet_app_function.page.add(otp)
    await flet_app_function.tester.pump_and_settle()

    otp.value = "4321"
    otp.update()
    await flet_app_function.tester.pump_and_settle()

    for digit in "4321":
        assert (await flet_app_function.tester.find_by_text(digit)).count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_tabs_switch(flet_app_function: ftt.FletTestApp):
    changes = []
    tabs = shad.Tabs(
        on_change=lambda e: changes.append(e.data),
        tabs=[
            shad.Tab(value="one", label="One", content=ft.Text("First content")),
            shad.Tab(value="two", label="Two", content=ft.Text("Second content")),
        ],
    )
    flet_app_function.page.add(tabs)
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("First content")).count == 1

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Two")
    )
    await flet_app_function.tester.pump_and_settle()

    assert tabs.value == "two"
    assert changes == ["two"]
    assert (await flet_app_function.tester.find_by_text("Second content")).count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_slider_in_intrinsic_width_column(flet_app_function: ftt.FletTestApp):
    # ShadSlider lays out with a LayoutBuilder, which throws on intrinsic size
    # queries; the wrapper must answer them instead.
    flet_app_function.page.add(
        ft.Column(
            intrinsic_width=True,
            controls=[ft.Text("Intrinsic slider"), shad.Slider(value=0.5)],
        )
    )
    await flet_app_function.tester.pump_and_settle()

    finder = await flet_app_function.tester.find_by_text("Intrinsic slider")
    assert finder.count == 1
