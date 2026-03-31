import flet as ft


def main(page: ft.Page):
    greeting = ft.Text()
    txt_name = ft.TextField(label="Your name")

    def btn_click(e):
        if not txt_name.value:
            txt_name.error_text = "Please enter your name"
            greeting.value = ""
        else:
            txt_name.error_text = None
            greeting.value = f"Hello, {txt_name.value}!"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    txt_name,
                    ft.Button("Say hello!", on_click=btn_click),
                    greeting,
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
