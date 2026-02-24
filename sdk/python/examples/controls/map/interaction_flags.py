import flet as ft
import flet_map as ftm

FLAG_OPTIONS: list[tuple[str, ftm.InteractionFlag]] = [
    ("Drag", ftm.InteractionFlag.DRAG),
    ("Fling animation", ftm.InteractionFlag.FLING_ANIMATION),
    ("Pinch move", ftm.InteractionFlag.PINCH_MOVE),
    ("Pinch zoom", ftm.InteractionFlag.PINCH_ZOOM),
    ("Double tap zoom", ftm.InteractionFlag.DOUBLE_TAP_ZOOM),
    ("Double tap drag zoom", ftm.InteractionFlag.DOUBLE_TAP_DRAG_ZOOM),
    ("Scroll wheel zoom", ftm.InteractionFlag.SCROLL_WHEEL_ZOOM),
    ("Rotate", ftm.InteractionFlag.ROTATE),
]


def main(page: ft.Page):
    page.padding = 16

    def get_selected_flags() -> ftm.InteractionFlag:
        flags = ftm.InteractionFlag.NONE
        for checkbox in checkboxes:
            if checkbox.value:
                flags |= checkbox.data
        return flags

    def update_interaction_flags(e: ft.Event[ft.Checkbox] = None):
        flags = get_selected_flags()
        my_map.interaction_configuration = ftm.InteractionConfiguration(flags=flags)
        page.update()

    def handle_map_event(e: ftm.MapEvent):
        event_type = e.event_type.value if e.event_type else "-"
        last_event.value = (
            "Last event: "
            f"type={event_type}, source={e.source.value}, zoom={e.camera.zoom:.2f}"
        )
        page.update()

    checkboxes = [
        ft.Checkbox(
            label=label,
            value=True,
            data=flag,
            on_change=update_interaction_flags,
        )
        for label, flag in FLAG_OPTIONS
    ]

    my_map = ftm.Map(
        expand=True,
        initial_center=ftm.MapLatitudeLongitude(latitude=52.52, longitude=13.405),
        initial_zoom=11,
        on_event=handle_map_event,
        interaction_configuration=ftm.InteractionConfiguration(
            flags=ftm.InteractionFlag.ALL
        ),
        layers=[
            ftm.TileLayer(
                url_template="https://tile.memomaps.de/tilegen/{z}/{x}/{y}.png",
                on_image_error=lambda e: print(f"TileLayer Error: {e.data}"),
            ),
            ftm.RichAttribution(
                attributions=[
                    ftm.TextSourceAttribution(
                        text="OpenStreetMap contributors",
                        on_click=lambda e: e.page.launch_url(
                            "https://www.openstreetmap.org/copyright"
                        ),
                    )
                ]
            ),
        ],
    )

    page.appbar = ft.AppBar(title="Interaction flags")
    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Text(
                    "Toggle flags and try dragging, zooming, rotating, and scrolling.",
                    size=12,
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(col={"sm": 6, "md": 4}, content=c)
                        for c in checkboxes
                    ]
                ),
                last_event := ft.Text(
                    "Last event: -", selectable=True, font_family="monospace"
                ),
                ft.Container(expand=True, content=my_map),
            ],
        )
    )

    update_interaction_flags()


ft.run(main)
