import random

import flet as ft
import flet_map as ftm


def main(page: ft.Page):
    def handle_tap(e: ftm.MapTapEvent):
        if e.name == "tap":
            marker_layer.markers.append(
                ftm.Marker(
                    content=ft.Icon(
                        ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED
                    ),
                    coordinates=e.coordinates,
                )
            )
        elif e.name == "secondary_tap":
            circle_layer.circles.append(
                ftm.CircleMarker(
                    radius=random.randint(5, 10),
                    coordinates=e.coordinates,
                    color=ft.Colors.random(),
                    border_color=ft.Colors.random(),
                    border_stroke_width=4,
                )
            )
        page.update()

    page.appbar = ft.AppBar(title="Multiple Layers")
    page.add(
        ft.Text("Click anywhere to add a Marker, right-click to add a CircleMarker."),
        ftm.Map(
            expand=True,
            initial_center=ftm.MapLatitudeLongitude(15, 10),
            initial_zoom=4.2,
            interaction_configuration=ftm.InteractionConfiguration(
                flags=ftm.InteractionFlag.ALL
            ),
            on_tap=handle_tap,
            on_secondary_tap=handle_tap,
            on_event=print,
            layers=[
                ftm.TileLayer(
                    url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    on_image_error=lambda e: print("TileLayer Error"),
                ),
                ftm.RichAttribution(
                    attributions=[
                        ftm.TextSourceAttribution(
                            text="OpenStreetMap Contributors",
                            on_click=lambda e: e.page.launch_url(
                                "https://www.openstreetmap.org/copyright"
                            ),
                        ),
                        ftm.TextSourceAttribution(
                            text="Flet",
                            on_click=lambda e: e.page.launch_url("https://flet.dev"),
                        ),
                    ]
                ),
                ftm.SimpleAttribution(
                    text="Flet",
                    alignment=ft.Alignment.TOP_RIGHT,
                    on_click=lambda e: print("Clicked SimpleAttribution"),
                ),
                marker_layer := ftm.MarkerLayer(
                    markers=[
                        ftm.Marker(
                            content=ft.Icon(ft.Icons.LOCATION_ON),
                            coordinates=ftm.MapLatitudeLongitude(30, 15),
                        ),
                        ftm.Marker(
                            content=ft.Icon(ft.Icons.LOCATION_ON),
                            coordinates=ftm.MapLatitudeLongitude(10, 10),
                        ),
                        ftm.Marker(
                            content=ft.Icon(ft.Icons.LOCATION_ON),
                            coordinates=ftm.MapLatitudeLongitude(25, 45),
                        ),
                    ],
                ),
                circle_layer := ftm.CircleLayer(
                    circles=[
                        ftm.CircleMarker(
                            radius=10,
                            coordinates=ftm.MapLatitudeLongitude(16, 24),
                            color=ft.Colors.RED,
                            border_color=ft.Colors.BLUE,
                            border_stroke_width=4,
                        ),
                    ],
                ),
                ftm.PolygonLayer(
                    polygons=[
                        ftm.PolygonMarker(
                            label="Popular Touristic Area",
                            label_text_style=ft.TextStyle(
                                color=ft.Colors.BLACK,
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                            color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE),
                            coordinates=[
                                ftm.MapLatitudeLongitude(10, 10),
                                ftm.MapLatitudeLongitude(30, 15),
                                ftm.MapLatitudeLongitude(25, 45),
                            ],
                        ),
                    ],
                ),
                ftm.PolylineLayer(
                    polylines=[
                        ftm.PolylineMarker(
                            border_stroke_width=3,
                            border_color=ft.Colors.RED,
                            gradient_colors=[ft.Colors.BLACK, ft.Colors.BLACK],
                            color=ft.Colors.with_opacity(0.6, ft.Colors.GREEN),
                            coordinates=[
                                ftm.MapLatitudeLongitude(10, 10),
                                ftm.MapLatitudeLongitude(30, 15),
                                ftm.MapLatitudeLongitude(25, 45),
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )


ft.run(main)
