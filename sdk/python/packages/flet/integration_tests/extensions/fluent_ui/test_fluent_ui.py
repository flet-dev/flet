from datetime import date, time

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
                        controls=[
                            ft.Icon(fluent.FluentIcons.SAVE),
                            ft.Text("Save"),
                        ],
                    )
                ),
            ]
        ),
        bgcolor=ft.Colors.SURFACE,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_picker_popup_follows_page_dark_mode(flet_app: ftt.FletTestApp, request):
    """A picker list opens on the app's navigator, above the controls, and
    still finds a Fluent theme matching the page."""
    flet_app.page.theme_mode = ft.ThemeMode.DARK
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(400, 480)
    flet_app.page.controls = [
        fluent.DatePicker(key="date", value=date(2025, 5, 14)),
    ]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.tap(await flet_app.tester.find_by_key("date"))
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
    # Close the list.
    await flet_app.tester.tap_at(ft.Offset(380, 460))
    await flet_app.tester.pump_and_settle()
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app.page.update()


def _local_dates(values) -> list[date]:
    return [v.astimezone().date() for v in values]


@pytest.mark.asyncio(loop_scope="module")
async def test_calendar_multiple_selection(flet_app: ftt.FletTestApp):
    changes = []
    calendar = fluent.CalendarView(
        width=300,
        selection_mode=fluent.CalendarSelectionMode.MULTIPLE,
        value=date(2025, 5, 13),
        on_change=lambda e: changes.append(e.selected_dates),
    )
    flet_app.page.controls = [calendar]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # Each click adds a date, including one before the first selected date:
    # reporting the selection to Python must not reset the calendar.
    for day in ["8", "21", "22"]:
        await flet_app.tester.tap(await flet_app.tester.find_by_text(day))
        await flet_app.tester.pump_and_settle()
    assert _local_dates(changes[-1]) == [
        date(2025, 5, 8),
        date(2025, 5, 13),
        date(2025, 5, 21),
        date(2025, 5, 22),
    ]
    assert len(changes) == 3
    assert calendar.value.astimezone().date() == date(2025, 5, 8)
    assert calendar.end_value.astimezone().date() == date(2025, 5, 22)

    # A date set from Python replaces the selection.
    calendar.value = date(2025, 5, 15)
    calendar.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.tap(await flet_app.tester.find_by_text("16"))
    await flet_app.tester.pump_and_settle()
    assert _local_dates(changes[-1]) == [
        date(2025, 5, 15),
        date(2025, 5, 16),
    ]


@pytest.mark.asyncio(loop_scope="module")
async def test_date_and_time_set_from_python(flet_app: ftt.FletTestApp):
    date_picker = fluent.DatePicker(value=date(2025, 5, 14))
    time_picker = fluent.TimePicker(value=time(7, 30))
    flet_app.page.controls = [date_picker, time_picker]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("May")).count == 1
    assert (await flet_app.tester.find_by_text("AM")).count == 1

    date_picker.value = date(2024, 2, 29)
    time_picker.value = time(15, 45)
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("February")).count == 1
    assert (await flet_app.tester.find_by_text("29")).count == 1
    assert (await flet_app.tester.find_by_text("2024")).count == 1
    assert (await flet_app.tester.find_by_text("45")).count == 1
    assert (await flet_app.tester.find_by_text("PM")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_flyout_open_close_and_dismiss(flet_app: ftt.FletTestApp):
    dismissed = []
    flyout = fluent.Flyout(
        content=ft.Text("Target"),
        flyout=ft.Text("Flyout content"),
        on_dismiss=lambda e: dismissed.append(True),
    )
    flet_app.page.controls = [flyout, ft.Text("Elsewhere")]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # Opened and closed from Python: no dismiss event.
    flyout.open = True
    flyout.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Flyout content")).count == 1
    flyout.open = False
    flyout.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Flyout content")).count == 0
    assert dismissed == []

    # Closed by the user: `open` is reset and the dismiss event fires, and
    # the flyout can be opened again.
    for _ in range(2):
        flyout.open = True
        flyout.update()
        await flet_app.tester.pump_and_settle()
        assert (await flet_app.tester.find_by_text("Flyout content")).count == 1
        await flet_app.tester.tap_at(ft.Offset(300, 300))
        await flet_app.tester.pump_and_settle()
        assert (await flet_app.tester.find_by_text("Flyout content")).count == 0
        assert flyout.open is False
    assert dismissed == [True, True]


@pytest.mark.asyncio(loop_scope="module")
async def test_flyout_uses_enclosing_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app.page.enable_screenshots = True
    flet_app.resize_page(320, 200)
    flet_app.page.controls = [
        fluent.Theme(
            brightness=ft.Brightness.DARK,
            accent_color=ft.Colors.PURPLE,
            content=fluent.Flyout(
                open=True,
                content=fluent.FilledButton("Target"),
                flyout=fluent.ToggleSwitch(label="Dark flyout", value=True),
            ),
        )
    ]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    flet_app.assert_screenshot(
        request.node.name,
        await flet_app.page.take_screenshot(
            pixel_ratio=flet_app.screenshots_pixel_ratio
        ),
    )
    await flet_app.tester.tap_at(ft.Offset(300, 180))
    await flet_app.tester.pump_and_settle()
    flet_app.page.enable_screenshots = False


@pytest.mark.asyncio(loop_scope="module")
async def test_menu_items_update_and_toggle(flet_app: ftt.FletTestApp):
    events = []
    toggle = fluent.ToggleMenuFlyoutItem(
        "Word wrap", on_change=lambda e: events.append(e.control.value)
    )
    item = fluent.MenuFlyoutItem("Old label")
    button = fluent.DropDownButton("Options", items=[item, toggle])
    flet_app.page.controls = [button]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # An item changed from Python shows its new label in the menu.
    item.content = "New label"
    item.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Options"))
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("New label")).count == 1

    await flet_app.tester.tap(await flet_app.tester.find_by_text("Word wrap"))
    await flet_app.tester.pump_and_settle()
    assert toggle.value is True
    assert events == [True]

    # Without items the button is disabled rather than failing.
    button.items = []
    button.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Options"))
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Word wrap")).count == 0


