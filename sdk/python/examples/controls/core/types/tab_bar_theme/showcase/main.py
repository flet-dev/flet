import flet as ft

TABS = [
    ("Inbox", ft.Icons.INBOX),
    ("Starred", ft.Icons.STAR),
    ("Archive", ft.Icons.ARCHIVE),
]


def tab_bar(**props) -> ft.TabBar:
    return ft.TabBar(
        **props,
        tabs=[ft.Tab(label=label, icon=icon) for label, icon in TABS],
    )


def showcase_card(
    title: str,
    description: str,
    bar: ft.TabBar,
    theme: ft.Theme | None = None,
) -> ft.Container:
    return ft.Container(
        padding=12,
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
        theme=theme,
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(title, weight=ft.FontWeight.BOLD),
                ft.Text(description, size=12),
                ft.Tabs(
                    length=len(TABS),
                    content=ft.Column(
                        spacing=0,
                        controls=[
                            bar,
                            ft.Container(
                                height=60,
                                content=ft.TabBarView(
                                    controls=[
                                        ft.Container(
                                            alignment=ft.Alignment.CENTER,
                                            content=ft.Text(f"{label} messages"),
                                        )
                                        for label, _ in TABS
                                    ]
                                ),
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        tab_bar_theme=ft.TabBarTheme(
            indicator_color=ft.Colors.DEEP_PURPLE,
            indicator_size=ft.TabBarIndicatorSize.TAB,
            label_color=ft.Colors.DEEP_PURPLE,
            unselected_label_color=ft.Colors.GREY_600,
            label_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            divider_color=ft.Colors.DEEP_PURPLE_100,
            overlay_color={
                ft.ControlState.HOVERED: ft.Colors.with_opacity(
                    0.08, ft.Colors.DEEP_PURPLE
                ),
                ft.ControlState.PRESSED: ft.Colors.with_opacity(
                    0.16, ft.Colors.DEEP_PURPLE
                ),
            },
        )
    )

    page.appbar = ft.AppBar(title="TabBarTheme Showcase")
    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    showcase_card(
                        title="App-wide theme",
                        description="Styled by the page's tab_bar_theme.",
                        bar=tab_bar(),
                    ),
                    showcase_card(
                        title="Section theme",
                        description=(
                            "The container's theme replaces the indicator and "
                            "label color. The other values come from the page."
                        ),
                        bar=tab_bar(),
                        theme=ft.Theme(
                            tab_bar_theme=ft.TabBarTheme(
                                indicator_size=ft.TabBarIndicatorSize.LABEL,
                                label_color=ft.Colors.TEAL,
                                indicator=ft.UnderlineTabIndicator(
                                    border_side=ft.BorderSide(
                                        width=4, color=ft.Colors.TEAL
                                    ),
                                    border_radius=ft.BorderRadius.only(
                                        top_left=4, top_right=4
                                    ),
                                ),
                            )
                        ),
                    ),
                    showcase_card(
                        title="TabBar properties",
                        description=(
                            "Properties set on the TabBar take precedence over "
                            "any theme."
                        ),
                        bar=tab_bar(
                            indicator_color=ft.Colors.ORANGE,
                            label_color=ft.Colors.ORANGE,
                        ),
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
