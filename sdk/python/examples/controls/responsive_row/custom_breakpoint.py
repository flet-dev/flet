import flet as ft


def main(page: ft.Page):
    page.title = "ResponsiveRow with custom breakpoints"
    page.padding = 16

    breakpoints = {
        "phone": 0,
        "tablet": 640,
        "desktop": 1000,
    }

    sorted_breakpoints = sorted(breakpoints.items(), key=lambda item: item[1])

    breakpoint_labels = {
        name: ft.Text(f"{name}: \u2265 {value}px", weight=ft.FontWeight.W_500)
        for name, value in sorted_breakpoints
    }

    width_label = ft.Text()
    breakpoint_label = ft.Text()

    def update_status(_=None):
        width = (
            (page.window.width if page.window and page.window.width else None)
            or page.width
            or 0
        )
        width_label.value = f"Page width: {width:.0f}px"
        active_breakpoint = max(
            (bp for bp, min_width in breakpoints.items() if width >= min_width),
            key=lambda bp: breakpoints[bp],
            default="phone",
        )
        breakpoint_label.value = f"Active breakpoint: {active_breakpoint}"
        for name, label in breakpoint_labels.items():
            is_active = name == active_breakpoint
            label.color = ft.Colors.BLUE_700 if is_active else None
            label.weight = ft.FontWeight.W_700 if is_active else ft.FontWeight.W_400
            label.update()
        width_label.update()
        breakpoint_label.update()

    page.on_resize = update_status

    page.add(
        ft.Text("Resize the window to see custom breakpoints in action."),
        ft.Text("Cards switch column spans at phone, tablet, and desktop widths."),
        ft.Column(
            [
                ft.Text(
                    "Custom breakpoints (min widths):",
                    weight=ft.FontWeight.W_600,
                ),
                ft.Column(list(breakpoint_labels.values()), spacing=2),
            ],
            spacing=6,
        ),
        ft.ResponsiveRow(
            breakpoints=breakpoints,
            columns={"phone": 4, "tablet": 8, "desktop": 12},
            spacing=10,
            run_spacing=10,
            controls=[
                ft.Container(
                    content=ft.Text("Card 1", size=16, weight=ft.FontWeight.W_600),
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.AMBER_200,
                    height=90,
                    col={"phone": 4, "tablet": 4, "desktop": 3},
                ),
                ft.Container(
                    content=ft.Text("Card 2", size=16, weight=ft.FontWeight.W_600),
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.GREEN_200,
                    height=90,
                    col={"phone": 4, "tablet": 4, "desktop": 3},
                ),
                ft.Container(
                    content=ft.Text("Card 3", size=16, weight=ft.FontWeight.W_600),
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.BLUE_200,
                    height=90,
                    col={"phone": 4, "tablet": 4, "desktop": 3},
                ),
                ft.Container(
                    content=ft.Text("Card 4", size=16, weight=ft.FontWeight.W_600),
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.PINK_200,
                    height=90,
                    col={"phone": 4, "tablet": 4, "desktop": 3},
                ),
            ],
        ),
        width_label,
        breakpoint_label,
    )
    update_status()


if __name__ == "__main__":
    ft.run(main)
