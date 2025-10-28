import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 20

    def switch_animation(e: ft.Event[ft.CupertinoSlidingSegmentedButton]):
        if e.control.selected_index == 0:
            tile.animation_style = None
        elif e.control.selected_index == 1:
            tile.animation_style = ft.AnimationStyle(
                curve=ft.AnimationCurve.BOUNCE_OUT,
                duration=ft.Duration(seconds=5),
            )
        else:
            tile.animation_style = ft.AnimationStyle.no_animation()

    page.add(
        ft.CupertinoSlidingSegmentedButton(
            selected_index=0,
            thumb_color=ft.Colors.BLUE_400,
            on_change=switch_animation,
            controls=[
                ft.Text("Default animation"),
                ft.Text("Custom animation"),
                ft.Text("No animation"),
            ],
        ),
        tile := ft.ExpansionTile(
            expanded=True,
            title=ft.Text(
                "Expand/Collapse me while being attentive to the animations!"
            ),
            controls=[
                ft.ListTile(title=ft.Text("Sub-item 1")),
                ft.ListTile(title=ft.Text("Sub-item 2")),
                ft.ListTile(title=ft.Text("Sub-item 3")),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
