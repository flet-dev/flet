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
                    theme=ft.Theme(),
                    dark_theme=ft.Theme(),
                    theme_mode=ft.ThemeMode.SYSTEM,
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
                    color_band(
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
    group_theme: ft.Theme,
    group_dark_theme: ft.Theme,
    group_theme_mode: ft.ThemeMode,
    get_role_value,
    format_role_value,
    on_color_click,
    on_tab_change,
    on_select_seed,
    on_export,
    on_import,
) -> list[ft.Control]:
    active_tab = role_tabs[selected_tab_index]
    return [
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
            ft.Container(
                theme=group_theme,
                dark_theme=group_dark_theme,
                theme_mode=group_theme_mode,
                content=color_group(
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
                    selected_label=selected_label,
                    on_color_click=on_color_click,
                ),
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


def build_time_picker_row(
    open_preview_time_picker, preview_time_text: ft.Text
) -> ft.Row:
    return ft.Row(
        spacing=12,
        controls=[
            ft.Button(
                "Pick time",
                icon=ft.Icons.SCHEDULE,
                on_click=open_preview_time_picker,
            ),
            preview_time_text,
        ],
    )


def build_error_examples() -> list[ft.Control]:
    password_field = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        value="hunter2",
    )
    password_field.error_text = "Incorrect password"
    return [
        password_field,
        ft.Text("Please correct the highlighted fields.", color=ft.Colors.ERROR),
    ]


def build_preview_tabs(
    *,
    preview_heading: str,
    preview_body: str,
    preview_time_text: ft.Text,
    theme_mode: ft.ThemeMode,
    on_toggle_theme,
    open_preview_time_picker,
) -> ft.Tabs:
    return ft.Tabs(
        selected_index=0,
        length=5,
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=12,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("Example", color=ft.Colors.ON_SURFACE),
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
                ft.TabBar(
                    tabs=[
                        ft.Tab(label="All"),
                        ft.Tab(label="Primary"),
                        ft.Tab(label="Secondary"),
                        ft.Tab(label="Tertiary"),
                        ft.Tab(label="Error"),
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
                                    showcase_section(
                                        "Palette together",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                preview_role_block(
                                                    "PRIMARY",
                                                    ft.Colors.PRIMARY,
                                                    ft.Colors.ON_PRIMARY,
                                                ),
                                                preview_role_block(
                                                    "SECONDARY",
                                                    ft.Colors.SECONDARY,
                                                    ft.Colors.ON_SECONDARY,
                                                ),
                                                preview_role_block(
                                                    "TERTIARY",
                                                    ft.Colors.TERTIARY,
                                                    ft.Colors.ON_TERTIARY,
                                                ),
                                                preview_role_block(
                                                    "ERROR",
                                                    ft.Colors.ERROR,
                                                    ft.Colors.ON_ERROR,
                                                ),
                                            ],
                                        ),
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                ft.FilledButton("Apply"),
                                                ft.FilledTonalButton("Tonal"),
                                                ft.OutlinedButton("Outline"),
                                            ],
                                        ),
                                        build_selected_chip_row(),
                                    ),
                                    showcase_section(
                                        "Error states",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                preview_role_block(
                                                    "ERROR_CONTAINER",
                                                    ft.Colors.ERROR_CONTAINER,
                                                    ft.Colors.ON_ERROR_CONTAINER,
                                                )
                                            ],
                                        ),
                                        *build_error_examples(),
                                    ),
                                    showcase_section(
                                        "Selection",
                                        build_selection_row(),
                                        ft.Slider(value=70, min=0, max=100),
                                    ),
                                    showcase_section(
                                        "Card",
                                        ft.Card(
                                            content=ft.Container(
                                                padding=16,
                                                content=ft.Column(
                                                    spacing=12,
                                                    controls=[
                                                        ft.Row(
                                                            spacing=12,
                                                            controls=[
                                                                ft.Icon(
                                                                    ft.Icons.COLOR_LENS
                                                                ),
                                                                ft.Text(
                                                                    preview_heading,
                                                                    theme_style=ft.TextThemeStyle.TITLE_MEDIUM,
                                                                ),
                                                            ],
                                                        ),
                                                        ft.Text(preview_body),
                                                        ft.Row(
                                                            spacing=12,
                                                            controls=[
                                                                ft.FilledButton(
                                                                    "Apply"
                                                                ),
                                                                ft.TextButton("Reset"),
                                                            ],
                                                        ),
                                                    ],
                                                ),
                                            ),
                                        ),
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
                                        "Primary roles",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                preview_role_block(
                                                    "PRIMARY",
                                                    ft.Colors.PRIMARY,
                                                    ft.Colors.ON_PRIMARY,
                                                ),
                                                preview_role_block(
                                                    "PRIMARY_CONTAINER",
                                                    ft.Colors.PRIMARY_CONTAINER,
                                                    ft.Colors.ON_PRIMARY_CONTAINER,
                                                ),
                                            ],
                                        ),
                                        build_primary_button_row(),
                                        ft.FloatingActionButton(icon=ft.Icons.PALETTE),
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
                                        "Secondary roles",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                preview_role_block(
                                                    "SECONDARY",
                                                    ft.Colors.SECONDARY,
                                                    ft.Colors.ON_SECONDARY,
                                                ),
                                                preview_role_block(
                                                    "SECONDARY_CONTAINER",
                                                    ft.Colors.SECONDARY_CONTAINER,
                                                    ft.Colors.ON_SECONDARY_CONTAINER,
                                                ),
                                            ],
                                        ),
                                        build_tonal_button(),
                                        build_preview_chip_row(),
                                        build_segmented_button(),
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
                                        "Tertiary roles",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                preview_role_block(
                                                    "TERTIARY",
                                                    ft.Colors.TERTIARY,
                                                    ft.Colors.ON_TERTIARY,
                                                ),
                                                preview_role_block(
                                                    "TERTIARY_CONTAINER",
                                                    ft.Colors.TERTIARY_CONTAINER,
                                                    ft.Colors.ON_TERTIARY_CONTAINER,
                                                ),
                                            ],
                                        ),
                                        build_time_picker_row(
                                            open_preview_time_picker, preview_time_text
                                        ),
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
                                        "Error roles",
                                        ft.Row(
                                            wrap=True,
                                            spacing=12,
                                            run_spacing=12,
                                            controls=[
                                                preview_role_block(
                                                    "ERROR",
                                                    ft.Colors.ERROR,
                                                    ft.Colors.ON_ERROR,
                                                ),
                                                preview_role_block(
                                                    "ERROR_CONTAINER",
                                                    ft.Colors.ERROR_CONTAINER,
                                                    ft.Colors.ON_ERROR_CONTAINER,
                                                ),
                                            ],
                                        ),
                                        *build_error_examples(),
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
            ],
        ),
    )
