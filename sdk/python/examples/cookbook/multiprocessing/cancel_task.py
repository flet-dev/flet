import multiprocessing
import time

import flet as ft


def long_job(seconds: int) -> None:
    """Burn CPU for roughly `seconds` seconds.

    Stands in for work you cannot interrupt from Python itself, e.g. a tight
    loop inside a C extension library. Runs in a worker process, which is why
    it can be cancelled at any point — threads can't be stopped like that.
    """
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        sum(range(1_000_000))


def main(page: ft.Page):
    process = None

    def watch(p: multiprocessing.Process):
        """Wait (on a background thread) for the worker to end, then report
        whether it finished on its own or was cancelled."""
        p.join()
        if p.exitcode == 0:
            status.value = "Process finished normally."
        else:
            # terminate() ends the child with a negative exit code (-SIGTERM).
            status.value = f"Process was terminated (exit code {p.exitcode})."
        start.disabled = False
        cancel.disabled = True
        page.update()

    def start_job():
        nonlocal process
        process = multiprocessing.Process(target=long_job, args=(30,), daemon=True)
        process.start()
        status.value = f"Running in process {process.pid}…"
        start.disabled = True
        cancel.disabled = False
        page.update()
        page.run_thread(watch, process)

    def cancel_job():
        if process is not None and process.is_alive():
            process.terminate()  # threads can't do this

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            start := ft.Button("Start 30s job", on_click=start_job),
                            cancel := ft.Button(
                                "Cancel", on_click=cancel_job, disabled=True
                            ),
                        ]
                    ),
                    status := ft.Text(),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
