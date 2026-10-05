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


@pytest.mark.asyncio(loop_scope="function")
async def test_accordion_expand_and_set(flet_app_function: ftt.FletTestApp):
    changes = []
    accordion = shad.Accordion(
        on_change=lambda e: changes.append(e.data),
        items=[
            shad.AccordionItem(value="a", title="Item A", content=ft.Text("Body A")),
            shad.AccordionItem(value="b", title="Item B", content=ft.Text("Body B")),
        ],
    )
    flet_app_function.page.add(accordion)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Item B")
    )
    await flet_app_function.tester.pump_and_settle()
    assert accordion.value == ["b"]
    assert changes == [["b"]]
    assert (await flet_app_function.tester.find_by_text("Body B")).count == 1

    # Setting the value from Python must not be reported back as a change.
    accordion.value = ["a"]
    accordion.update()
    await flet_app_function.tester.pump_and_settle()
    assert changes == [["b"]]
    assert (await flet_app_function.tester.find_by_text("Body A")).count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_popover_open_and_dismiss(flet_app_function: ftt.FletTestApp):
    dismissed = []
    flet_app_function.resize_page(400, 300)
    popover = shad.Popover(
        on_dismiss=lambda e: dismissed.append(e),
        content=ft.Text("Anchor"),
        popover=ft.Text("Popover body"),
    )
    flet_app_function.page.add(popover)
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Popover body")).count == 0

    popover.open = True
    popover.update()
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Popover body")).count == 1
    assert dismissed == []

    await flet_app_function.tester.tap_at(ft.Offset(380, 280))
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Popover body")).count == 0
    assert popover.open is False
    assert len(dismissed) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_tooltip_shows_on_hover(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.add(
        shad.Tooltip(message="Tip text", content=ft.Text("Target"))
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Tip text")).count == 0

    await flet_app_function.tester.mouse_hover(
        await flet_app_function.tester.find_by_text("Target")
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Tip text")).count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_resizable_in_intrinsic_width_column(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.add(
        ft.Column(
            intrinsic_width=True,
            controls=[
                ft.Text("Intrinsic resizable"),
                shad.ResizablePanelGroup(
                    width=200,
                    height=80,
                    panels=[
                        shad.ResizablePanel(default_size=0.5, content=ft.Text("L")),
                        shad.ResizablePanel(default_size=0.5, content=ft.Text("R")),
                    ],
                ),
            ],
        )
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("R")).count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_calendar_pick_and_clear(flet_app_function: ftt.FletTestApp):
    import datetime

    changes = []
    calendar = shad.Calendar(
        value=datetime.date(2025, 6, 12), on_change=lambda e: changes.append(e)
    )
    flet_app_function.page.add(calendar)
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("20")
    )
    await flet_app_function.tester.pump_and_settle()
    assert len(changes) == 1
    # A picked day arrives as midnight UTC of that day.
    assert calendar.value.date() == datetime.date(2025, 6, 20)
    assert calendar.value.utcoffset() == datetime.timedelta(0)

    # Clearing from Python must deselect the day without reporting a change.
    calendar.value = None
    calendar.update()
    await flet_app_function.tester.pump_and_settle()
    assert len(changes) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_calendar_min_max_date(flet_app_function: ftt.FletTestApp):
    import datetime

    changes = []
    calendar = shad.Calendar(
        value=datetime.date(2025, 6, 12),
        min_date=datetime.date(2025, 6, 10),
        max_date=datetime.date(2025, 6, 15),
        on_change=lambda e: changes.append(e),
    )
    flet_app_function.page.add(calendar)
    await flet_app_function.tester.pump_and_settle()

    # The 20th is outside the allowed range, so tapping it does nothing.
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("20")
    )
    await flet_app_function.tester.pump_and_settle()
    assert changes == []
    assert calendar.value == datetime.date(2025, 6, 12)


