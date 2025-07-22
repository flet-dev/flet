import flet as ft
from components.properties_table import PropertiesList

name = "Text with variable properties"


def example():
    t = ft.Text(
        value="This is a sample text",
        italic=True,
        selectable=True,
        text_align=ft.TextAlign.CENTER,
        badge=ft.Badge(label="Badge on the Text"),
        spans=[
            ft.TextSpan(text="Span1", style=ft.TextStyle(size=30)),
            ft.TextSpan(
                text="Span2",
                style=ft.TextStyle(size=30),
            ),
        ],
        size=20,
        color=ft.Colors.GREEN_800,
        bgcolor=ft.Colors.GREEN_100,
        max_lines=2,
        tooltip=ft.Tooltip("Tooltip"),
        style=ft.TextStyle(
            size=30,
            shadow=[
                # ft.BoxShadow(spread_radius=5, blur_radius=10, color=ft.Colors.ORANGE)
            ],
            foreground=ft.Paint(
                color=ft.Colors.BLUE_400, blend_mode=ft.BlendMode.COLOR_BURN
            ),
        ),
    )

    paint_properties_list = [
        {
            "name": "color",
            "value_type": "enum",
            "values": ft.Colors,
            "description": "Description.",
        },
    ]

    shadow_properties_list = [
        {
            "name": "spread_radius",
            "value_type": "number",
            "min": 0,
            "max": 100,
            "description": "Description.",
        },
        {
            "name": "blur_radius",
            "value_type": "number",
            "min": 0,
            "max": 100,
            "description": "Description.",
        },
        {
            "name": "color",
            "value_type": "enum",
            "values": ft.Colors,
            "description": "Description.",
        },
    ]

    style_properties_list = [
        {
            "name": "size",
            "value_type": "number",
            "min": 0,
            "max": 100,
            "description": "Description.",
        },
        {
            "name": "letter_spacing",
            "value_type": "number",
            "min": 0,
            "max": 100,
            "description": "Description.",
        },
        {
            "name": "foreground",
            "value_type": "dataclass",
            "dataclass": ft.Paint,
            "properties": paint_properties_list,
            "description": "Description.",
        },
        {
            "name": "shadow",
            "value_type": "list",
            "dataclass": ft.BoxShadow,
            "properties": shadow_properties_list,
            "description": "Description.",
        },
    ]

    span_properties_list = [
        {"name": "text", "value_type": "str", "description": "Description."},
        {
            "name": "style",
            "value_type": "dataclass",
            "dataclass": ft.TextStyle,
            "properties": style_properties_list,
            "description": "Description.",
        },
    ]

    badge_properties_list = [
        {
            "name": "label",
            "value_type": "str",
            "description": "Description.",
        },
        {
            "name": "bgcolor",
            "value_type": "enum",
            "values": ft.Colors,
            "description": "Description.",
        },
    ]

    properties_list = [
        {
            "name": "value",
            "value_type": "str",
            "description": "The text displayed.",
        },
        {
            "name": "italic",
            "value_type": "bool",
            "description": "True to use italic typeface.",
        },
        {
            "name": "selectable",
            "value_type": "bool",
            "description": "Whether the text should be selectable.",
        },
        {
            "name": "size",
            "value_type": "number",
            "min": 0,
            "max": 100,
            "description": "Text size in virtual pixels.",
        },
        {
            "name": "color",
            "value_type": "enum",
            "values": ft.Colors,
            "description": "Text foreground color. If style foreground color property is specified, it overrides this color.",
        },
        {
            "name": "bgcolor",
            "value_type": "enum",
            "values": ft.Colors,
            "description": "Text background color.",
        },
        {
            "name": "text_align",
            "value_type": "enum",
            "values": ft.TextAlign,
            "description": "Text horizontal align.",
        },
        {
            "name": "max_lines",
            "value_type": "number",
            "min": 0,
            "max": 100,
            "description": "An optional maximum number of lines for the text to span, wrapping if necessary. If the text exceeds the given number of lines, it will be truncated according to overflow.",
        },
        {
            "name": "style",
            "value_type": "dataclass",
            "dataclass": ft.TextStyle,
            "properties": style_properties_list,
            "description": "The text's style.",
        },
        {
            "name": "badge",
            "value_type": "dataclass",
            "dataclass": ft.Badge,
            "properties": badge_properties_list,
            "description": "Badges are used to show notifications, counts, or status information about its control.",
        },
        {
            "name": "spans",
            "value_type": "list",
            "dataclass": ft.TextSpan,
            "properties": span_properties_list,
            "description": "The list of TextSpan objects to build a rich text paragraph.",
        },
    ]

    # properties = PropertiesTable(properties_list, t)

    properties = PropertiesList(properties=properties_list, control=t)

    # source_code = ft.Text(value=get_source_code(), selectable=True)
    # source_code = properties.source_code

    # source_code = SourceCode(t)

    example_control = ft.Column(
        controls=[
            t,
            ft.Column(expand=True, scroll=ft.ScrollMode.AUTO, controls=[properties]),
            ft.Text("Source code:", weight=ft.FontWeight.BOLD),
            # source_code,
        ],
    )

    return example_control
