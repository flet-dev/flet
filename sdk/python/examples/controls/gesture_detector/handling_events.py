import flet as ft


def main(page: ft.Page):
    page.add(
        ft.GestureDetector(
            content=ft.Container(bgcolor=ft.Colors.GREEN, width=200, height=200),
            hover_interval=50,
            on_tap=lambda e: print(e),
            on_tap_down=lambda e: print(e),
            on_tap_up=lambda e: print(e),
            on_secondary_tap=lambda e: print(e),
            on_secondary_tap_down=lambda e: print(e),
            on_secondary_tap_up=lambda e: print(e),
            on_long_press_start=lambda e: print(e),
            on_long_press_end=lambda e: print(e),
            on_secondary_long_press_start=lambda e: print(e),
            on_secondary_long_press_end=lambda e: print(e),
            on_double_tap=lambda e: print(e),
            on_double_tap_down=lambda e: print(e),
            on_pan_start=lambda e: print(e),
            on_pan_update=lambda e: print(e),
            on_pan_end=lambda e: print(e),
            on_hover=lambda e: print(e),
            on_enter=lambda e: print(e),
            on_exit=lambda e: print(e),
        )
    )


if __name__ == "__main__":
    ft.run(main)
