import flet as ft


def resolve_theme_token(token_name: str) -> ft.ColorValue:
    return getattr(ft.Colors, token_name)


def color_band(
    role_label: str,
    display_label: str,
    background: ft.ColorValue,
    foreground: ft.ColorValue,
    *,
    width: int,
    height: int,
    selected: bool = False,
    on_click=None,
) -> ft.Container:
    swatch_size = max(24, height - 8)
    return ft.Container(
        width=width,
        height=height,
        padding=ft.Padding.symmetric(horizontal=8),
        ink=True,
        on_click=on_click,
        content=ft.Row(
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=swatch_size,
                    height=swatch_size,
                    bgcolor=background,
                    border_radius=8,
                    border=ft.Border.all(
                        2 if selected else 1,
                        ft.Colors.BLACK if selected else ft.Colors.OUTLINE_VARIANT,
                    ),
                ),
                ft.Container(
                    content=ft.Text(
                        display_label,
                        size=12,
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                ),
            ],
        ),
    )


def color_group(
    items: list[tuple[str, str, ft.ColorValue, ft.ColorValue]],
    *,
    width: int,
    height: int,
    title: str | None = None,
    hint: str | None = None,
    swatch_theme: ft.Theme,
    swatch_dark_theme: ft.Theme,
    swatch_theme_mode: ft.ThemeMode,
    selected_label: str | None = None,
    on_color_click=None,
) -> ft.Container:
    return ft.Container(
        border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
        content=ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    visible=title is not None or hint is not None,
                    height=25,
                    padding=ft.Padding.only(left=8, right=2),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Text(title or "", weight=ft.FontWeight.W_600),
                            ft.Container(
                                visible=hint is not None,
                                content=ft.IconButton(
                                    icon=ft.Icons.INFO_OUTLINE,
                                    icon_size=14,
                                    tooltip=ft.Tooltip(
                                        message=hint or "",
                                        bgcolor=ft.Colors.SURFACE_BRIGHT,
                                        padding=ft.Padding.symmetric(
                                            horizontal=12, vertical=8
                                        ),
                                        prefer_below=False,
                                        vertical_offset=8,
                                        text_style=ft.TextStyle(
                                            color=ft.Colors.ON_SURFACE
                                        ),
                                    ),
                                ),
                            ),
                        ],
                    ),
                ),
                *[
                    ft.Container(
                        theme=swatch_theme,
                        dark_theme=swatch_dark_theme,
                        theme_mode=swatch_theme_mode,
                        content=color_band(
                            role_label,
                            display_label,
                            background,
                            foreground,
                            width=width,
                            height=height,
                            selected=selected_label == role_label,
                            on_click=(
                                on_color_click(role_label) if on_color_click else None
                            ),
                        ),
                    )
                    for role_label, display_label, background, foreground in items
                ],
            ],
        ),
    )


def showcase_section(title: str, *controls: ft.Control) -> ft.Container:
    return ft.Container(
        margin=ft.Margin.only(bottom=16),
        content=ft.Column(spacing=8, controls=[ft.Text(title), *controls]),
    )


def material_color_circle(
    color: ft.ColorValue, label: str, *, selected: bool = False, on_click=None
) -> ft.Container:
    selected_border_color = (
        getattr(ft.Colors, f"{label}_900")
        if hasattr(ft.Colors, f"{label}_900")
        else ft.Colors.BLACK
    )
    return ft.Container(
        width=28,
        height=28,
        border_radius=14,
        bgcolor=color,
        border=ft.Border.all(
            2 if selected else 1,
            selected_border_color if selected else ft.Colors.OUTLINE_VARIANT,
        ),
        tooltip=label,
        ink=True,
        on_click=on_click,
    )


def material_shade_swatch(
    color: ft.ColorValue, label: str, *, selected: bool = False, on_click=None
) -> ft.Container:
    return ft.Container(
        width=32,
        height=44,
        border_radius=22 if selected else 0,
        bgcolor=color,
        alignment=ft.Alignment.TOP_CENTER,
        padding=ft.Padding.only(top=5),
        tooltip=label,
        ink=True,
        on_click=on_click,
        content=ft.Text(
            label,
            size=11,
            color=ft.Colors.BLACK if label in {"50", "100", "200"} else ft.Colors.WHITE,
        ),
    )


