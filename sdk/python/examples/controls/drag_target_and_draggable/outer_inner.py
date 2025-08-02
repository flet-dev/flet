import flet as ft


class OuterContainer(ft.Draggable):
    def __init__(self, color, list_ref):
        self.list_ref = list_ref
        self.container_color = color
        self.inner_container = InnerContainer(self)
        self.outer_container = ft.Container(
            content=self.inner_container,
            width=200,
            height=200,
            bgcolor=self.container_color,
            border_radius=5,
            alignment=ft.Alignment.CENTER,
            border=ft.Border.all(4, ft.Colors.BLACK12),
        )

        self.target = ft.DragTarget(
            group="inner",
            data=self,
            on_accept=self.inner_drag_accept,
            on_will_accept=self.inner_drag_will_accept,
            on_leave=self.inner_drag_leave,
            content=ft.DragTarget(
                group="outer",
                content=self.outer_container,
                on_accept=self.handle_drag_accept,
                on_will_accept=self.handle_drag_will_accept,
                on_leave=self.handle_drag_leave,
            ),
        )
        super().__init__(content=self.target, group="outer")

    def handle_drag_accept(self, e: ft.DragTargetEvent):
        if e.data:
            self.outer_container.border = ft.Border.all(4, ft.Colors.BLACK12)
        self.update()

    def handle_drag_will_accept(self, e: ft.DragWillAcceptEvent):
        if e.data:
            self.outer_container.border = ft.Border.all(4, ft.Colors.BLACK54)
        self.update()

    def handle_drag_leave(self, e: ft.DragTargetLeaveEvent):
        self.outer_container.border = ft.Border.all(4, ft.Colors.BLACK12)
        self.update()

    def inner_drag_accept(self, e):
        if e.data:
            self.outer_container.border_radius = 5
        self.update()

    def inner_drag_will_accept(self, e: ft.DragWillAcceptEvent):
        if e.data:
            self.outer_container.border_radius = 25
        self.update()

    def inner_drag_leave(self, e: ft.DragTargetLeaveEvent):
        self.outer_container.border_radius = 5
        self.update()


class InnerContainer(ft.Draggable):
    def __init__(self, outer: OuterContainer):
        self.outer = outer
        self.inner_icon = ft.Icon(
            name=ft.Icons.CIRCLE,
            color=ft.Colors.WHITE54,
            size=100,
            tooltip="drag me!",
        )
        # self.data = self

        self.target = ft.DragTarget(
            group="inner",
            content=self.inner_icon,
            on_accept=self.handle_drag_accept,
            on_leave=self.handle_drag_leave,
            on_will_accept=self.handle_drag_will_accept,
        )
        super().__init__(content=self.target, group="outer")

    def set_color(self, color: str):
        self.inner_icon.color = color
        self.update()

    def handle_drag_accept(self, e: ft.DragTargetEvent):
        if e.data:
            self.set_color(ft.Colors.WHITE54)

    def handle_drag_will_accept(self, e: ft.DragWillAcceptEvent):
        if e.data:
            self.set_color(ft.Colors.BLUE_GREY)
        self.update()

    def handle_drag_leave(self, e: ft.DragTargetLeaveEvent):
        self.set_color(ft.Colors.WHITE54)
        self.update()


def main(page: ft.Page):
    page.bgcolor = ft.Colors.BLUE_GREY_100

    list_ref = ft.Ref[ft.Row]()

    page.add(
        ft.Row(
            ref=list_ref,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            controls=[
                OuterContainer(ft.Colors.DEEP_ORANGE_400, list_ref),
                OuterContainer(ft.Colors.BLUE_400, list_ref),
            ],
        )
    )
    page.update()


ft.run(main)
