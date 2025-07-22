import flet as ft

name = "Scrolling column programmatically"


def example():
    cl = ft.Column(
        spacing=10,
        height=200,
        # width=float("inf"),
        width=200,
        scroll=ft.ScrollMode.ALWAYS,
    )
    for i in range(0, 100):
        cl.controls.append(ft.Text(f"Text line {i}", scroll_key=str(i)))

    def scroll_to_offset(e):
        cl.scroll_to(offset=100, duration=1000)

    def scroll_to_start(e):
        cl.scroll_to(offset=0, duration=1000)

    def scroll_to_end(e):
        cl.scroll_to(offset=-1, duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT)

    # def scroll_to_key(e):
    #     cl.scroll_to(key="20", duration=1000)

    def scroll_to_delta(e):
        cl.scroll_to(delta=40, duration=200)

    def scroll_to_minus_delta(e):
        cl.scroll_to(delta=-40, duration=200)

    return ft.Column(
        [
            ft.Container(cl, border=ft.Border.all(1)),
            ft.ElevatedButton("Scroll to offset 100", on_click=scroll_to_offset),
            ft.Row(
                [
                    ft.ElevatedButton("Scroll to start", on_click=scroll_to_start),
                    ft.ElevatedButton("Scroll to end", on_click=scroll_to_end),
                ]
            ),
            # ft.ElevatedButton("Scroll to key '20'", on_click=scroll_to_key),
            ft.Row(
                [
                    ft.ElevatedButton("Scroll -40", on_click=scroll_to_minus_delta),
                    ft.ElevatedButton("Scroll +40", on_click=scroll_to_delta),
                ]
            ),
        ]
    )