def build_left_pane_controls(
    *,
    selected_label: str | None,
    swatch_width: int,
    swatch_height: int,
    theme_mode: ft.ThemeMode,
    role_tabs: list[dict],
    selected_tab_index: int,
    seed_color_options: list[tuple[str, ft.ColorValue]],
    selected_seed_color: ft.ColorValue,
    swatch_theme: ft.Theme,
    swatch_dark_theme: ft.Theme,
    swatch_theme_mode: ft.ThemeMode,
    get_role_value,
    format_role_value,
    on_color_click,
    on_tab_change,
    on_select_seed,
    on_toggle_theme,
    on_export,
    on_import,
) -> list[ft.Control]:
    active_tab = role_tabs[selected_tab_index]
    return [
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=8,
                    controls=[
                        ft.PopupMenuButton(
                            icon=ft.Icons.PALETTE,
                            tooltip="Rebuild from seed",
                            menu_position=ft.PopupMenuPosition.UNDER,
                            items=[
                                ft.PopupMenuItem(
                                    checked=color == selected_seed_color,
                                    content=ft.Row(
                                        spacing=12,
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.PALETTE_OUTLINED,
                                                color=color,
                                            ),
                                            ft.Text(label),
                                        ],
                                    ),
                                    on_click=on_select_seed(color),
                                )
                                for label, color in seed_color_options
                            ],
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DOWNLOAD,
                            tooltip="Export",
                            on_click=on_export,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.UPLOAD,
                            tooltip="Import",
                            on_click=on_import,
                        ),
                    ],
                ),
                ft.IconButton(
                    icon=(
                        ft.Icons.DARK_MODE
                        if theme_mode == ft.ThemeMode.LIGHT
                        else ft.Icons.LIGHT_MODE
                    ),
                    tooltip=(
                        "Switch to dark mode"
                        if theme_mode == ft.ThemeMode.LIGHT
                        else "Switch to light mode"
                    ),
                    on_click=on_toggle_theme,
                ),
            ],
        ),
        ft.Tabs(
            length=len(role_tabs),
            selected_index=selected_tab_index,
            on_change=on_tab_change,
            content=ft.TabBar(
                tab_alignment=ft.TabAlignment.START,
                scrollable=True,
                tabs=[ft.Tab(label=tab["label"]) for tab in role_tabs],
            ),
        ),
        *[
            color_group(
                [
                    (
                        label,
                        label,
                        get_role_value(background_token),
                        get_role_value(foreground_token),
                    )
                    for label, background_token, foreground_token in group["items"]
                ],
                width=swatch_width,
                height=swatch_height,
                title=group.get("title"),
                hint=group.get("hint"),
                swatch_theme=swatch_theme,
                swatch_dark_theme=swatch_dark_theme,
                swatch_theme_mode=swatch_theme_mode,
                selected_label=selected_label,
                on_color_click=on_color_click,
            )
            for group in active_tab["groups"]
        ],
    ]


def preview_role_block(
    label: str, background: ft.ColorValue, foreground: ft.ColorValue
) -> ft.Container:
    return ft.Container(
        bgcolor=background,
        padding=12,
        border_radius=12,
        content=ft.Text(label, color=foreground),
    )


def surface_sample_card(
    label: str,
    background: ft.ColorValue,
    foreground: ft.ColorValue,
    *,
    outline_label: str,
    outline_color: ft.ColorValue,
    text_label: str,
) -> ft.Container:
    subtitle = f"{outline_label}, {text_label}" if outline_label else text_label
    return ft.Container(
        width=300,
        height=132,
        bgcolor=background,
        border_radius=16,
        border=ft.Border.all(2, outline_color),
        padding=16,
        content=ft.Column(
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Text(
                    label,
                    color=foreground,
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
                ft.Text(
                    subtitle,
                    color=foreground,
                    size=13,
                ),
            ],
        ),
    )


