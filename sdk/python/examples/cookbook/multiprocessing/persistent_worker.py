import multiprocessing
import time

import flet as ft


def calc_worker(conn) -> None:
    """Serve calculation jobs over the pipe until told to stop.

    Runs in a worker process that stays alive across jobs, so the process
    startup cost is paid once. Expensive setup (loading models, opening
    datasets, warming caches) could be done once here, before the loop,
    and reused by every job. Receiving `None` is the shutdown signal.
    """
    while (job := conn.recv()) is not None:
        started = time.perf_counter()
        result = sum(i * i for i in range(job))
        conn.send((result, time.perf_counter() - started))
    conn.close()


def main(page: ft.Page):
    # One end of the pipe goes to the worker, the other stays with the UI.
    parent_conn, child_conn = multiprocessing.Pipe()
    worker = multiprocessing.Process(
        target=calc_worker, args=(child_conn,), daemon=True
    )
    worker.start()

    def submit():
        # One job in flight at a time: the button stays disabled until the
        # worker replies (a bare Pipe is not multiplexed).
        button.disabled = True
        status.value = "Working…"
        page.update()
        page.run_thread(request)

    def request():
        """Send a job to the worker and wait for its reply.

        Should be run on a background thread: conn.recv() blocks until the worker
        answers, so it must stay off the UI event loop.
        """
        parent_conn.send(100_000_000)
        result, duration = parent_conn.recv()
        status.value = (
            f"sum of squares = {result}\n{duration:.2f}s in process {worker.pid}"
        )
        button.disabled = False
        page.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    button := ft.Button("Compute in worker", on_click=submit),
                    status := ft.Text(f"Worker ready (pid {worker.pid})"),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
