import flet_lottie as ftl

import flet as ft


def main(page: ft.Page):
    page.add(
        ftl.Lottie(
            src="https://raw.githubusercontent.com/xvrh/lottie-flutter/master/example/assets/Mobilo/A.json",
            reverse=False,
            animate=True,
            error_content=ft.Placeholder(ft.Text("Error loading Lottie")),
            on_error=lambda e: print(f"Error loading Lottie: {e.data}"),
        ),
        ftl.Lottie(
            src="sample.json",
            reverse=False,
            animate=True,
            enable_merge_paths=True,
            enable_layers_opacity=True,
            error_content=ft.Placeholder(ft.Text("Error loading Lottie")),
            on_error=lambda e: print(f"Error loading Lottie: {e.data}"),
        ),
    )


ft.run(main)
