import flet as ft

name = "Receiving scroll notifications"


def example():
    def on_column_scroll(e: ft.OnScrollEvent):
        notification = f"Type: {e.event_type}, pixels: {e.pixels}, min_scroll_extent: {e.min_scroll_extent}, max_scroll_extent: {e.max_scroll_extent}"
        notification_text.value = notification
        notification_text.update()

    cl = ft.Column(
        spacing=10,
        height=200,
        width=200,
        scroll=ft.ScrollMode.ALWAYS,
        on_scroll=on_column_scroll,
    )
    for i in range(0, 50):
        cl.controls.append(ft.Text(f"Text line {i}", scroll_key=str(i)))

    notification_text = ft.Text()

    return ft.Column([ft.Container(cl, border=ft.Border.all(1)), notification_text])
