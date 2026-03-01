import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    counts = {event_type: 0 for event_type in ft.ScrollType}
    count_labels = {
        event_type: ft.Text(f"{event_type.name}: 0") for event_type in ft.ScrollType
    }

    def on_scroll(e: ft.OnScrollEvent):
        counts[e.event_type] += 1
        count_labels[
            e.event_type
        ].value = f"{e.event_type.name}: {counts[e.event_type]}"
        last.value = (
            f"Last event: {e.event_type.name}, pixels={round(e.pixels, 1)}"
            f"{', direction=' if e.direction else ''}"
        )
        for label in count_labels.values():
            label.update()
        last.update()

    page.appbar = ft.AppBar(title="ScrollType Showcase")
    page.add(
        ft.Text("Scroll the list to generate start/update/user/end notifications."),
        last := ft.Text(),
        ft.Row(
            wrap=True,
            spacing=10,
            controls=[count_labels[t] for t in ft.ScrollType],
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
