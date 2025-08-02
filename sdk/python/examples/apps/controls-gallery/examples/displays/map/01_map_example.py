import flet as ft

# import flet.map as map

name = "Map example"


def example():
    # marker_layer_ref = ft.Ref[map.MarkerLayer]()
    # circle_layer_ref = ft.Ref[map.CircleLayer]()

    # def handle_tap(e: map.MapTapEvent):
    #     print(
    #         f"Name: {e.name} - coordinates: {e.coordinates} - Local: ({e.local_x}, {e.local_y}) - Global: ({e.global_x}, {e.global_y})"
    #     )
    #     if e.name == "tap":
    #         marker_layer_ref.current.markers.append(
    #             map.Marker(
    #                 content=ft.Icon(
    #                     ft.Icons.LOCATION_ON, color=ft.CupertinoColors.DESTRUCTIVE_RED
    #                 ),
    #                 coordinates=e.coordinates,
    #             )
    #         )
    #     elif e.name == "secondary_tap":
    #         circle_layer_ref.current.circles.append(
    #             map.CircleMarker(
    #                 radius=random.randint(5, 10),
    #                 coordinates=e.coordinates,
    #                 color=ft.Colors.random_color(),
    #                 border_color=ft.Colors.random_color(),
    #                 border_stroke_width=4,
    #             )
    #         )
    #     e.control.page.update()

    # def handle_event(e: map.MapEvent):
    #     print(
    #         f"{e.name} - Source: {e.source} - Center: {e.center} - Zoom: {e.zoom} - Rotation: {e.rotation}"
    #     )

    # return ft.Column(
    #     [
    #         ft.Text(
    #             "Click anywhere to add a Marker, right-click to add a CircleMarker."
    #         ),
    #         map.Map(
    #             expand=True,
    #             configuration=map.MapConfiguration(
    #                 initial_center=map.MapLatitudeLongitude(15, 10),
    #                 initial_zoom=4.2,
    #                 interaction_configuration=map.MapInteractionConfiguration(
    #                     flags=map.MapInteractiveFlag.ALL
    #                 ),
    #                 on_init=lambda e: print(f"Initialized Map"),
    #                 on_tap=handle_tap,
    #                 on_secondary_tap=handle_tap,
    #                 on_long_press=handle_tap,
    #                 on_event=handle_event,
    #             ),
    #             layers=[
    #                 map.TileLayer(
    #                     url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    #                     on_image_error=lambda e: print("TileLayer Error"),
    #                 ),
    #                 map.RichAttribution(
    #                     attributions=[
    #                         map.TextSourceAttribution(
    #                             text="OpenStreetMap Contributors",
    #                             on_click=lambda e: e.page.launch_url(
    #                                 "https://openstreetmap.org/copyright"
    #                             ),
    #                         ),
    #                         map.TextSourceAttribution(
    #                             text="Flet",
    #                             on_click=lambda e: e.page.launch_url(
    #                                 "https://flet.dev"
    #                             ),
    #                         ),
    #                     ]
    #                 ),
    #                 map.SimpleAttribution(
    #                     text="Flet",
    #                     alignment=ft.alignment.top_right,
    #                     on_click=lambda e: print("Clicked SimpleAttribution"),
    #                 ),
    #                 map.MarkerLayer(
    #                     ref=marker_layer_ref,
    #                     markers=[
    #                         map.Marker(
    #                             content=ft.Icon(ft.Icons.LOCATION_ON),
    #                             coordinates=map.MapLatitudeLongitude(30, 15),
    #                         ),
    #                         map.Marker(
    #                             content=ft.Icon(ft.Icons.LOCATION_ON),
    #                             coordinates=map.MapLatitudeLongitude(10, 10),
    #                         ),
    #                         map.Marker(
    #                             content=ft.Icon(ft.Icons.LOCATION_ON),
    #                             coordinates=map.MapLatitudeLongitude(25, 45),
    #                         ),
    #                     ],
    #                 ),
    #                 map.CircleLayer(
    #                     ref=circle_layer_ref,
    #                     circles=[
    #                         map.CircleMarker(
    #                             radius=10,
    #                             coordinates=map.MapLatitudeLongitude(16, 24),
    #                             color=ft.Colors.RED,
    #                             border_color=ft.Colors.BLUE,
    #                             border_stroke_width=4,
    #                         ),
    #                     ],
    #                 ),
    #                 map.PolygonLayer(
    #                     polygons=[
    #                         map.PolygonMarker(
    #                             label="Popular Touristic Area",
    #                             label_text_style=ft.TextStyle(
    #                                 color=ft.Colors.BLACK,
    #                                 size=15,
    #                                 weight=ft.FontWeight.BOLD,
    #                             ),
    #                             color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE),
    #                             coordinates=[
    #                                 map.MapLatitudeLongitude(10, 10),
    #                                 map.MapLatitudeLongitude(30, 15),
    #                                 map.MapLatitudeLongitude(25, 45),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #                 map.PolylineLayer(
    #                     polylines=[
    #                         map.PolylineMarker(
    #                             border_stroke_width=3,
    #                             border_color=ft.Colors.RED,
    #                             gradient_colors=[ft.Colors.BLACK, ft.Colors.BLACK],
    #                             color=ft.Colors.with_opacity(0.6, ft.Colors.GREEN),
    #                             coordinates=[
    #                                 map.MapLatitudeLongitude(10, 10),
    #                                 map.MapLatitudeLongitude(30, 15),
    #                                 map.MapLatitudeLongitude(25, 45),
    #                             ],
    #                         ),
    #                     ],
    #                 ),
    #             ],
    #         ),
    #     ],
    #     height=400,
    #     expand=True,
    # )
    return ft.Column([ft.Text("This example is under construction.")])
