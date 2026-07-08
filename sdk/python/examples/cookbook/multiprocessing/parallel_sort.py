import random
from concurrent.futures import ProcessPoolExecutor, as_completed

import flet as ft


def sort_chunk(chunk: list[float]) -> list[float]:
    """Sort one chunk of data."""
    return sorted(chunk)


def main(page: ft.Page):
    def run_sort():
        """Orchestrate the pool from a background thread, updating the UI
        from the main process as results come in."""
        chunks = [[random.random() for _ in range(250_000)] for _ in range(8)]
        completed = 0
        # Without max_workers, the pool sizes itself to the machine's CPUs.
        with ProcessPoolExecutor() as pool:
            futures = [pool.submit(sort_chunk, c) for c in chunks]
            # as_completed() yields each future as soon as its worker is done.
            for _ in as_completed(futures):
                completed += 1
                progress.value = completed / len(futures)
                status.value = f"Sorted {completed}/{len(futures)} chunks"
                page.update()
        status.value = "Done!"
        page.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Button(
                        "Start sorting", on_click=lambda: page.run_thread(run_sort)
                    ),
                    status := ft.Text("Idle"),
                    progress := ft.ProgressBar(value=0, width=300),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
