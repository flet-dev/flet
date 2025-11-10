import flet as ft


def main(page: ft.Page):
    # just need hold a reference to ShakeDetector in the session store
    page.session.store.set(
        "shake_detector",
        ft.ShakeDetector(
            minimum_shake_count=2,
            shake_slop_time_ms=300,
            shake_count_reset_time_ms=1000,
            on_shake=lambda _: page.add(ft.Text("Shake detected!")),
        ),
    )

    page.add(ft.Text("Shake your device!"))


ft.run(main)
