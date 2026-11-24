import multiprocessing

import flet as ft


def crunch(progress_queue: multiprocessing.Queue, steps: int) -> None:
    """Do `steps` slices of CPU-heavy work, reporting progress after each one.

    Runs in a worker process, which has no access to the page — the queue is
    the only channel back to the UI. Values are fractions 0..1; a final `None`
    tells the consumer there is nothing more to read.
    """
    for i in range(steps):
        sum(range(50_000_000))  # one slice of real work
        progress_queue.put((i + 1) / steps)
    progress_queue.put(None)  # sentinel: no more updates


def main(page: ft.Page):
    def start():
        button.disabled = True
        status.value = "Starting worker…"
        page.update()
        queue = multiprocessing.Queue()
        worker = multiprocessing.Process(target=crunch, args=(queue, 20), daemon=True)
        worker.start()
        page.run_thread(drain, queue, worker)

    def drain(queue: multiprocessing.Queue, worker: multiprocessing.Process):
        """Forward the worker's progress reports to the UI.

        Runs on a background thread: queue.get() blocks until the worker
        reports again, so it must stay off the UI event loop.
        """
        while (value := queue.get()) is not None:
            progress.value = value
            status.value = f"Crunching… {value:.0%}"
            page.update()
        worker.join()
        status.value = "Done!"
        button.disabled = False
        page.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    button := ft.Button("Start", on_click=start),
                    progress := ft.ProgressBar(value=0, width=300),
                    status := ft.Text(),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
