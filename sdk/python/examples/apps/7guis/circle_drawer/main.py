from dataclasses import dataclass

import flet as ft

DEFAULT_RADIUS = 28.0
MIN_RADIUS = 12
MAX_RADIUS = 90


@dataclass
class Circle:
    x: float
    y: float
    radius: float


def clone_circles(circles: list[Circle]) -> list[Circle]:
    return [Circle(circle.x, circle.y, circle.radius) for circle in circles]


def main(page: ft.Page):
    page.title = "7GUIs - Circle Drawer"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    history: list[list[Circle]] = [[]]
    history_index = 0
    selected_index: int | None = None

    def get_circles() -> list[Circle]:
        return history[history_index]

    def push_snapshot(new_state: list[Circle], select: int | None):
        nonlocal history, history_index, selected_index
        history = history[: history_index + 1]
        history.append(clone_circles(new_state))
        history_index += 1
        selected_index = select
        refresh_ui()

    def build_circle_control(index: int, circle: Circle) -> ft.Container:
        diameter = circle.radius * 2
        is_selected = index == selected_index
        return ft.Container(
            left=circle.x - circle.radius,
            top=circle.y - circle.radius,
            width=diameter,
            height=diameter,
            border_radius=circle.radius,
            bgcolor=ft.Colors.AMBER_100 if is_selected else ft.Colors.BLUE_100,
            border=ft.Border.all(
                3 if is_selected else 2,
                ft.Colors.AMBER_700 if is_selected else ft.Colors.BLUE_400,
            ),
            alignment=ft.Alignment.CENTER,
            on_click=lambda e, i=index: open_editor(i),
            content=ft.Text(
                str(index + 1),
                size=12,
                weight=ft.FontWeight.W_700,
                color=ft.Colors.BLUE_GREY_900,
            ),
        )

    def refresh_ui():
        undo_button.disabled = history_index == 0
        redo_button.disabled = history_index >= len(history) - 1

        canvas_host.content = ft.Stack(
            height=295,
            controls=[
                ft.GestureDetector(
                    on_tap_down=add_circle,
                    content=ft.Container(border_radius=18, bgcolor=ft.Colors.WHITE),
                ),
                *[
                    build_circle_control(index, circle)
                    for index, circle in enumerate(get_circles())
                ],
            ],
        )
        page.update()

    def add_circle(e: ft.TapEvent):
        if e.local_position is None:
            return

        new_circles = clone_circles(get_circles())
        new_circles.append(
            Circle(x=e.local_position.x, y=e.local_position.y, radius=DEFAULT_RADIUS)
        )
        push_snapshot(new_circles, len(new_circles) - 1)

    def open_editor(index: int):
        nonlocal selected_index
        selected_index = index
        circle = get_circles()[index]

        def apply_radius(e: ft.Event[ft.Button]):
            new_circles = clone_circles(get_circles())
            new_circles[index].radius = float(rslider.value)
            page.pop_dialog()
            push_snapshot(new_circles, index)

        def handle_radius_change(e: ft.Event[ft.Slider]):
            rlabel.value = f"Radius: {int(float(rslider.value))} px"
            rlabel.update()

        refresh_ui()
        page.show_dialog(
            ft.AlertDialog(
                title=ft.Text(f"Resize Circle {index + 1}"),
                content=ft.Column(
                    tight=True,
                    spacing=14,
                    controls=[
                        ft.Text("Use the slider to set a new radius."),
                        rlabel := ft.Text(f"Radius: {int(circle.radius)} px"),
                        rslider := ft.Slider(
                            min=MIN_RADIUS,
                            max=MAX_RADIUS,
                            value=circle.radius,
                            divisions=MAX_RADIUS - MIN_RADIUS,
                            label="{value}",
                            on_change=handle_radius_change,
                        ),
                    ],
                ),
                actions=[
                    ft.TextButton("Cancel", on_click=lambda e: page.pop_dialog()),
                    ft.FilledButton("Apply", on_click=apply_radius),
                ],
            )
        )

    def undo(e: ft.Event[ft.OutlinedButton]):
        nonlocal history_index, selected_index
        if history_index == 0:
            return
        history_index -= 1
        selected_index = None
        refresh_ui()

    def redo(e: ft.Event[ft.OutlinedButton]):
        nonlocal history_index, selected_index
        if history_index >= len(history) - 1:
            return
        history_index += 1
        selected_index = None
        refresh_ui()

    page.add(
        ft.SafeArea(
            content=ft.Container(
                width=700,
                height=500,
                padding=28,
                border_radius=24,
                bgcolor=ft.Colors.ORANGE_50,
                content=ft.Column(
                    tight=True,
                    spacing=18,
                    controls=[
                        ft.Text("Circle Drawer", size=28, weight=ft.FontWeight.W_700),
                        ft.Text(
                            "Add circles with a click, resize them in a dialog, "
                            "and step through history.",
                            color=ft.Colors.BLUE_GREY_700,
                        ),
                        canvas_host := ft.Container(
                            border_radius=24,
                            bgcolor=ft.Colors.WHITE,
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                undo_button := ft.OutlinedButton(
                                    "Undo",
                                    icon=ft.Icons.UNDO,
                                    on_click=undo,
                                ),
                                redo_button := ft.OutlinedButton(
                                    "Redo",
                                    icon=ft.Icons.REDO,
                                    on_click=redo,
                                ),
                            ],
                        ),
                    ],
                ),
            ),
        )
    )
    refresh_ui()


if __name__ == "__main__":
    ft.run(main)
