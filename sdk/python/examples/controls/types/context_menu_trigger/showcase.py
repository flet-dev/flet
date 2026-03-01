import flet as ft


def showcase_card(trigger: ft.ContextMenuTrigger) -> ft.Container:
    def on_select(e: ft.ContextMenuSelectEvent):
        item = e.item.content if e.item else f"item #{e.item_index}"
        status.value = f"Selected: {item}"
        status.update()

    def on_dismiss(_):
        if status.value == "Open the menu in the area below.":
            status.value = "Menu dismissed."
            status.update()

    menu = ft.ContextMenu(
        primary_trigger=trigger,
        primary_items=[
            ft.PopupMenuItem(icon=ft.Icons.EDIT, content="Edit"),
            ft.PopupMenuItem(icon=ft.Icons.CONTENT_COPY, content="Duplicate"),
            ft.PopupMenuItem(icon=ft.Icons.DELETE, content="Delete"),
        ],
        on_select=on_select,
        on_dismiss=on_dismiss,
        content=ft.Container(
            width=280,
            height=120,
            border=ft.Border.all(1, ft.Colors.OUTLINE),
            border_radius=8,
            bgcolor=ft.Colors.SURFACE,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(
                text_align=ft.TextAlign.CENTER,
                value=(
                    "Press and hold inside the area."
                    if trigger == ft.ContextMenuTrigger.LONG_PRESS
                    else "Press mouse button down inside the area."
                ),
            ),
        ),
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
                ft.Text(trigger.name, weight=ft.FontWeight.BOLD),
                menu,
                status := ft.Text("Open the menu in the area below.", size=11),
            ],
        ),
    )


async def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    if page.web:
        await ft.BrowserContextMenu().disable()

    page.appbar = ft.AppBar(title="ContextMenuTrigger Showcase")
    page.add(
        ft.Text("Compare context-menu open behavior for primary trigger modes."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(trigger) for trigger in ft.ContextMenuTrigger],
        ),
    )


ft.run(main)
