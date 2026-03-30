import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    counts = {direction: 0 for direction in ft.ScrollDirection}
    count_labels = {
        direction: ft.Text(f"{direction.name}: 0") for direction in ft.ScrollDirection
    }

    def on_scroll(e: ft.OnScrollEvent):
        if e.event_type == ft.ScrollType.USER and e.direction is not None:
            counts[e.direction] += 1
            count_labels[
                e.direction
            ].value = f"{e.direction.name}: {counts[e.direction]}"
            last.value = f"Last USER direction: {e.direction.name}"
            for label in count_labels.values():
                label.update()
            last.update()

    page.appbar = ft.AppBar(title="ScrollDirection Showcase")
    page.add(
        ft.Text("Scroll the list and watch USER direction notifications."),
        last := ft.Text("Last USER direction: none"),
        ft.Row(
            wrap=True,
            spacing=10,
            controls=[count_labels[d] for d in ft.ScrollDirection],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Container(
            width=360,
            height=240,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=8,
            padding=8,
            content=ft.Column(
                scroll=ft.ScrollMode.ALWAYS,
                on_scroll=on_scroll,
                controls=[ft.Text(f"Scrollable item {i + 1}") for i in range(60)],
            ),
        ),
    )


ft.run(main)
