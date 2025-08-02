import flet as ft


def main(page: ft.Page):
    def handle_button_click(e: ft.Event[ft.ElevatedButton]):
        message.value = f"Textboxes values are:  '{prefix_field.value}', '{suffix_field.value}', '{prefix_suffix_field.value}', '{color_field.value}'."
        page.update()

    page.add(
        prefix_field := ft.TextField(label="With prefix", prefix="https://"),
        suffix_field := ft.TextField(label="With suffix", suffix=".com"),
        prefix_suffix_field := ft.TextField(
            label="With prefix and suffix",
            prefix="https://",
            suffix=".com",
            enable_interactive_selection=True,
        ),
        color_field := ft.TextField(
            label="My favorite color",
            icon=ft.Icons.FORMAT_SIZE,
            hint_text="Type your favorite color",
            helper="You can type only one color",
            counter="{value_length}/{max_length} chars used",
            prefix_icon=ft.Icons.COLOR_LENS,
            suffix="...is your color",
            max_length=20,
        ),
        ft.ElevatedButton(content="Submit", on_click=handle_button_click),
        message := ft.Text(),
    )


ft.run(main)
