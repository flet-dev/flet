from datetime import datetime

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def showcase_card(date_order: ft.CupertinoDatePickerDateOrder) -> ft.Container:
        def open_picker(_):
            picker = ft.CupertinoDatePicker(
                date_picker_mode=ft.CupertinoDatePickerMode.DATE,
                date_order=date_order,
                value=datetime(2024, 3, 12, 10, 0),
            )
            page.show_dialog(
                ft.CupertinoBottomSheet(
                    content=picker,
                    height=216,
                    padding=ft.Padding.only(top=6),
                )
            )

        return ft.Container(
            width=320,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(date_order.name, weight=ft.FontWeight.BOLD),
                    ft.Button(
                        "Open picker",
                        icon=ft.CupertinoIcons.CALENDAR,
                        on_click=open_picker,
                    ),
                ],
            ),
        )

    page.appbar = ft.AppBar(title="CupertinoDatePickerDateOrder Showcase")
    page.add(
        ft.Text("Open each variant in CupertinoBottomSheet."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                showcase_card(date_order)
                for date_order in ft.CupertinoDatePickerDateOrder
            ],
        ),
    )


ft.run(main)