@pytest.mark.asyncio(loop_scope="function")
async def test_time_picker_set_from_python(flet_app_function: ftt.FletTestApp):
    import datetime

    changes = []
    picker = shad.TimePicker(
        value=datetime.time(9, 5), on_change=lambda e: changes.append(e)
    )
    flet_app_function.page.add(picker)
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("09")).count == 1
    assert (await flet_app_function.tester.find_by_text("05")).count == 1

    picker.value = datetime.time(17, 45)
    picker.update()
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("17")).count == 1
    assert (await flet_app_function.tester.find_by_text("45")).count == 1
    assert changes == []


@pytest.mark.asyncio(loop_scope="function")
async def test_pickers_in_intrinsic_width_column(flet_app_function: ftt.FletTestApp):
    # ShadCalendar and ShadTimePicker can't compute a dry layout; the wrapper
    # must answer intrinsic queries (e.g. inside AlertDialog content) instead.
    import datetime

    flet_app_function.page.add(
        ft.Column(
            intrinsic_width=True,
            controls=[
                ft.Text("Intrinsic pickers"),
                shad.Calendar(value=datetime.date(2025, 6, 12)),
                shad.TimePicker(value=datetime.time(8, 15)),
            ],
        )
    )
    await flet_app_function.tester.pump_and_settle()

    assert (await flet_app_function.tester.find_by_text("Intrinsic pickers")).count == 1
    assert (await flet_app_function.tester.find_by_text("08")).count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_date_range_picker_new_range(flet_app_function: ftt.FletTestApp):
    import datetime

    flet_app_function.resize_page(700, 500)
    picker = shad.DateRangePicker(
        key="range",
        start_value=datetime.date(2025, 6, 9),
        end_value=datetime.date(2025, 6, 13),
    )
    flet_app_function.page.add(picker)
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_key("range")
    )
    await flet_app_function.tester.pump_and_settle()

    # A click after a complete range starts a new one...
    await flet_app_function.tester.tap(
        (await flet_app_function.tester.find_by_text("16")).first
    )
    await flet_app_function.tester.pump_and_settle()
    assert picker.start_value.date() == datetime.date(2025, 6, 16)
    assert picker.end_value is None

    # ...a click before the start moves the start...
    await flet_app_function.tester.tap(
        (await flet_app_function.tester.find_by_text("11")).first
    )
    await flet_app_function.tester.pump_and_settle()
    assert picker.start_value.date() == datetime.date(2025, 6, 11)
    assert picker.end_value is None

    # ...and a click after the start sets the end.
    await flet_app_function.tester.tap(
        (await flet_app_function.tester.find_by_text("20")).first
    )
    await flet_app_function.tester.pump_and_settle()
    assert picker.start_value.date() == datetime.date(2025, 6, 11)
    assert picker.end_value.date() == datetime.date(2025, 6, 20)


@pytest.mark.asyncio(loop_scope="function")
async def test_context_menu_click_and_disabled(flet_app_function: ftt.FletTestApp):
    clicks = []
    flet_app_function.resize_page(500, 400)
    flet_app_function.page.add(
        shad.ContextMenu(
            content=ft.Container(
                key="area", width=200, height=100, content=ft.Text("Area")
            ),
            items=[
                shad.MenuItem("Enabled", on_click=lambda e: clicks.append("enabled")),
                shad.MenuItem(
                    "Off", disabled=True, on_click=lambda e: clicks.append("off")
                ),
            ],
        )
    )
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.right_mouse_click(
        await flet_app_function.tester.find_by_key("area")
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Off")
    )
    await flet_app_function.tester.pump_and_settle()
    assert clicks == []

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Enabled")
    )
    await flet_app_function.tester.pump_and_settle()
    assert clicks == ["enabled"]
    assert (await flet_app_function.tester.find_by_text("Enabled")).count == 0