@pytest.mark.asyncio(loop_scope="module")
async def test_toggle_split_button(flet_app: ftt.FletTestApp):
    events = []
    button = fluent.SplitButton(
        "Bold",
        checked=False,
        items=[fluent.MenuFlyoutItem("Bold italic")],
        on_change=lambda e: events.append(e.control.checked),
    )
    flet_app.page.controls = [button]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    for _ in range(2):
        await flet_app.tester.tap(await flet_app.tester.find_by_text("Bold"))
        await flet_app.tester.pump_and_settle()
    assert events == [True, False]
    assert button.checked is False


@pytest.mark.asyncio(loop_scope="module")
async def test_tab_view_keeps_tab_state(flet_app: ftt.FletTestApp):
    # Earlier tests leave the window too small for the controls below.
    flet_app.resize_page(700, 420)
    tabs = fluent.TabView(
        height=200,
        tabs=[
            fluent.Tab("Notes", content=fluent.TextBox(key="notes")),
            fluent.Tab("Other", content=ft.Text("Other tab")),
        ],
    )
    flet_app.page.controls = [tabs]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.enter_text(
        await flet_app.tester.find_by_key("notes"), "Draft"
    )
    await flet_app.tester.pump_and_settle()

    # Adding a tab and renaming one keep the typed text of the first tab.
    tabs.tabs.append(fluent.Tab("New", content=ft.Text("New tab")))
    tabs.tabs[1].text = "Renamed"
    tabs.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Renamed")).count == 1
    assert (await flet_app.tester.find_by_text("Draft")).count == 1

    # Selecting from Python and by clicking.
    tabs.selected_index = 2
    tabs.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("New tab")).count == 1
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Notes"))
    await flet_app.tester.pump_and_settle()
    assert tabs.selected_index == 0
    assert (await flet_app.tester.find_by_text("Draft")).count == 1


@pytest.mark.asyncio(loop_scope="module")
async def test_tree_view_expand_and_select(flet_app: ftt.FletTestApp):
    expanded = []
    child = fluent.TreeViewItem("Child")
    parent = fluent.TreeViewItem(
        "Parent",
        items=[child],
        on_expand_change=lambda e: expanded.append(e.control.expanded),
    )
    tree = fluent.TreeView(
        width=240,
        selection_mode=fluent.TreeViewSelectionMode.SINGLE,
        items=[parent, fluent.TreeViewItem("Other")],
    )
    flet_app.page.controls = [tree]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Child")).count == 0

    # Expanded from Python, then selected by the user.
    parent.expanded = True
    parent.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Child"))
    await flet_app.tester.pump_and_settle()
    assert child.selected is True
    assert parent.selected is False

    # Selecting another item deselects the first one.
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Other"))
    await flet_app.tester.pump_and_settle()
    assert child.selected is False
    assert expanded == []


