import flet_shadcn_ui as shad

import flet as ft

FAQ = [
    ("a11y", "Is it accessible?", "Yes. It adheres to the WAI-ARIA design pattern."),
    (
        "styled",
        "Is it styled?",
        "Yes. It comes with default styles that match the other components.",
    ),
    (
        "animated",
        "Is it animated?",
        "Yes. It's animated by default, but you can disable it if you prefer.",
    ),
]


def main(page: ft.Page):
    page.title = "Shadcn Accordion"

    def handle_change(e: ft.Event[shad.Accordion]):
        status.value = f"Expanded: {', '.join(e.control.value) or 'none'}"

    status = ft.Text("Expanded: none")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=420,
                controls=[
                    shad.Accordion(
                        on_change=handle_change,
                        items=[
                            shad.AccordionItem(
                                value=value, title=title, content=ft.Text(answer)
                            )
                            for value, title, answer in FAQ
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