@pytest.mark.asyncio(loop_scope="function")
async def test_menubar_submenu_click(flet_app_function: ftt.FletTestApp):
    clicks = []
    flet_app_function.resize_page(500, 400)
    flet_app_function.page.add(
        shad.Menubar(
            items=[
                shad.MenubarItem(
                    "Menu",
                    items=[
                        shad.MenuItem(
                            "Sub",
                            items=[
                                shad.MenuItem(
                                    "Deep", on_click=lambda e: clicks.append("deep")
                                )
                            ],
                        )
                    ],
                )
            ]
        )
    )
    await flet_app_function.tester.pump_and_settle()

    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Menu")
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.mouse_hover(
        await flet_app_function.tester.find_by_text("Sub")
    )
    await flet_app_function.tester.pump_and_settle()
    await flet_app_function.tester.tap(
        await flet_app_function.tester.find_by_text("Deep")
    )
    await flet_app_function.tester.pump_and_settle()
    assert clicks == ["deep"]


@pytest.mark.asyncio(loop_scope="function")
async def test_context_menu_open_on_tap_and_long_press(
    flet_app_function: ftt.FletTestApp,
):
    # Tests run on desktop, where only right-click opens the menu by default.
    flet_app_function.resize_page(600, 400)

    def menu(key: str, **kwargs) -> shad.ContextMenu:
        return shad.ContextMenu(
            content=ft.Container(key=key, width=150, height=60, content=ft.Text(key)),
            items=[shad.MenuItem(f"{key} item")],
            **kwargs,
        )

    flet_app_function.page.add(
        ft.Row(
            [
                menu("default"),
                menu("tap", open_on_tap=True),
                menu("long", open_on_long_press=True),
            ]
        )
    )
    await flet_app_function.tester.pump_and_settle()
    tester = flet_app_function.tester

    await tester.tap(await tester.find_by_key("default"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("default item")).count == 0

    await tester.tap(await tester.find_by_key("tap"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("tap item")).count == 1

    # Tapping outside closes it.
    await tester.tap_at(ft.Offset(580, 380))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("tap item")).count == 0

    await tester.long_press(await tester.find_by_key("long"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("long item")).count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_table_row_click_index(flet_app_function: ftt.FletTestApp):
    clicks = []
    flet_app_function.page.add(
        shad.Table(
            on_row_click=lambda e: clicks.append(e.data),
            columns=[shad.TableColumn("Header A"), shad.TableColumn("Header B")],
            rows=[
                shad.TableRow(cells=[shad.TableCell("r0"), shad.TableCell("x")]),
                shad.TableRow(cells=[shad.TableCell("r1"), shad.TableCell("y")]),
            ],
            footer=[shad.TableCell("Footer"), shad.TableCell("")],
        )
    )
    await flet_app_function.tester.pump_and_settle()
    tester = flet_app_function.tester

    for text in ["Header A", "r1", "r0", "Footer"]:
        await tester.tap(await tester.find_by_text(text))
        await tester.pump_and_settle()

    # Header and footer clicks are ignored; data rows report their index.
    assert clicks == [1, 0]


@pytest.mark.asyncio(loop_scope="function")
async def test_table_in_intrinsic_width_column(flet_app_function: ftt.FletTestApp):
    flet_app_function.page.add(
        ft.Column(
            intrinsic_width=True,
            controls=[
                ft.Text("Intrinsic table"),
                shad.Table(
                    columns=[shad.TableColumn("A"), shad.TableColumn("B", fill=True)],
                    rows=[
                        shad.TableRow(cells=[shad.TableCell("1"), shad.TableCell("2")])
                    ],
                ),
            ],
        )
    )
    await flet_app_function.tester.pump_and_settle()
    assert (await flet_app_function.tester.find_by_text("Intrinsic table")).count == 1
    assert (await flet_app_function.tester.find_by_text("2")).count == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_dialog_show_pop_and_modal(flet_app_function: ftt.FletTestApp):
    page = flet_app_function.page
    tester = flet_app_function.tester
    page.window.width = 600
    page.window.height = 500
    dismissed = []
    dialog = shad.Dialog(
        title="Dialog title",
        content=ft.Text("Dialog body"),
        on_dismiss=lambda e: dismissed.append("dialog"),
    )
    page.add(ft.Text("Page"))
    await tester.pump_and_settle()

    page.show_dialog(dialog)
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Dialog body")).count == 1

    page.pop_dialog()
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Dialog body")).count == 0
    assert dismissed == ["dialog"]
    assert dialog.open is False

    # A non-modal dialog closes when the barrier is tapped...
    page.show_dialog(dialog)
    await tester.pump_and_settle()
    await tester.tap_at(ft.Offset(10, 10))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Dialog body")).count == 0
    assert dismissed == ["dialog", "dialog"]

    # ...a modal one does not.
    modal = shad.Dialog(title="Modal", content=ft.Text("Modal body"), modal=True)
    page.show_dialog(modal)
    await tester.pump_and_settle()
    await tester.tap_at(ft.Offset(10, 10))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Modal body")).count == 1
    page.pop_dialog()
    await tester.pump_and_settle()


@pytest.mark.asyncio(loop_scope="function")
async def test_sheet_show_and_close(flet_app_function: ftt.FletTestApp):
    page = flet_app_function.page
    tester = flet_app_function.tester
    dismissed = []
    sheet = shad.Sheet(
        side=shad.SheetSide.RIGHT,
        title="Sheet title",
        content=ft.Text("Sheet body"),
        on_dismiss=lambda e: dismissed.append(e),
    )
    page.add(ft.Text("Page"))
    await tester.pump_and_settle()

    page.show_dialog(sheet)
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Sheet body")).count == 1

    sheet.open = False
    sheet.update()
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Sheet body")).count == 0
    assert len(dismissed) == 1


@pytest.mark.asyncio(loop_scope="function")
async def test_toast_timeout_close_and_replace(flet_app_function: ftt.FletTestApp):
    import asyncio

    page = flet_app_function.page
    tester = flet_app_function.tester
    dismissed = []

    def toast(name: str, seconds: float) -> shad.Toast:
        return shad.Toast(
            title=name,
            duration=ft.Duration(milliseconds=int(seconds * 1000)),
            on_dismiss=lambda e: dismissed.append(name),
        )

    page.add(ft.Text("Page"))
    await tester.pump_and_settle()

    # Times out.
    page.show_dialog(toast("Short", 1))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("Short")).count == 1
    await asyncio.sleep(1.5)
    await tester.pump_and_settle()
    assert dismissed == ["Short"]
    assert (await tester.find_by_text("Short")).count == 0

    # Closed with the close button.
    page.show_dialog(toast("Closable", 30))
    await tester.pump_and_settle()
    await tester.tap(await tester.find_by_icon(shad.LucideIcons.X))
    await tester.pump_and_settle()
    assert dismissed == ["Short", "Closable"]

    # Replaced by a newer toast.
    page.show_dialog(toast("First", 30))
    await tester.pump_and_settle()
    page.show_dialog(toast("Second", 30))
    await tester.pump_and_settle()
    assert dismissed == ["Short", "Closable", "First"]
    assert (await tester.find_by_text("Second")).count == 1
    page.pop_dialog()
    await tester.pump_and_settle()


@pytest.mark.asyncio(loop_scope="function")
async def test_sonner_stacks_and_closes_one(flet_app_function: ftt.FletTestApp):
    page = flet_app_function.page
    tester = flet_app_function.tester
    dismissed = []

    def sonner(name: str) -> shad.Sonner:
        return shad.Sonner(
            title=name,
            duration=ft.Duration(seconds=30),
            on_dismiss=lambda e: dismissed.append(name),
        )

    page.add(ft.Text("Page"))
    await tester.pump_and_settle()
    first = sonner("One")
    page.show_dialog(first)
    await tester.pump_and_settle()
    page.show_dialog(sonner("Two"))
    await tester.pump_and_settle()
    assert (await tester.find_by_text("One")).count == 1
    assert (await tester.find_by_text("Two")).count == 1
    assert dismissed == []

    first.open = False
    first.update()
    await tester.pump_and_settle()
    assert dismissed == ["One"]
    assert (await tester.find_by_text("Two")).count == 1