@pytest.mark.asyncio(loop_scope="module")
async def test_navigation_view_selection(flet_app: ftt.FletTestApp):
    changes = []
    view = fluent.NavigationView(
        height=300,
        display_mode=fluent.PaneDisplayMode.EXPANDED,
        selected_index=0,
        on_change=lambda e: changes.append(e.control.selected_index),
        items=[
            fluent.PaneItem("First", content=ft.Text("First page")),
            fluent.PaneItemHeader("Group"),
            fluent.PaneItem(
                "Expander",
                expanded=True,
                items=[fluent.PaneItem("Nested", content=ft.Text("Nested page"))],
            ),
        ],
        footer_items=[fluent.PaneItem("Last", content=ft.Text("Last page"))],
    )
    flet_app.page.controls = [view]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("First page")).count == 1

    # Pages are counted across expanders and footer items.
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Nested"))
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Nested page")).count == 1
    assert changes == [1]

    view.selected_index = 2
    view.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Last page")).count == 1

    # An index past the last page selects nothing rather than failing.
    view.selected_index = 5
    view.update()
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Last page")).count == 0


@pytest.mark.asyncio(loop_scope="module")
async def test_breadcrumb_click(flet_app: ftt.FletTestApp):
    clicked = []
    flet_app.page.controls = [
        fluent.BreadcrumbBar(
            items=[
                fluent.BreadcrumbItem(
                    name, on_click=lambda e: clicked.append(e.control.content)
                )
                for name in ["Home", "Music"]
            ]
        )
    ]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()
    await flet_app.tester.tap(await flet_app.tester.find_by_text("Home"))
    await flet_app.tester.pump_and_settle()
    assert clicked == ["Home"]


@pytest.mark.asyncio(loop_scope="module")
async def test_error_text(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=240,
            controls=[
                fluent.TextBox(value="jo", error_text="Enter at least 3 letters"),
                fluent.PasswordBox(value="abc", error_text="Too short"),
                fluent.NumberBox(value=120, error_text="Enter 1 to 100"),
                fluent.AutoSuggestBox(error_text="Pick a city from the list"),
                fluent.ComboBox(
                    placeholder="Country",
                    items=[fluent.ComboBoxItem("cz", text="Czechia")],
                    error_text="Required",
                ),
            ],
        ),
        bgcolor=ft.Colors.SURFACE,
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_error_text_keeps_focus(flet_app: ftt.FletTestApp):
    def validate(e):
        box.error_text = None if len(box.value) >= 3 else "Too short"

    box = fluent.TextBox(key="name", width=200, on_change=validate)
    flet_app.page.controls = [box]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    # The error appears and disappears while typing, without losing the
    # typed text or focus.
    finder = await flet_app.tester.find_by_key("name")
    await flet_app.tester.enter_text(finder, "ab")
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Too short")).count == 1
    await flet_app.tester.enter_text(finder, "abc")
    await flet_app.tester.pump_and_settle()
    assert (await flet_app.tester.find_by_text("Too short")).count == 0
    assert box.value == "abc"


@pytest.mark.asyncio(loop_scope="module")
async def test_radio_menu_items(flet_app: ftt.FletTestApp):
    small = fluent.RadioMenuFlyoutItem("Small", checked=True)
    large = fluent.RadioMenuFlyoutItem("Large")
    left = fluent.RadioMenuFlyoutItem("Left", group="align", checked=True)
    right = fluent.RadioMenuFlyoutItem("Right", group="align")
    flet_app.page.controls = [
        fluent.DropDownButton(
            "View",
            items=[small, large, fluent.MenuFlyoutSeparator(), left, right],
        )
    ]
    flet_app.page.update()
    await flet_app.tester.pump_and_settle()

    async def choose(text):
        await flet_app.tester.tap(await flet_app.tester.find_by_text("View"))
        await flet_app.tester.pump_and_settle()
        await flet_app.tester.tap(await flet_app.tester.find_by_text(text))
        await flet_app.tester.pump_and_settle()

    # Choosing an option unchecks the others of its group only.
    await choose("Large")
    assert (small.checked, large.checked) == (False, True)
    assert (left.checked, right.checked) == (True, False)
    await choose("Right")
    assert (small.checked, large.checked) == (False, True)
    assert (left.checked, right.checked) == (False, True)
