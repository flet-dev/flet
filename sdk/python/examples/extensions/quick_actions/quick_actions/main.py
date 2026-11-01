from flet_quick_actions import QuickActions, ShortcutItem

import flet as ft


def main(page: ft.Page):
    page.title = "Quick Actions Demo"

    status = ft.Text("no action set", size=20, weight=ft.FontWeight.BOLD)
    hint = ft.Text(
        "On the home screen, long-press the app icon to get "
        "'Action one' or 'Action two'. Tapping one should change the title.",
        color=ft.Colors.ON_SURFACE_VARIANT,
    )

    qa = QuickActions()

    def on_action(e: ft.ControlEvent):
        status.value = e.data
        page.update()

    async def clear_shortcuts(_):
        await qa.clear_shortcuts()
        status.value = "Shortcuts cleared."
        page.update()

    qa.on_action = on_action

    async def install_shortcuts(_):
        await qa.set_shortcuts(
            [
                ShortcutItem(
                    type="new_message",
                    localized_title="New Message",
                    icon="ic_launcher",
                ),
                ShortcutItem(
                    type="search",
                    localized_title="Search",
                    icon="ic_launcher",
                ),
            ]
        )
        status.value = "New Shortcuts installed - long-press the app icon."
        page.update()

    async def setup():
        await qa.set_shortcuts(
            [
                # NOTE: this first icon works on iOS only in the example.
                # Use the same file name across platforms in real projects.
                ShortcutItem(
                    type="action_one",
                    localized_title="Action one",
                    localized_subtitle="Action one subtitle",
                    icon="AppIcon",
                ),
                # NOTE: this second icon works on Android only.
                ShortcutItem(
                    type="action_two",
                    localized_title="Action two",
                    icon="ic_launcher",
                ),
            ]
        )
        if status.value == "no action set":
            status.value = "actions ready"

        page.update()

        # Cold-start pickup: if the app was launched by tapping a shortcut,
        # the action fired before `on_action` was attached. Replay it now.
        pending = await qa.get_pending_action()
        if pending:
            on_action(ft.ControlEvent(control=qa, name="action", data=pending))

    page.add(
        ft.SafeArea(
            content=ft.Column(
                [
                    status,
                    hint,
                    ft.Button(
                        "Install shortcuts",
                        on_click=install_shortcuts,
                    ),
                    ft.Button(
                        "Clear shortcuts",
                        on_click=clear_shortcuts,
                    ),
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
    )

    page.run_task(setup)


if __name__ == "__main__":
    ft.run(main)
