import flet as ft
import flet_map as ftm

IMAGE_URL = (
    "https://images.pexels.com/photos/231009/pexels-photo-231009.jpeg"
    "?auto=compress&cs=tinysrgb&dpr=2&h=300&w=600"
)


def label(text: str, color: ft.ColorValue) -> ft.Container:
    return ft.Container(
        width=32,
        height=32,
        bgcolor=color,
        border_radius=16,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(text, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
    )


def main(page: ft.Page):
    page.appbar = ft.AppBar(title="Overlay Images")
    page.add(
        ft.SafeArea(
            expand=True,
            content=ftm.Map(
                expand=True,
                initial_center=ftm.MapLatitudeLongitude(51.5, -0.09),
                initial_zoom=6,
                layers=[
                    ftm.TileLayer(
                        url_template="https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                        user_agent_package_name="Flet Overlay Images Example",
                    ),
                    ftm.OverlayImageLayer(
                        overlay_images=[
                            ftm.OverlayImage(
                                src=IMAGE_URL,
                                bounds=ftm.MapLatitudeLongitudeBounds(
                                    corner_1=ftm.MapLatitudeLongitude(51.5, -0.09),
                                    corner_2=ftm.MapLatitudeLongitude(48.8566, 2.3522),
                                ),
                                opacity=0.8,
                            ),
                            ftm.RotatedOverlayImage(
                                src=IMAGE_URL,
                                top_left_corner=ftm.MapLatitudeLongitude(
                                    53.377, -2.999
                                ),
                                bottom_left_corner=ftm.MapLatitudeLongitude(
                                    52.503, -1.868
                                ),
                                bottom_right_corner=ftm.MapLatitudeLongitude(
                                    53.475, 0.275
                                ),
                                opacity=0.8,
                            ),
                        ]
                    ),
                    ftm.MarkerLayer(
                        markers=[
                            ftm.Marker(
                                content=label("TL", ft.Colors.RED_ACCENT),
                                coordinates=ftm.MapLatitudeLongitude(53.377, -2.999),
                            ),
                            ftm.Marker(
                                content=label("BL", ft.Colors.RED_ACCENT),
                                coordinates=ftm.MapLatitudeLongitude(52.503, -1.868),
                            ),
                            ftm.Marker(
                                content=label("BR", ft.Colors.RED_ACCENT),
                                coordinates=ftm.MapLatitudeLongitude(53.475, 0.275),
                            ),
                        ]
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
