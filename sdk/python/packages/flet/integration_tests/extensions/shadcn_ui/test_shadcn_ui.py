import datetime

import flet_shadcn_ui as shad
import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_button_variants(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            [shad.Button(v.name.title(), variant=v) for v in shad.ButtonVariant],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_button_sizes(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row([shad.Button(s.name.title(), size=s) for s in shad.ButtonSize]),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_button_lucide_icons(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            [
                shad.Button("Mail", leading=shad.LucideIcons.MAIL),
                shad.Button(
                    "Next",
                    trailing=shad.LucideIcons.CHEVRON_RIGHT,
                    variant=shad.ButtonVariant.OUTLINE,
                ),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_card(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Card(
            width=320,
            title="Create project",
            description="Deploy your new project in one-click.",
            content=ft.Container(
                padding=ft.Padding.symmetric(vertical=16),
                content=shad.Input(placeholder="Name of your project"),
            ),
            footer=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    shad.Button("Cancel", variant=shad.ButtonVariant.OUTLINE),
                    shad.Button("Deploy"),
                ],
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_input(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=300,
            controls=[
                shad.Input(placeholder="Email", leading=shad.LucideIcons.MAIL),
                shad.Input(value="secret", password=True),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_checkbox(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                shad.Checkbox(label="Unchecked"),
                shad.Checkbox(label="Checked", sublabel="With a sublabel", value=True),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_switch(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                shad.Switch(label="Off"),
                shad.Switch(label="On", value=True),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_theme_violet_dark(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Theme(
            color_scheme=shad.ColorScheme.VIOLET,
            brightness=ft.Brightness.DARK,
            content=ft.Container(
                bgcolor="#020817",
                padding=16,
                content=ft.Row(
                    [
                        shad.Button("Primary"),
                        shad.Checkbox(label="Checked", value=True),
                        shad.Switch(value=True),
                    ]
                ),
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_follows_page_dark_mode(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.DARK
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Container(
            bgcolor=ft.Colors.SURFACE,
            padding=16,
            content=ft.Row([shad.Button("Primary"), shad.Switch(value=True)]),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_alert_variants(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=360,
            controls=[
                shad.Alert(
                    icon=shad.LucideIcons.TERMINAL,
                    title="Heads up!",
                    description="Primary alert.",
                ),
                shad.Alert(
                    icon=shad.LucideIcons.CIRCLE_ALERT,
                    title="Error",
                    description="Destructive alert.",
                    variant=shad.AlertVariant.DESTRUCTIVE,
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_avatar_placeholders(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            [
                shad.Avatar(placeholder="CN"),
                shad.Avatar(placeholder="JD", size=56, bgcolor=ft.Colors.AMBER_100),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_badge_variants(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row([shad.Badge(v.name.title(), variant=v) for v in shad.BadgeVariant]),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_breadcrumb(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Breadcrumb(
            items=[
                shad.BreadcrumbItem("Home", on_click=lambda e: None),
                shad.BreadcrumbEllipsis(),
                shad.BreadcrumbItem("Current"),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_icon_button_variants(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            [
                shad.IconButton(icon=shad.LucideIcons.ROCKET, variant=v)
                for v in shad.ButtonVariant
                if v != shad.ButtonVariant.LINK
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_progress_values(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=300,
            controls=[
                shad.Progress(value=0),
                shad.Progress(value=0.5),
                shad.Progress(value=1, color=ft.Colors.GREEN, bar_height=8),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_separators(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=240,
            spacing=0,
            controls=[
                ft.Text("Above"),
                shad.Separator(),
                ft.Text("Below"),
                shad.Separator(thickness=3, color=ft.Colors.RED, margin=4),
                ft.Row(
                    height=24,
                    controls=[
                        ft.Text("Left"),
                        shad.Separator(vertical=True),
                        ft.Text("Right"),
                    ],
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_textarea(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=300,
            controls=[
                shad.Textarea(placeholder="Placeholder", min_height=60),
                shad.Textarea(value="Line 1\nLine 2", resizable=False),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_slider(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=300,
            controls=[
                shad.Slider(value=0.25),
                shad.Slider(value=7, min=0, max=10, divisions=10),
                shad.Slider(
                    value=0.5,
                    active_track_color=ft.Colors.GREEN,
                    thumb_color=ft.Colors.GREEN_100,
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_radio_group(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.RadioGroup(
            value="b",
            horizontal=True,
            spacing=16,
            items=[
                shad.Radio(value="a", label="A"),
                shad.Radio(value="b", label="B"),
                shad.Radio(value="c", label="C", disabled=True),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_select(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            [
                shad.Select(
                    placeholder="Pick one",
                    options=[shad.SelectOption(value="x", text="X")],
                ),
                shad.Select(
                    value="x",
                    options=[shad.SelectOption(value="x", text="Chosen")],
                ),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_input_otp(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                shad.InputOTP(value="12", length=4),
                shad.InputOTP(value="123456", groups=[2, 2, 2], separator=ft.Text("-")),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_tabs(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Tabs(
            width=320,
            value="two",
            tabs=[
                shad.Tab(value="one", label="One", content=ft.Text("First")),
                shad.Tab(
                    value="two",
                    label="Two",
                    icon=shad.LucideIcons.STAR,
                    content=ft.Text("Second"),
                ),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_accordion_multiple(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Accordion(
            width=320,
            multiple=True,
            value=["one", "three"],
            items=[
                shad.AccordionItem(value=v, title=v.title(), content=ft.Text(v * 3))
                for v in ["one", "two", "three"]
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_resizable_vertical(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.ResizablePanelGroup(
            width=200,
            height=160,
            vertical=True,
            show_handle=True,
            divider_color=ft.Colors.RED,
            panels=[
                shad.ResizablePanel(default_size=0.25, content=ft.Text("Top")),
                shad.ResizablePanel(default_size=0.75, content=ft.Text("Bottom")),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_calendar_limits_two_months(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Calendar(
            value=datetime.date(2025, 6, 12),
            min_date=datetime.date(2025, 6, 5),
            max_date=datetime.date(2025, 7, 10),
            number_of_months=2,
            show_week_numbers=True,
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_time_picker_period(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                shad.TimePicker(value=datetime.time(0, 5), period=True),
                shad.TimePicker(
                    value=datetime.time(23, 59),
                    hour_label="H",
                    minute_label="M",
                ),
                shad.TimePicker(),
            ]
        ),
    )


def _table_rows(count: int) -> list[shad.TableRow]:
    return [
        shad.TableRow(cells=[shad.TableCell(f"Row {i}"), shad.TableCell(str(i * 10))])
        for i in range(1, count + 1)
    ]


@pytest.mark.asyncio(loop_scope="module")
async def test_table_scrolls_with_pinned_header(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Table(
            height=150,
            row_height=36,
            pinned_row_count=1,
            columns=[
                shad.TableColumn("Name", width=120),
                shad.TableColumn(
                    "Value", width=80, alignment=ft.Alignment.CENTER_RIGHT
                ),
            ],
            rows=_table_rows(10),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_table_without_header(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Table(
            columns=[shad.TableColumn(), shad.TableColumn()],
            rows=_table_rows(3),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_table_fill_column_in_middle(flet_app: ftt.FletTestApp, request):
    # A filling column must leave room for the fixed columns after it.
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        shad.Table(
            width=360,
            columns=[
                shad.TableColumn("Left", width=80),
                shad.TableColumn("Middle fills", fill=True),
                shad.TableColumn(
                    "Right", width=80, alignment=ft.Alignment.CENTER_RIGHT
                ),
            ],
            rows=[
                shad.TableRow(
                    cells=[
                        shad.TableCell("a"),
                        shad.TableCell("b"),
                        shad.TableCell("c"),
                    ]
                )
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_field_errors(flet_app: ftt.FletTestApp, request):
    # Every value control with a label, description and error. The fixed
    # width keeps button-like fields (Select, DatePicker) at full width.
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            width=300,
            spacing=12,
            controls=[
                shad.Input(
                    label="Input",
                    description="Description",
                    error_text="Input error",
                ),
                shad.Textarea(label="Textarea", error_text="Textarea error"),
                shad.Select(
                    width=300,
                    label="Select",
                    placeholder="Pick one",
                    error_text="Select error",
                    options=[shad.SelectOption(value="a", text="A")],
                ),
                shad.InputOTP(length=4, label="InputOTP", error_text="OTP error"),
                shad.DatePicker(width=300, label="DatePicker", error_text="Date error"),
                shad.TimePicker(label="TimePicker", error_text="Time error"),
                shad.RadioGroup(
                    label="RadioGroup",
                    error_text="Radio error",
                    items=[shad.Radio(value="a", label="A")],
                ),
                shad.Checkbox(label="Checkbox", error_text="Checkbox error"),
                shad.Switch(label="Switch", error_text="Switch error"),
            ],
        ),
    )
