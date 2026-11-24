import datetime

import flet_shadcn_ui as shad

import flet as ft

PAYMENTS = [
    ("Success", "ken99@example.com", 316.00),
    ("Success", "abe45@example.com", 242.00),
    ("Pending", "monica@example.com", 837.00),
    ("Failed", "carla@example.com", 721.00),
    ("Success", "silas22@example.com", 129.00),
]

STATUS_BADGES = {
    "Success": shad.BadgeVariant.SECONDARY,
    "Pending": shad.BadgeVariant.OUTLINE,
    "Failed": shad.BadgeVariant.DESTRUCTIVE,
}

TEAM = [
    ("Sofia Davis", "m@example.com", "SD", "owner"),
    ("Jackson Lee", "p@example.com", "JL", "developer"),
    ("Isabella Nguyen", "i@example.com", "IN", "billing"),
]

ROLES = [
    ("owner", "Owner"),
    ("developer", "Developer"),
    ("billing", "Billing"),
    ("viewer", "Viewer"),
]


def muted(value: str, size: float = 14) -> ft.Text:
    return ft.Text(value, size=size, color=ft.Colors.ON_SURFACE_VARIANT)


def stat_card(title: str, value: str, change: str, icon: ft.IconData) -> shad.Card:
    return shad.Card(
        expand=True,
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(title, size=14, weight=ft.FontWeight.W_500),
                        ft.Icon(icon, size=16, color=ft.Colors.ON_SURFACE_VARIANT),
                    ],
                ),
                ft.Text(value, size=26, weight=ft.FontWeight.BOLD),
                muted(change, size=12),
            ],
        ),
    )


def create_account_card() -> shad.Card:
    return shad.Card(
        title="Create an account",
        description="Enter your email below to create your account",
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Container(height=4),
                ft.Row(
                    spacing=12,
                    controls=[
                        shad.Button(
                            "Apple",
                            leading=shad.LucideIcons.APPLE,
                            variant=shad.ButtonVariant.OUTLINE,
                            expand=True,
                        ),
                        shad.Button(
                            "Google",
                            leading=shad.LucideIcons.MAIL,
                            variant=shad.ButtonVariant.OUTLINE,
                            expand=True,
                        ),
                    ],
                ),
                ft.Row(
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        shad.Separator(expand=True),
                        muted("OR CONTINUE WITH", size=11),
                        shad.Separator(expand=True),
                    ],
                ),
                shad.Input(
                    label="Email",
                    placeholder="m@example.com",
                    keyboard_type=ft.KeyboardType.EMAIL,
                ),
                shad.Input(label="Password", password=True, value="secret123"),
                ft.Row([shad.Button("Create account", expand=True)]),
            ],
        ),
    )


def team_card() -> shad.Card:
    return shad.Card(
        title="Team Members",
        description="Invite your team members to collaborate.",
        content=ft.Column(
            spacing=16,
            controls=[ft.Container(height=0)]
            + [
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            spacing=12,
                            controls=[
                                shad.Avatar(placeholder=initials),
                                ft.Column(
                                    spacing=0,
                                    controls=[
                                        ft.Text(
                                            name, size=14, weight=ft.FontWeight.W_500
                                        ),
                                        muted(email, size=13),
                                    ],
                                ),
                            ],
                        ),
                        shad.Select(
                            value=role,
                            min_width=130,
                            options=[
                                shad.SelectOption(value=v, text=t) for v, t in ROLES
                            ],
                        ),
                    ],
                )
                for name, email, initials, role in TEAM
            ],
        ),
    )


def calendar_card() -> shad.Card:
    return shad.Card(
        padding=8,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[shad.Calendar(value=datetime.date(2026, 11, 4))],
        ),
    )


def goal_card() -> shad.Card:
    goal = ft.Text("350", size=56, weight=ft.FontWeight.BOLD)

    def set_goal(value: float):
        value = max(200, min(600, round(value / 10) * 10))
        slider.value = value
        goal.value = str(int(value))

    slider = shad.Slider(
        value=350,
        min=200,
        max=600,
        on_change=lambda e: set_goal(e.control.value),
    )

    return shad.Card(
        title="Move Goal",
        description="Set your daily activity goal.",
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        shad.IconButton(
                            icon=shad.LucideIcons.MINUS,
                            variant=shad.ButtonVariant.OUTLINE,
                            on_click=lambda: set_goal(slider.value - 10),
                        ),
                        ft.Column(
                            spacing=0,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[goal, muted("CALORIES/DAY", size=11)],
                        ),
                        shad.IconButton(
                            icon=shad.LucideIcons.PLUS,
                            variant=shad.ButtonVariant.OUTLINE,
                            on_click=lambda: set_goal(slider.value + 10),
                        ),
                    ],
                ),
                slider,
            ],
        ),
    )


