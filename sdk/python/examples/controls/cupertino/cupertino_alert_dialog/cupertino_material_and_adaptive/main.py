from typing import Union

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    messages = ft.Column(tight=True)

    def handle_action_click(
        e: ft.Event[Union[ft.TextButton, ft.CupertinoDialogAction]],
    ):
        messages.controls.append(ft.Text(f"Action clicked: {e.control.content}"))
        page.pop_dialog()

    cupertino_actions = [
        ft.CupertinoDialogAction(
            destructive=True,
            on_click=handle_action_click,
            content="Yes",
        ),
        ft.CupertinoDialogAction(
            default=False,
            on_click=handle_action_click,
            content="No",
        ),
    ]

    material_actions = [
        ft.TextButton(on_click=handle_action_click, content="Yes"),
        ft.TextButton(on_click=handle_action_click, content="No"),
    ]

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.FilledButton(
                        on_click=lambda _: page.show_dialog(
                            ft.AlertDialog(
                                title=ft.Text("Material Alert Dialog"),
                                content=ft.Text("Do you want to delete this file?"),
                                actions=material_actions,
                            )
                        ),
                        content="Open Material Dialog",
                    ),
                    ft.CupertinoFilledButton(
                        on_click=lambda _: page.show_dialog(
                            ft.CupertinoAlertDialog(
                                title=ft.Text("Cupertino Alert Dialog"),
                                content=ft.Text("Do you want to delete this file?"),
                                actions=cupertino_actions,
                            )
                        ),
                        content="Open Cupertino Dialog",
                    ),
                    ft.FilledButton(
                        adaptive=True,
                        bgcolor=ft.Colors.BLUE_ACCENT,
                        on_click=lambda _: page.show_dialog(
                            ft.AlertDialog(
                                adaptive=True,
                                title=ft.Text("Adaptive Alert Dialog"),
                                content=ft.Text("Do you want to delete this file?"),
                                actions=(
                                    cupertino_actions
                                    if page.platform.is_apple()
                                    else material_actions
                                ),
                            )
                        ),
                        content="Open Adaptive Dialog",
                    ),
                    messages,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
