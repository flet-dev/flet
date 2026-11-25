import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent TeachingTip"

    def show_tip(e: ft.Event[fluent.HyperlinkButton]):
        tip.open = True

    def close_tip(e: ft.Event[fluent.FilledButton]):
        tip.open = False

    tip = fluent.TeachingTip(
        content=fluent.Button("Save"),
        title="Save your work",
        subtitle="Your changes are kept on this device until you save them.",
        leading=fluent.FluentIcons.LIGHTBULB,
        placement=fluent.FlyoutPlacementMode.BOTTOM_LEFT,
        buttons=[fluent.FilledButton("Got it", on_click=close_tip)],
    )

    page.add(
        ft.SafeArea(
            content=ft.Row(
                controls=[
                    tip,
                    fluent.HyperlinkButton("What's new?", on_click=show_tip),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