def inverse_surface_card() -> ft.Container:
    return ft.Container(
        width=300,
        height=132,
        bgcolor=ft.Colors.INVERSE_SURFACE,
        border_radius=16,
        padding=16,
        content=ft.Column(
            spacing=12,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Text(
                    "INVERSE_SURFACE",
                    color=ft.Colors.ON_INVERSE_SURFACE,
                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
                ft.Text(
                    "On inverse surface, Inverse primary",
                    color=ft.Colors.ON_INVERSE_SURFACE,
                    size=13,
                ),
                ft.Container(
                    bgcolor=ft.Colors.INVERSE_PRIMARY,
                    border_radius=999,
                    padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                    content=ft.Text(
                        "OK",
                        color=ft.Colors.ON_PRIMARY,
                        weight=ft.FontWeight.W_600,
                    ),
                ),
            ],
        ),
    )


def noop(_):
    return None


def build_preview_chip_row() -> ft.Row:
    return ft.Row(
        wrap=True,
        spacing=12,
        run_spacing=12,
        controls=[
            ft.Chip(label=ft.Text("Filter chip"), on_select=noop),
            ft.Chip(
                label=ft.Text("Assist chip"),
                leading=ft.Icon(ft.Icons.MAP_SHARP),
                on_click=noop,
            ),
            ft.Chip(label=ft.Text("Selected"), selected=True, on_select=noop),
        ],
    )


def build_selected_chip_row() -> ft.Row:
    return ft.Row(
        wrap=True,
        spacing=12,
        run_spacing=12,
        controls=[
            ft.Chip(label=ft.Text("Filter chip"), on_select=noop),
            ft.Chip(label=ft.Text("Selected"), selected=True, on_select=noop),
        ],
    )


def build_primary_button_row() -> ft.Row:
    return ft.Row(
        wrap=True,
        spacing=12,
        run_spacing=12,
        controls=[
            ft.FilledButton("Filled button"),
            ft.OutlinedButton("Outlined button"),
            ft.TextButton("Text button"),
            ft.Button("Button"),
        ],
    )


def build_segmented_button() -> ft.SegmentedButton:
    return ft.SegmentedButton(
        selected=["grid"],
        segments=[
            ft.Segment(
                value="list",
                icon=ft.Icon(ft.Icons.VIEW_LIST),
                label=ft.Text("List"),
            ),
            ft.Segment(
                value="grid",
                icon=ft.Icon(ft.Icons.GRID_VIEW),
                label=ft.Text("Grid"),
            ),
        ],
    )


def build_tonal_button() -> ft.FilledTonalButton:
    return ft.FilledTonalButton("Filled tonal button")


def build_selection_row() -> ft.Row:
    return ft.Row(
        wrap=True,
        spacing=16,
        run_spacing=12,
        controls=[
            ft.Switch(label="Use dark mode", value=True),
            ft.Checkbox(label="Enable accents", value=True),
        ],
    )


def build_error_examples() -> list[ft.Control]:
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        value="hunter2",
    )
    password_field.error = "Incorrect password"
    return [
        password_field,
        ft.Text("Please correct the highlighted fields.", color=ft.Colors.ERROR),
    ]


