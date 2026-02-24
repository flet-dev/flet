import flet as ft
import flet_map as ftm


def main(page: ft.Page):
    page.padding = 16

    async def update_camera_status(trigger: str):
        camera = await my_map.get_camera()
        camera_status.value = (
            f"Camera [{trigger}]: "
            f"center=({camera.center.latitude:.5f}, {camera.center.longitude:.5f}), "
            f"zoom={camera.zoom:.2f}, rotation={camera.rotation:.1f}"
        )
        page.update()

    async def zoom_in(e: ft.Event[ft.Button]):
        await my_map.zoom_in()
        await update_camera_status("zoom_in")

    async def zoom_out(e: ft.Event[ft.Button]):
        await my_map.zoom_out()
        await update_camera_status("zoom_out")

    async def rotate_plus_15(e: ft.Event[ft.Button]):
        await my_map.rotate_from(15)
        await update_camera_status("rotate_from(+15)")

    async def reset_rotation(e: ft.Event[ft.Button]):
        await my_map.reset_rotation()
        await update_camera_status("reset_rotation")

    async def center_berlin(e: ft.Event[ft.Button]):
        await my_map.center_on(point=ftm.MapLatitudeLongitude(52.52, 13.405), zoom=12)
        await update_camera_status("center_on(berlin)")

    async def move_tokyo(e: ft.Event[ft.Button]):
        await my_map.move_to(
            destination=ftm.MapLatitudeLongitude(35.6762, 139.6503), zoom=11
        )
        await update_camera_status("move_to(tokyo)")

    async def set_world_zoom(e: ft.Event[ft.Button]):
        await my_map.zoom_to(3)
        await update_camera_status("zoom_to(3)")

    page.appbar = ft.AppBar(title="Camera controls")
    page.add(
        ft.Column(
            expand=True,
            controls=[
                ft.Text(
                    "Use buttons to control map camera programmatically.",
                    size=12,
                ),
                ft.Row(
                    wrap=True,
                    spacing=8,
                    run_spacing=8,
                    controls=[
                        ft.Button("Zoom in", on_click=zoom_in),
                        ft.Button("Zoom out", on_click=zoom_out),
                        ft.Button("Rotate +15°", on_click=rotate_plus_15),
                        ft.Button("Reset rotation", on_click=reset_rotation),
                        ft.Button("Center Berlin", on_click=center_berlin),
                        ft.Button("Move to Tokyo", on_click=move_tokyo),
                        ft.Button("World zoom (3)", on_click=set_world_zoom),
                    ],
                ),
                camera_status := ft.Text(selectable=True, font_family="monospace"),
                my_map := ftm.Map(
                    expand=True,
                    initial_center=ftm.MapLatitudeLongitude(52.52, 13.405),
                    initial_zoom=5,
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
                        ftm.MarkerLayer(
                            markers=[
                                ftm.Marker(
                                    coordinates=ftm.MapLatitudeLongitude(52.52, 13.405),
                                    content=ft.Icon(ft.Icons.LOCATION_ON),
                                ),
                                ftm.Marker(
                                    coordinates=ftm.MapLatitudeLongitude(
                                        35.6762, 139.6503
                                    ),
                                    content=ft.Icon(ft.Icons.LOCATION_ON),
                                ),
                            ]
                        ),
                    ],
                ),
            ],
        )
    )


ft.run(main)
