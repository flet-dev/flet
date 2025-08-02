import flet as ft

name = "Controlling scroll position for Column"


def example():
    cl = ft.Column(
        spacing=10,
        height=180,
        width=300,
        scroll=ft.ScrollMode.ALWAYS,
        controls=[
            ft.Container(
                ft.Text("Section A"),
                alignment=ft.Alignment.TOP_LEFT,
                bgcolor=ft.Colors.YELLOW_200,
                height=100,
                scroll_key="A",
            ),
            ft.Container(
                ft.Text("Section B"),
                alignment=ft.Alignment.TOP_LEFT,
                bgcolor=ft.Colors.GREEN_200,
                height=100,
                scroll_key="B",
            ),
            ft.Container(
                ft.Text("Section C"),
                alignment=ft.Alignment.TOP_LEFT,
                bgcolor=ft.Colors.BLUE_200,
                height=100,
                scroll_key="C",
            ),
            ft.Container(
                ft.Text("Section D"),
                alignment=ft.Alignment.TOP_LEFT,
                bgcolor=ft.Colors.PINK_200,
                height=100,
                scroll_key="D",
            ),
        ],
    )

    def scroll_to_a(_):
        cl.scroll_to(key="A", duration=1000)

    def scroll_to_b(_):
        cl.scroll_to(key="B", duration=1000)

    def scroll_to_c(_):
        cl.scroll_to(key="C", duration=1000)

    def scroll_to_d(_):
        cl.scroll_to(key="D", duration=1000)

    return ft.Column(
        [
            ft.Container(cl, border=ft.Border.all(1)),
            ft.Column(
                [
                    ft.Text("Scroll to:"),
                    ft.Row(
                        [
                            ft.ElevatedButton(
                                "Section A",
                                on_click=scroll_to_a,
                            ),
                            ft.ElevatedButton(
                                "Section B",
                                on_click=scroll_to_b,
                            ),
                            ft.ElevatedButton(
                                "Section C",
                                on_click=scroll_to_c,
                            ),
                            ft.ElevatedButton(
                                "Section D",
                                on_click=scroll_to_d,
                            ),
                        ]
                    ),
                ]
            ),
        ]
    )
