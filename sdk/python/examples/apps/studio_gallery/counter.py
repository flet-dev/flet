import flet as ft


@ft.component
def App():
    # keep the state as a string so it maps cleanly to TextField.value
    count, set_count = ft.use_state("0")

    txt_number = ft.TextField(value=count, text_align=ft.TextAlign.RIGHT, width=100)

    def parse_int_or_fallback(value, fallback):
        try:
            return int(value)
        except (TypeError, ValueError):
            try:
                return int(fallback)
            except (TypeError, ValueError):
                return 0

    def minus_click(e):
        n = parse_int_or_fallback(txt_number.value, count)
        set_count(str(n - 1))

    def plus_click(e):
        n = parse_int_or_fallback(txt_number.value, count)
        set_count(str(n + 1))

    return ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(
                [
                    ft.IconButton(ft.Icons.REMOVE, on_click=minus_click),
                    txt_number,
                    ft.IconButton(ft.Icons.ADD, on_click=plus_click),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(App))
