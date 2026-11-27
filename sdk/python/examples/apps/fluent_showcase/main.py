import datetime

import flet_fluent_ui as fluent

import flet as ft

ACCENTS = [
    ("Blue", "#0078D4"),
    ("Purple", "#8764B8"),
    ("Green", "#107C10"),
    ("Orange", "#CA5010"),
    ("Red", "#D13438"),
    ("Teal", "#038387"),
]

ACTIVITY = [
    (
        fluent.FluentIcons.DOCUMENT_TEXT,
        "Q4 report.docx",
        "Edited by Sofia Davis, 5 min ago",
    ),
    (fluent.FluentIcons.PERSON_ADD, "Jackson Lee joined", "Developer, 1 hour ago"),
    (
        fluent.FluentIcons.ARROW_UPLOAD,
        "Release 1.1 published",
        "Build 2026.11.4, today",
    ),
    (fluent.FluentIcons.CHAT, "3 new comments", 'On "Launch plan", yesterday'),
]


def muted(value: str, size: float = 13) -> ft.Text:
    return ft.Text(value, size=size, color=ft.Colors.ON_SURFACE_VARIANT)


def title(value: str) -> ft.Text:
    return ft.Text(value, size=16, weight=ft.FontWeight.W_600)


def card(*controls: ft.Control, spacing: float = 12) -> fluent.Card:
    return fluent.Card(
        padding=16,
        border_radius=8,
        content=ft.Column(spacing=spacing, controls=list(controls)),
    )


def stat_card(label: str, value: str, change: str, icon: ft.IconData) -> fluent.Card:
    return fluent.Card(
        col={"xs": 12, "sm": 6, "lg": 3},
        padding=16,
        border_radius=8,
        content=ft.Row(
            spacing=14,
            controls=[
                ft.Container(
                    width=40,
                    height=40,
                    border_radius=20,
                    bgcolor=ft.Colors.with_opacity(0.08, ft.Colors.ON_SURFACE),
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(icon, size=20),
                ),
                ft.Column(
                    spacing=0,
                    controls=[
                        muted(label),
                        ft.Text(value, size=22, weight=ft.FontWeight.W_600),
                        muted(change, size=12),
                    ],
                ),
            ],
        ),
    )


def new_project_card() -> fluent.Card:
    return card(
        title("New project"),
        fluent.InfoLabel("Name", content=fluent.TextBox(value="flet-dashboard")),
        fluent.InfoLabel(
            "Template",
            content=fluent.ComboBox(
                value="dashboard",
                expand_to_fit=True,
                items=[
                    fluent.ComboBoxItem(value="dashboard", text="Dashboard"),
                    fluent.ComboBoxItem(value="blank", text="Blank app"),
                    fluent.ComboBoxItem(value="chat", text="Chat"),
                ],
            ),
        ),
        fluent.InfoLabel(
            "Access token", content=fluent.PasswordBox(value="secret-token")
        ),
        fluent.ToggleSwitch(label="Deploy on push", value=True),
        fluent.Checkbox(label="Create a README", value=True),
        ft.Row(
            alignment=ft.MainAxisAlignment.END,
            controls=[
                fluent.Button("Cancel"),
                fluent.FilledButton("Create"),
            ],
        ),
    )


def team_card() -> fluent.Card:
    return card(
        title("Team"),
        *[
            fluent.ListTile(
                leading=ft.CircleAvatar(
                    content=ft.Text(initials, size=12),
                    radius=16,
                ),
                title=name,
                subtitle=role,
                trailing=badge,
            )
            for initials, name, role, badge in [
                ("SD", "Sofia Davis", "Owner", None),
                ("JL", "Jackson Lee", "Developer", fluent.InfoBadge("New")),
                ("IN", "Isabella Nguyen", "Billing", None),
            ]
        ],
        spacing=4,
    )


def calendar_card() -> fluent.Card:
    return fluent.Card(
        padding=8,
        border_radius=8,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                fluent.CalendarView(
                    width=300,
                    value=datetime.date(2026, 11, 4),
                    highlight_today=False,
                )
            ],
        ),
    )


def storage_card() -> fluent.Card:
    return card(
        title("Storage"),
        ft.Row(
            spacing=16,
            controls=[
                fluent.ProgressRing(value=68, width=56, height=56, stroke_width=6),
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text("68 GB of 100 GB used", weight=ft.FontWeight.W_500),
                        muted("Photos take up most space"),
                    ],
                ),
            ],
        ),
        fluent.ProgressBar(value=40),
        muted("Syncing 124 of 310 files"),
    )


def activity_card() -> fluent.Card:
    return card(
        title("Recent activity"),
        *[
            fluent.ListTile(leading=icon, title=name, subtitle=detail)
            for icon, name, detail in ACTIVITY
        ],
        spacing=4,
    )


def settings_card() -> fluent.Card:
    return card(
        title("Notifications"),
        fluent.ToggleSwitch(label="Push notifications", value=True),
        fluent.ToggleSwitch(label="Product updates"),
        fluent.InfoLabel(
            "Daily summary at",
            content=fluent.NumberBox(value=9, min=0, max=23),
        ),
        fluent.Expander(
            header="Quiet hours",
            content=muted("No notifications from 22:00 to 07:00."),
        ),
    )


def dashboard(page: ft.Page, theme: fluent.Theme) -> fluent.ScaffoldPage:
    def change_accent(e: ft.Event[fluent.ComboBox]):
        theme.accent_color = e.control.value

    def toggle_theme_mode():
        dark = page.theme_mode == ft.ThemeMode.DARK
        page.theme_mode = ft.ThemeMode.LIGHT if dark else ft.ThemeMode.DARK
        mode_button.icon = (
            fluent.FluentIcons.WEATHER_MOON
            if dark
            else fluent.FluentIcons.WEATHER_SUNNY
        )

    mode_button = fluent.IconButton(
        icon=fluent.FluentIcons.WEATHER_MOON, on_click=toggle_theme_mode
    )

    header = fluent.PageHeader(
        title="Overview",
        command_bar=ft.Row(
            spacing=8,
            tight=True,
            controls=[
                fluent.TextBox(
                    placeholder="Search",
                    width=200,
                    suffix=fluent.FluentIcons.SEARCH,
                ),
                fluent.ComboBox(
                    value=ACCENTS[0][1],
                    items=[
                        fluent.ComboBoxItem(value=color, text=name)
                        for name, color in ACCENTS
                    ],
                    on_change=change_accent,
                ),
                mode_button,
                fluent.FilledButton(
                    ft.Row(
                        spacing=8,
                        tight=True,
                        controls=[
                            ft.Icon(fluent.FluentIcons.ADD, size=16),
                            ft.Text("New report"),
                        ],
                    )
                ),
            ],
        ),
    )

    def column(*cards: ft.Control) -> ft.Column:
        return ft.Column(
            col={"xs": 12, "md": 6, "lg": 4}, spacing=16, controls=list(cards)
        )

    return fluent.ScaffoldPage(
        header=header,
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=16,
            controls=[
                fluent.InfoBar(
                    title="Backup complete",
                    content="All 310 files were backed up to the cloud.",
                    severity=fluent.InfoBarSeverity.SUCCESS,
                    on_close=lambda e: None,
                ),
                ft.ResponsiveRow(
                    spacing=16,
                    run_spacing=16,
                    controls=[
                        stat_card(
                            "Revenue",
                            "$45,231",
                            "+20.1% from last month",
                            fluent.FluentIcons.MONEY,
                        ),
                        stat_card(
                            "Subscriptions",
                            "2,350",
                            "+180 this week",
                            fluent.FluentIcons.PEOPLE,
                        ),
                        stat_card(
                            "Sales",
                            "12,234",
                            "+19% from last month",
                            fluent.FluentIcons.CART,
                        ),
                        stat_card(
                            "Active now",
                            "573",
                            "+201 since last hour",
                            fluent.FluentIcons.PULSE,
                        ),
                    ],
                ),
                ft.ResponsiveRow(
                    spacing=16,
                    run_spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        column(new_project_card(), team_card()),
                        column(calendar_card(), storage_card()),
                        column(activity_card(), settings_card()),
                    ],
                ),
            ],
        ),
    )


def placeholder(name: str) -> fluent.ScaffoldPage:
    return fluent.ScaffoldPage(
        header=fluent.PageHeader(title=name),
        content=muted(f"{name} goes here."),
    )


async def main(page: ft.Page):
    page.title = "Fluent UI for Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 1360
    page.window.height = 900

    theme = fluent.Theme(accent_color=ACCENTS[0][1], content=ft.Container())
    theme.content = fluent.NavigationView(
        expand=True,
        selected_index=0,
        display_mode=fluent.PaneDisplayMode.AUTO,
        header=ft.Row(
            spacing=10,
            controls=[
                ft.Icon(fluent.FluentIcons.BOARD, size=20),
                ft.Text("Contoso", size=16, weight=ft.FontWeight.W_600),
            ],
        ),
        items=[
            fluent.PaneItem(
                "Home",
                icon=fluent.FluentIcons.HOME,
                content=dashboard(page, theme),
            ),
            fluent.PaneItem(
                "Analytics",
                icon=fluent.FluentIcons.DATA_TRENDING,
                content=placeholder("Analytics"),
            ),
            fluent.PaneItem(
                "Customers",
                icon=fluent.FluentIcons.PEOPLE_TEAM,
                info_badge=fluent.InfoBadge("4"),
                content=placeholder("Customers"),
            ),
            fluent.PaneItem(
                "Documents",
                icon=fluent.FluentIcons.FOLDER,
                content=placeholder("Documents"),
            ),
            fluent.PaneItemSeparator(),
            fluent.PaneItemHeader("Projects"),
            fluent.PaneItem(
                "flet-dashboard",
                icon=fluent.FluentIcons.BOARD,
                content=placeholder("flet-dashboard"),
            ),
            fluent.PaneItem(
                "Mobile app",
                icon=fluent.FluentIcons.PHONE,
                content=placeholder("Mobile app"),
            ),
        ],
        footer_items=[
            fluent.PaneItem(
                "Settings",
                icon=fluent.FluentIcons.SETTINGS,
                content=placeholder("Settings"),
            ),
        ],
    )

    page.add(ft.SafeArea(expand=True, content=theme))
    await page.window.center()


if __name__ == "__main__":
    ft.run(main)