def notifications_card() -> shad.Card:
    return shad.Card(
        title="Notifications",
        description="Choose what you want to be notified about.",
        content=ft.Column(
            spacing=16,
            controls=[
                ft.Container(height=0),
                shad.Switch(
                    label="Push notifications",
                    sublabel="Send notifications to your devices.",
                    value=True,
                ),
                shad.Switch(
                    label="Product updates",
                    sublabel="News about features and releases.",
                ),
                shad.Checkbox(
                    label="Weekly digest",
                    sublabel="A summary of activity every Monday.",
                    value=True,
                ),
            ],
        ),
    )


def payments_card() -> shad.Card:
    right = ft.Alignment.CENTER_RIGHT
    return shad.Card(
        title="Payments",
        description="Manage your payments.",
        content=ft.Container(
            padding=ft.Padding.only(top=12),
            content=shad.Table(
                row_height=44,
                columns=[
                    shad.TableColumn("Status", width=110),
                    shad.TableColumn("Email", fill=True),
                    shad.TableColumn("Amount", width=90, alignment=right),
                ],
                rows=[
                    shad.TableRow(
                        cells=[
                            shad.TableCell(
                                shad.Badge(status, variant=STATUS_BADGES[status])
                            ),
                            shad.TableCell(email),
                            shad.TableCell(f"${amount:,.2f}"),
                        ]
                    )
                    for status, email, amount in PAYMENTS
                ],
            ),
        ),
    )


def verify_card() -> shad.Card:
    return shad.Card(
        title="Verify your login",
        description="Enter the code we sent to your phone.",
        content=ft.Column(
            spacing=12,
            controls=[
                ft.Container(height=0),
                shad.InputOTP(value="4096", length=6, groups=[3, 3]),
                muted("Didn't get a code? Resend in 0:42", size=13),
            ],
        ),
    )


async def main(page: ft.Page):
    page.title = "Shadcn UI for Flet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 1360
    page.window.height = 900

    def toggle_theme_mode():
        dark = page.theme_mode == ft.ThemeMode.DARK
        page.theme_mode = ft.ThemeMode.LIGHT if dark else ft.ThemeMode.DARK
        mode_button.icon = shad.LucideIcons.MOON if dark else shad.LucideIcons.SUN

    def change_color_scheme(e: ft.Event[shad.Select]):
        theme.color_scheme = shad.ColorScheme(e.control.value)

    mode_button = shad.IconButton(
        icon=shad.LucideIcons.MOON,
        variant=shad.ButtonVariant.OUTLINE,
        on_click=toggle_theme_mode,
    )

    header = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Row(
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(shad.LucideIcons.LAYOUT_DASHBOARD, size=22),
                    ft.Text("Dashboard", size=22, weight=ft.FontWeight.BOLD),
                    shad.Badge("Flet 1.1", variant=shad.BadgeVariant.OUTLINE),
                    ft.Container(width=8),
                    shad.Tabs(
                        width=300,
                        value="overview",
                        tabs=[
                            shad.Tab(value="overview", label="Overview"),
                            shad.Tab(value="analytics", label="Analytics"),
                            shad.Tab(value="reports", label="Reports"),
                        ],
                    ),
                ],
            ),
            ft.Row(
                spacing=8,
                controls=[
                    shad.Input(
                        placeholder="Search...",
                        leading=shad.LucideIcons.SEARCH,
                        width=220,
                    ),
                    shad.Select(
                        value=shad.ColorScheme.ZINC.value,
                        min_width=120,
                        on_change=change_color_scheme,
                        options=[
                            shad.SelectOption(value=s.value, text=s.name.title())
                            for s in shad.ColorScheme
                        ],
                    ),
                    mode_button,
                    shad.Button("Download", leading=shad.LucideIcons.DOWNLOAD),
                ],
            ),
        ],
    )

    stats = ft.Row(
        spacing=16,
        controls=[
            stat_card(
                "Total Revenue",
                "$45,231.89",
                "+20.1% from last month",
                shad.LucideIcons.DOLLAR_SIGN,
            ),
            stat_card(
                "Subscriptions",
                "+2,350",
                "+180.1% from last month",
                shad.LucideIcons.USERS,
            ),
            stat_card(
                "Sales", "+12,234", "+19% from last month", shad.LucideIcons.CREDIT_CARD
            ),
            stat_card(
                "Active Now", "+573", "+201 since last hour", shad.LucideIcons.ACTIVITY
            ),
        ],
    )

    def column(*cards: ft.Control) -> ft.Column:
        return ft.Column(
            col={"xs": 12, "md": 6, "lg": 4}, spacing=16, controls=list(cards)
        )

    theme = shad.Theme(
        color_scheme=shad.ColorScheme.ZINC,
        content=ft.Column(
            spacing=20,
            controls=[
                header,
                stats,
                ft.ResponsiveRow(
                    spacing=16,
                    run_spacing=16,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        column(create_account_card(), team_card()),
                        column(calendar_card(), goal_card(), verify_card()),
                        column(payments_card(), notifications_card()),
                    ],
                ),
            ],
        ),
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                expand=True,
                controls=[ft.Container(padding=24, content=theme)],
            ),
        )
    )
    await page.window.center()


if __name__ == "__main__":
    ft.run(main)
