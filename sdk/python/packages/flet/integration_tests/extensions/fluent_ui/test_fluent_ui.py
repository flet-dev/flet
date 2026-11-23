import flet_fluent_ui as fluent
import pytest

import flet as ft
import flet.testing as ftt


def _showcase() -> ft.Control:
    return ft.Column(
        intrinsic_width=True,
        controls=[
            ft.Row(
                [
                    fluent.FilledButton("Filled"),
                    fluent.Button("Default"),
                    fluent.IconButton(fluent.FluentIcons.SETTINGS),
                ]
            ),
            fluent.Checkbox(label="Checkbox", value=True),
            fluent.ToggleSwitch(label="Switch", value=True),
            fluent.ProgressBar(value=60, width=200),
        ],
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_fallback_theme_light(flet_app: ftt.FletTestApp, request):
    """Controls render without a `Theme` ancestor (default FluentTheme)."""
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name, _showcase(), bgcolor=ft.Colors.SURFACE
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_follows_page_dark_mode(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.DARK
    await flet_app.assert_control_screenshot(
        request.node.name, _showcase(), bgcolor=ft.Colors.SURFACE
    )
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app.page.update()


@pytest.mark.asyncio(loop_scope="module")
async def test_theme_accent_color_and_brightness(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                fluent.Theme(accent_color=ft.Colors.PURPLE, content=_showcase()),
                fluent.Theme(
                    accent_color=ft.Colors.ORANGE,
                    brightness=ft.Brightness.DARK,
                    content=ft.Container(
                        bgcolor="#202020", padding=8, content=_showcase()
                    ),
                ),
            ],
        ),
        bgcolor=ft.Colors.SURFACE,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_checkbox_tristate_cycle(flet_app: ftt.FletTestApp):
    changes = []
    checkbox = fluent.Checkbox(
        label="Tristate",
        tristate=True,
        value=False,
        on_change=lambda e: changes.append(e.control.value),
    )
    flet_app.page.controls = [checkbox]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    finder = await flet_app.tester.find_by_text("Tristate")
    for _ in range(3):
        await flet_app.tester.tap(finder)
        await flet_app.tester.pump_and_settle()

    assert changes == [True, None, False]
    assert checkbox.value is False


@pytest.mark.asyncio(loop_scope="module")
async def test_values_set_from_python(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    changes = []
    expander = fluent.Expander(
        header="Details",
        content=ft.Text("Hidden content"),
        on_change=lambda e: changes.append(e.control.expanded),
    )
    radios = fluent.RadioGroup(
        items=[
            fluent.RadioButton(value="a", label="Option A"),
            fluent.RadioButton(value="b", label="Option B"),
        ],
    )
    combo = fluent.ComboBox(
        placeholder="Pick",
        items=[
            fluent.ComboBoxItem(value="one", text="One"),
            fluent.ComboBoxItem(value="two", text="Two"),
        ],
    )
    flet_app.page.controls = [ft.Column(width=300, controls=[expander, radios, combo])]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        f"{request.node.name}_initial",
        await flet_app.take_page_controls_screenshot(bgcolor=ft.Colors.SURFACE),
    )

    expander.expanded = True
    radios.value = "b"
    combo.value = "two"
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    assert (await flet_app.tester.find_by_text("Two")).count == 1
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.take_page_controls_screenshot(bgcolor=ft.Colors.SURFACE),
    )
    # A value set from Python is not reported back as a change.
    assert changes == []

    # The user collapsing it is.
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Details"))
    await flet_app.tester.pump_and_settle()
    assert changes == [False]
    assert expander.expanded is False


@pytest.mark.asyncio(loop_scope="module")
async def test_text_box_enter_text(flet_app: ftt.FletTestApp):
    changes = []
    text_box = fluent.TextBox(
        key="tb", width=300, on_change=lambda e: changes.append(e.control.value)
    )
    flet_app.page.controls = [text_box]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.enter_text(await flet_app.tester.find_by_key("tb"), "Fluent")
    await flet_app.tester.pump_and_settle()

    assert text_box.value == "Fluent"
    assert changes[-1] == "Fluent"


@pytest.mark.asyncio(loop_scope="module")
async def test_combo_box_pick(flet_app: ftt.FletTestApp):
    combo = fluent.ComboBox(
        placeholder="Pick a fruit",
        items=[
            fluent.ComboBoxItem(value="apple", text="Apple"),
            fluent.ComboBoxItem(value="pear", text="Pear"),
        ],
    )
    flet_app.page.controls = [combo]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    await flet_app.tester.tap(await flet_app.tester.find_by_text("Pick a fruit"))
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Pear"))
    await flet_app.tester.pump_and_settle()

    assert combo.value == "pear"


@pytest.mark.asyncio(loop_scope="module")
async def test_content_dialog_open_and_close(flet_app: ftt.FletTestApp):
    dismissed = []
    dialog = fluent.ContentDialog(
        title="Dialog title",
        content="Dialog content",
        actions=[
            fluent.Button("Close", on_click=lambda e: flet_app.page.pop_dialog()),
        ],
        on_dismiss=lambda e: dismissed.append(True),
    )
    flet_app.page.controls = [ft.Text("Page")]
    flet_app.page.update()
    flet_app.page.show_dialog(dialog)
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Dialog content")).count == 1

    await flet_app.tester.tap(await flet_app.tester.find_by_text("Close"))
    await flet_app.tester.pump_and_settle()

    assert (await flet_app.tester.find_by_text("Dialog content")).count == 0
    assert dismissed == [True]
    assert dialog.open is False


@pytest.mark.asyncio(loop_scope="module")
async def test_fluent_icons(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            [
                ft.Icon(fluent.FluentIcons.HOME),
                ft.Icon(fluent.FluentIcons.MAIL, color=ft.Colors.BLUE),
                fluent.Button(
                    content=ft.Row(
                        tight=True,
                        controls=[ft.Icon(fluent.FluentIcons.SAVE), ft.Text("Save")],
                    )
                ),
            ]
        ),
        bgcolor=ft.Colors.SURFACE,
    )