def build_all_preview_pagelet(
    *,
    preview_heading: str,
    preview_body: str,
    preview_time_text: ft.Text,
    open_preview_time_picker,
) -> ft.Pagelet:
    return ft.Pagelet(
        height=760,
        bgcolor=ft.Colors.SURFACE,
        appbar=ft.AppBar(
            leading=ft.Icon(ft.Icons.PALETTE),
            title=ft.Row(
                spacing=16,
                controls=[
                    ft.Text("Palette preview"),
                    ft.Container(
                        width=280,
                        height=40,
                        bgcolor=ft.Colors.SURFACE,
                        border_radius=999,
                        padding=ft.Padding.symmetric(horizontal=14),
                        content=ft.Row(
                            spacing=10,
                            controls=[
                                ft.Icon(
                                    ft.Icons.SEARCH,
                                    size=18,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                ),
                                ft.Text(
                                    "Search palettes and roles",
                                    size=13,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            actions=[
                ft.IconButton(icon=ft.Icons.HELP_OUTLINE),
                ft.IconButton(icon=ft.Icons.SETTINGS_OUTLINED),
                ft.IconButton(icon=ft.Icons.MORE_VERT),
            ],
        ),
        content=ft.Container(
            padding=ft.Padding.only(top=12, bottom=12),
            content=ft.Row(
                expand=True,
                spacing=12,
                controls=[
                    ft.NavigationRail(
                        selected_index=1,
                        bgcolor=ft.Colors.SURFACE_CONTAINER,
                        label_type=ft.NavigationRailLabelType.ALL,
                        min_width=76,
                        destinations=[
                            ft.NavigationRailDestination(
                                icon=ft.Icons.HOME_OUTLINED,
                                selected_icon=ft.Icons.HOME,
                                label="Home",
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.PALETTE_OUTLINED,
                                selected_icon=ft.Icons.PALETTE,
                                label="Theme",
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.Icons.SCHEDULE_OUTLINED,
                                selected_icon=ft.Icons.SCHEDULE,
                                label="Time",
                            ),
                        ],
                    ),
                    ft.Container(
                        width=220,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
                        border_radius=20,
                        padding=16,
                        content=ft.Column(
                            spacing=14,
                            controls=[
                                ft.FilledTonalButton("New palette", icon=ft.Icons.ADD),
                                ft.Text(
                                    "Recent palettes",
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                ),
                                ft.Column(
                                    spacing=8,
                                    controls=[
                                        ft.Container(
                                            bgcolor=ft.Colors.SECONDARY_CONTAINER,
                                            border_radius=14,
                                            padding=12,
                                            content=ft.Row(
                                                spacing=10,
                                                controls=[
                                                    ft.Icon(
                                                        ft.Icons.PALETTE,
                                                        color=ft.Colors.ON_SECONDARY_CONTAINER,
                                                    ),
                                                    ft.Text(
                                                        "Studio theme",
                                                        color=ft.Colors.ON_SECONDARY_CONTAINER,
                                                    ),
                                                ],
                                            ),
                                        ),
                                        ft.Row(
                                            spacing=10,
                                            controls=[
                                                ft.CircleAvatar(
                                                    content=ft.Text("A"),
                                                    bgcolor=ft.Colors.PRIMARY_CONTAINER,
                                                    color=ft.Colors.ON_PRIMARY_CONTAINER,
                                                ),
                                                ft.Column(
                                                    spacing=2,
                                                    controls=[
                                                        ft.Text("Accent set"),
                                                        ft.Text(
                                                            "Primary and secondary",
                                                            size=12,
                                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        ft.Row(
                                            spacing=10,
                                            controls=[
                                                ft.CircleAvatar(
                                                    content=ft.Text("S"),
                                                    bgcolor=ft.Colors.TERTIARY_CONTAINER,
                                                    color=ft.Colors.ON_TERTIARY_CONTAINER,
                                                ),
                                                ft.Column(
                                                    spacing=2,
                                                    controls=[
                                                        ft.Text("Surface study"),
                                                        ft.Text(
                                                            "Containers and outline",
                                                            size=12,
                                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                        ft.Row(
                                            spacing=10,
                                            controls=[
                                                ft.CircleAvatar(
                                                    content=ft.Text("E"),
                                                    bgcolor=ft.Colors.ERROR_CONTAINER,
                                                    color=ft.Colors.ON_ERROR_CONTAINER,
                                                ),
                                                ft.Column(
                                                    spacing=2,
                                                    controls=[
                                                        ft.Text("Errors and states"),
                                                        ft.Text(
                                                            "Validation colors",
                                                            size=12,
                                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        expand=2,
                        bgcolor=ft.Colors.SURFACE_CONTAINER_LOWEST,
                        border_radius=20,
                        padding=18,
                        content=ft.Column(
                            spacing=14,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Column(
                                            spacing=4,
                                            controls=[
                                                ft.Text(
                                                    preview_heading,
                                                    theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                                ),
                                                ft.Text(
                                                    "Theme collaboration space",
                                                    size=12,
                                                    color=ft.Colors.ON_SURFACE_VARIANT,
                                                ),
                                            ],
                                        ),
                                        build_selected_chip_row(),
                                    ],
                                ),
                                ft.Container(
                                    bgcolor=ft.Colors.SURFACE,
                                    border_radius=18,
                                    padding=16,
                                    content=ft.Column(
                                        spacing=14,
                                        controls=[
                                            ft.Row(
                                                spacing=10,
                                                controls=[
                                                    ft.CircleAvatar(
                                                        content=ft.Text("P"),
                                                        bgcolor=ft.Colors.PRIMARY,
                                                        color=ft.Colors.ON_PRIMARY,
                                                    ),
                                                    ft.Column(
                                                        spacing=2,
                                                        controls=[
                                                            ft.Text("Palette review"),
                                                            ft.Text(
                                                                "22 members",
                                                                size=12,
                                                                color=ft.Colors.ON_SURFACE_VARIANT,
                                                            ),
                                                        ],
                                                    ),
                                                ],
                                            ),
                                            ft.Text(preview_body),
                                            ft.Container(
                                                bgcolor=ft.Colors.PRIMARY_CONTAINER,
                                                border_radius=16,
                                                padding=14,
                                                content=ft.Column(
                                                    spacing=6,
                                                    controls=[
                                                        ft.Text(
                                                            "Primary spotlight",
                                                            color=ft.Colors.ON_PRIMARY_CONTAINER,
                                                            weight=ft.FontWeight.W_600,
                                                        ),
                                                        ft.Text(
                                                            "Use this space to "
                                                            "compare strong accents "
                                                            "against calmer surfaces.",
                                                            color=ft.Colors.ON_PRIMARY_CONTAINER,
                                                            size=12,
                                                        ),
                                                    ],
                                                ),
                                            ),
                                            ft.Row(
                                                spacing=12,
                                                controls=[
                                                    ft.FilledButton("Apply"),
                                                    ft.FilledTonalButton("Share"),
                                                    ft.OutlinedButton("Inspect"),
                                                ],
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Row(
                                    wrap=True,
                                    spacing=16,
                                    run_spacing=12,
                                    controls=[
                                        ft.Switch(label="Use dark mode", value=True),
                                        ft.Checkbox(label="Enable accents", value=True),
                                    ],
                                ),
                                *build_error_examples(),
                            ],
                        ),
                    ),
                    ft.Container(
                        width=240,
                        bgcolor=ft.Colors.SURFACE_CONTAINER,
                        border_radius=20,
                        padding=16,
                        content=ft.Column(
                            spacing=14,
                            controls=[
                                ft.Text(
                                    "Today",
                                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                ),
                                ft.Container(
                                    bgcolor=ft.Colors.TERTIARY_CONTAINER,
                                    border_radius=18,
                                    padding=14,
                                    content=ft.Column(
                                        spacing=6,
                                        controls=[
                                            ft.Text(
                                                "Teaching workshop",
                                                color=ft.Colors.ON_TERTIARY_CONTAINER,
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            ft.Text(
                                                "9:00 AM - 12:00 PM",
                                                color=ft.Colors.ON_TERTIARY_CONTAINER,
                                                size=12,
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    bgcolor=ft.Colors.SECONDARY_CONTAINER,
                                    border_radius=18,
                                    padding=14,
                                    content=ft.Column(
                                        spacing=6,
                                        controls=[
                                            ft.Text(
                                                "Lunch",
                                                color=ft.Colors.ON_SECONDARY_CONTAINER,
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            ft.Text(
                                                "1:00 PM - 2:00 PM",
                                                color=ft.Colors.ON_SECONDARY_CONTAINER,
                                                size=12,
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    bgcolor=ft.Colors.ERROR_CONTAINER,
                                    border_radius=18,
                                    padding=14,
                                    content=ft.Column(
                                        spacing=6,
                                        controls=[
                                            ft.Text(
                                                "Review alerts",
                                                color=ft.Colors.ON_ERROR_CONTAINER,
                                                weight=ft.FontWeight.W_600,
                                            ),
                                            ft.Text(
                                                "2 palette issues need attention",
                                                color=ft.Colors.ON_ERROR_CONTAINER,
                                                size=12,
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ),
        bottom_appbar=ft.BottomAppBar(
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        spacing=4,
                        controls=[
                            ft.IconButton(icon=ft.Icons.MENU),
                            ft.IconButton(icon=ft.Icons.TUNE),
                        ],
                    ),
                    ft.Row(
                        spacing=4,
                        controls=[
                            ft.IconButton(icon=ft.Icons.CHAT_BUBBLE_OUTLINE),
                            ft.IconButton(icon=ft.Icons.PERSON_OUTLINE),
                        ],
                    ),
                ],
            )
        ),
        floating_action_button=ft.FloatingActionButton(icon=ft.Icons.ADD),
        floating_action_button_location=ft.FloatingActionButtonLocation.END_FLOAT,
    )


def build_preview_tabs(
    *,
    preview_heading: str,
    preview_body: str,
    preview_time_text: ft.Text,
    scaffold_bgcolor: ft.ColorValue,
    selected_tab_index: int,
    on_tab_change,
    open_preview_time_picker,
) -> ft.Tabs:
    return ft.Tabs(
        selected_index=selected_tab_index,
        on_change=on_tab_change,
        length=4,
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[
                        ft.Text("Example", color=ft.Colors.ON_SURFACE),
                    ],
                ),
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="All"),
                        ft.Tab(label="Accent"),
                        ft.Tab(label="Surface"),
                        ft.Tab(label="Add-on"),
                    ]
                ),
                ft.TabBarView(
                    expand=True,
                    controls=[
                        ft.Container(
                            padding=ft.Padding.only(top=4),
                            content=ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                spacing=0,
                                controls=[
                                    build_all_preview_pagelet(
                                        preview_heading=preview_heading,
                                        preview_body=preview_body,
                                        preview_time_text=preview_time_text,
                                        open_preview_time_picker=open_preview_time_picker,
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            padding=ft.Padding.only(top=4),
                            content=ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                spacing=0,
                                controls=[
                                    showcase_section(
                                        "Primary",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                surface_sample_card(
                                                    "PRIMARY",
                                                    ft.Colors.PRIMARY,
                                                    ft.Colors.ON_PRIMARY,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On primary",
                                                ),
                                                surface_sample_card(
                                                    "PRIMARY_CONTAINER",
                                                    ft.Colors.PRIMARY_CONTAINER,
                                                    ft.Colors.ON_PRIMARY_CONTAINER,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On primary container",
                                                ),
                                            ],
                                        ),
                                        build_primary_button_row(),
                                        ft.FloatingActionButton(icon=ft.Icons.PALETTE),
                                    ),
                                    showcase_section(
                                        "Secondary",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                surface_sample_card(
                                                    "SECONDARY",
                                                    ft.Colors.SECONDARY,
                                                    ft.Colors.ON_SECONDARY,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On secondary",
                                                ),
                                                surface_sample_card(
                                                    "SECONDARY_CONTAINER",
                                                    ft.Colors.SECONDARY_CONTAINER,
                                                    ft.Colors.ON_SECONDARY_CONTAINER,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On secondary container",
                                                ),
                                            ],
                                        ),
                                        build_tonal_button(),
                                        build_preview_chip_row(),
                                        build_segmented_button(),
                                    ),
                                    showcase_section(
                                        "Tertiary",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                surface_sample_card(
                                                    "TERTIARY",
                                                    ft.Colors.TERTIARY,
                                                    ft.Colors.ON_TERTIARY,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On tertiary",
                                                ),
                                                surface_sample_card(
                                                    "TERTIARY_CONTAINER",
                                                    ft.Colors.TERTIARY_CONTAINER,
                                                    ft.Colors.ON_TERTIARY_CONTAINER,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On tertiary container",
                                                ),
                                            ],
                                        ),
                                    ),
                                    showcase_section(
                                        "Error",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                surface_sample_card(
                                                    "ERROR",
                                                    ft.Colors.ERROR,
                                                    ft.Colors.ON_ERROR,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On error",
                                                ),
                                                surface_sample_card(
                                                    "ERROR_CONTAINER",
                                                    ft.Colors.ERROR_CONTAINER,
                                                    ft.Colors.ON_ERROR_CONTAINER,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On error container",
                                                ),
                                            ],
                                        ),
                                        *build_error_examples(),
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            padding=ft.Padding.only(top=4),
                            content=ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                spacing=12,
                                controls=[
                                    ft.Row(
                                        wrap=True,
                                        spacing=12,
                                        run_spacing=12,
                                        controls=[
                                            surface_sample_card(
                                                "SURFACE",
                                                ft.Colors.SURFACE,
                                                ft.Colors.ON_SURFACE,
                                                outline_label="Outline",
                                                outline_color=ft.Colors.OUTLINE,
                                                text_label="On surface",
                                            ),
                                            surface_sample_card(
                                                "SURFACE_CONTAINER",
                                                ft.Colors.SURFACE_CONTAINER,
                                                ft.Colors.ON_SURFACE_VARIANT,
                                                outline_label="Outline variant",
                                                outline_color=ft.Colors.OUTLINE_VARIANT,
                                                text_label="On surface variant",
                                            ),
                                            surface_sample_card(
                                                "SURFACE_CONTAINER_LOW",
                                                ft.Colors.SURFACE_CONTAINER_LOW,
                                                ft.Colors.ON_SURFACE,
                                                outline_label="Outline",
                                                outline_color=ft.Colors.OUTLINE,
                                                text_label="On surface",
                                            ),
                                            surface_sample_card(
                                                "SURFACE_CONTAINER_LOWEST",
                                                ft.Colors.SURFACE_CONTAINER_LOWEST,
                                                ft.Colors.ON_SURFACE_VARIANT,
                                                outline_label="Outline variant",
                                                outline_color=ft.Colors.OUTLINE_VARIANT,
                                                text_label="On surface variant",
                                            ),
                                            surface_sample_card(
                                                "SURFACE_CONTAINER_HIGH",
                                                ft.Colors.SURFACE_CONTAINER_HIGH,
                                                ft.Colors.ON_SURFACE,
                                                outline_label="Outline",
                                                outline_color=ft.Colors.OUTLINE,
                                                text_label="On surface",
                                            ),
                                            surface_sample_card(
                                                "SURFACE_CONTAINER_HIGHEST",
                                                ft.Colors.SURFACE_CONTAINER_HIGHEST,
                                                ft.Colors.ON_SURFACE_VARIANT,
                                                outline_label="Outline variant",
                                                outline_color=ft.Colors.OUTLINE_VARIANT,
                                                text_label="On surface variant",
                                            ),
                                        ],
                                    ),
                                    ft.Row(
                                        wrap=True,
                                        spacing=12,
                                        run_spacing=12,
                                        controls=[
                                            ft.Container(
                                                width=300,
                                                height=132,
                                                bgcolor=scaffold_bgcolor,
                                                border_radius=16,
                                                border=ft.Border.all(
                                                    2, ft.Colors.OUTLINE_VARIANT
                                                ),
                                                padding=16,
                                                content=ft.Column(
                                                    spacing=12,
                                                    controls=[
                                                        ft.Text(
                                                            "SCAFFOLD_BGCOLOR",
                                                            color=ft.Colors.ON_SURFACE,
                                                            theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                                        ),
                                                        ft.Text(
                                                            (
                                                                "Outline variant, "
                                                                "On surface variant"
                                                            ),
                                                            color=ft.Colors.ON_SURFACE_VARIANT,
                                                        ),
                                                    ],
                                                ),
                                            ),
                                            inverse_surface_card(),
                                        ],
                                    ),
                                ],
                            ),
                        ),
                        ft.Container(
                            padding=ft.Padding.only(top=4),
                            content=ft.Column(
                                scroll=ft.ScrollMode.AUTO,
                                spacing=0,
                                controls=[
                                    showcase_section(
                                        "Primary fixed",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                surface_sample_card(
                                                    "PRIMARY_FIXED",
                                                    ft.Colors.PRIMARY_FIXED,
                                                    ft.Colors.ON_PRIMARY_FIXED,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On primary fixed",
                                                ),
                                                surface_sample_card(
                                                    "PRIMARY_FIXED_DIM",
                                                    ft.Colors.PRIMARY_FIXED_DIM,
                                                    ft.Colors.ON_PRIMARY_FIXED_VARIANT,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label=(
                                                        "On primary fixed variant"
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ),
                                    showcase_section(
                                        "Secondary fixed",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                surface_sample_card(
                                                    "SECONDARY_FIXED",
                                                    ft.Colors.SECONDARY_FIXED,
                                                    ft.Colors.ON_SECONDARY_FIXED,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On secondary fixed",
                                                ),
                                                surface_sample_card(
                                                    "SECONDARY_FIXED_DIM",
                                                    ft.Colors.SECONDARY_FIXED_DIM,
                                                    ft.Colors.ON_SECONDARY_FIXED_VARIANT,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label=(
                                                        "On secondary fixed variant"
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ),
                                    showcase_section(
                                        "Tertiary fixed",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                surface_sample_card(
                                                    "TERTIARY_FIXED",
                                                    ft.Colors.TERTIARY_FIXED,
                                                    ft.Colors.ON_TERTIARY_FIXED,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On tertiary fixed",
                                                ),
                                                surface_sample_card(
                                                    "TERTIARY_FIXED_DIM",
                                                    ft.Colors.TERTIARY_FIXED_DIM,
                                                    ft.Colors.ON_TERTIARY_FIXED_VARIANT,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label=(
                                                        "On tertiary fixed variant"
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ),
                                    showcase_section(
                                        "Surface add-ons",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                surface_sample_card(
                                                    "SURFACE_DIM",
                                                    ft.Colors.SURFACE_DIM,
                                                    ft.Colors.ON_SURFACE,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On surface",
                                                ),
                                                surface_sample_card(
                                                    "SURFACE_BRIGHT",
                                                    ft.Colors.SURFACE_BRIGHT,
                                                    ft.Colors.ON_SURFACE_VARIANT,
                                                    outline_label="",
                                                    outline_color=None,
                                                    text_label="On surface variant",
                                                ),
                                            ],
                                        ),
                                    ),
                                    showcase_section(
                                        "Effects",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                ft.Container(
                                                    width=300,
                                                    height=132,
                                                    bgcolor=ft.Colors.SURFACE_CONTAINER,
                                                    border_radius=16,
                                                    shadow=ft.BoxShadow(
                                                        spread_radius=4,
                                                        blur_radius=28,
                                                        color=ft.Colors.SHADOW,
                                                        offset=ft.Offset(0, 12),
                                                    ),
                                                    padding=16,
                                                    content=ft.Column(
                                                        spacing=8,
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                                        controls=[
                                                            ft.Text(
                                                                "Container with Shadow",
                                                                color=ft.Colors.ON_SURFACE,
                                                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                                            ),
                                                            ft.Text(
                                                                "Surface container, "
                                                                "Shadow",
                                                                color=ft.Colors.ON_SURFACE_VARIANT,
                                                                size=13,
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                                ft.Container(
                                                    width=300,
                                                    height=132,
                                                    bgcolor=ft.Colors.SCRIM,
                                                    border_radius=16,
                                                    padding=16,
                                                    content=ft.Column(
                                                        spacing=8,
                                                        alignment=ft.MainAxisAlignment.CENTER,
                                                        horizontal_alignment=ft.CrossAxisAlignment.START,
                                                        controls=[
                                                            ft.Text(
                                                                "SCRIM",
                                                                color=ft.Colors.ON_INVERSE_SURFACE,
                                                                theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                                            ),
                                                            ft.Text(
                                                                "On inverse surface",
                                                                color=ft.Colors.ON_INVERSE_SURFACE,
                                                                size=13,
                                                            ),
                                                        ],
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )
