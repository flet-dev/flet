import flet as ft
import flet_map as ftm

IDLE_EVENT_TYPES = {
    ftm.MapEventType.MOVE_END,
    ftm.MapEventType.FLING_ANIMATION_END,
    ftm.MapEventType.FLING_ANIMATION_NOT_STARTED,
    ftm.MapEventType.DOUBLE_TAP_ZOOM_END,
    ftm.MapEventType.ROTATE_END,
}


def main(page: ft.Page):
    page.padding = 16

    async def handle_map_event(e: ftm.MapEvent):
        last_event.value = (
            "Last event: "
            f"type={e.event_type}, source={e.source.value}, zoom={e.camera.zoom:.2f}"
        )

        if e.event_type in IDLE_EVENT_TYPES:  # here the camera is settled/idle
            camera = await e.control.get_camera()
            settled_camera.value = (
                "Settled camera: "
                f"center=({camera.center.latitude:.3f}, "
                f"{camera.center.longitude:.3f}), "
                f"zoom={camera.zoom:.2f}, rotation={camera.rotation:.1f}, "
                f"trigger={e.event_type}"
            )

        page.update()

    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Text("Camera idle pattern", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Drag, fling, rotate, zoom and watch when the camera is settled.",
                    size=12,
                ),
                last_event := ft.Text(
                    "Last event: -", selectable=True, font_family="monospace"
                ),
                settled_camera := ft.Text(
                    "Settled camera: -", selectable=True, font_family="monospace"
                ),
                ftm.Map(
                    expand=True,
                    initial_center=ftm.MapLatitudeLongitude(
                        latitude=52.52, longitude=13.405
                    ),
                    initial_zoom=11,
                    on_event=handle_map_event,
                    interaction_configuration=ftm.InteractionConfiguration(
                        flags=ftm.InteractionFlag.ALL
                    ),
                    layers=[
                        ftm.TileLayer(
                            url_template="https://tile.memomaps.de/tilegen/{z}/{x}/{y}.png"
                        ),
                        ftm.SimpleAttribution(
                            text="OpenStreetMap contributors",
                            on_click=lambda e: e.page.launch_url(
                                "https://www.openstreetmap.org/copyright"
                            ),
                        ),
                    ],
                ),
            ],
        )
    )


ft.run(main)
