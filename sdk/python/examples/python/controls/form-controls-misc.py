import flet as ft


def main(page: ft.Page):
    page.title = "Form Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = ft.Padding.all(20)

    results = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=100)

    checkboxes = ft.Column(
        controls=[
            ft.Checkbox(value=True),
            ft.Checkbox(label="A simple checkbox with a label"),
            ft.Checkbox(label="Checkbox with tristate", tristate=True),
            ft.Checkbox(label="Disabled checkbox", disabled=True),
            ft.Checkbox(
                label="Label on the left", label_position=ft.LabelPosition.LEFT
            ),
        ]
    )

    switches = ft.Column(
        controls=[
            ft.Switch(value=True),
            ft.Switch(value=False),
            ft.Switch(label="Switch with a label"),
            ft.Switch(label="Disabled switch", disabled=True),
            ft.Switch(label="Label on the left", label_position=ft.LabelPosition.LEFT),
        ]
    )

    radio_group1 = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.Radio(value="red", label="Red color"),
                ft.Radio(value="green", label="Green color"),
                ft.Radio(value="blue", label="Blue color"),
            ]
        )
    )

    def handle_rg2_change(e: ft.Event[ft.RadioGroup]):
        results.controls.append(ft.Text(f"Selected value: {e.data}"))
        page.update()

    radio_group2 = ft.RadioGroup(
        value="two",
        on_change=handle_rg2_change,
        content=ft.Row(
            controls=[
                ft.Radio(value="one", label="One"),
                ft.Radio(value="two", label="Two"),
                ft.Radio(value="three", label="Three"),
            ]
        ),
    )

    dd = ft.Dropdown(
        value="b",
        content_padding=ft.Padding.all(5),
        height=35,
        options=[
            ft.dropdown.Option("a", "Item A"),
            ft.dropdown.Option("b", "Item B"),
            ft.dropdown.Option("c", "Item C"),
        ],
    )

    dd1 = ft.Dropdown(
        options=[
            ft.dropdown.Option("r", "Red"),
            ft.dropdown.Option("g", "Green"),
            ft.dropdown.Option("b", "Blue"),
        ]
    )
    dd2 = ft.DropdownM2(
        label="My favorite number",
        icon=ft.Icons.FORMAT_SIZE,
        hint_text="Choose your favorite color",
        helper="You can choose only one color",
        counter="0 colors selected",
        prefix_icon=ft.Icons.COLOR_LENS,
        suffix="...is your color",
        options=[
            ft.dropdownm2.Option("1", "One"),
            ft.dropdownm2.Option("2", "Two"),
            ft.dropdownm2.Option("3", "Three"),
        ],
    )

    page.add(
        ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            expand=1,
            controls=[
                ft.Text("Checkboxes", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                checkboxes,
                ft.Text("Switches", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                switches,
                ft.Text("Radio", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                radio_group1,
                ft.Text(
                    value="Radio with on_change",
                    theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                ),
                radio_group2,
                ft.Container(
                    content=results,
                    padding=10,
                    border=ft.border.all(1, "black12"),
                    border_radius=ft.border_radius.all(10),
                    bgcolor="black12",
                ),
                ft.Text(
                    value="Dropdown with pre-selected value",
                    theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                ),
                dd,
                ft.Text("Dropdown", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                dd1,
                ft.Text(
                    value="Dropdown with all decoration",
                    theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                ),
                dd2,
                ft.Text("Slider", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                ft.Slider(value=0.5),
                ft.Slider(min=0, max=100, divisions=10, value=30, label="{value}%"),
            ],
        ),
    )


ft.run(main)
