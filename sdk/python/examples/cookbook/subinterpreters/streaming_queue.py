import threading
from concurrent import interpreters

import flet as ft


def _is_prime(n: int) -> bool:
    """Returns True if `n` is prime."""
    if n < 2:
        return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            return False
    return True


def _count_in_range(lo: int, hi: int) -> int:
    """Returns the number of primes in the half-open range [lo, hi)."""
    count = 0
    for n in range(lo, hi):
        if _is_prime(n):
            count += 1
    return count


def stream_primes(progress_queue, chunks: int, per_chunk: int) -> None:
    """Count primes in `chunks` slices, reporting progress after each one.

    Runs in a subinterpreter, which has no access to the page — the queue is
    the only channel back to the UI. Values are fractions 0..1; a final `None`
    tells the consumer there is nothing more to read.
    """
    for i in range(chunks):
        lo = i * per_chunk + 2
        _count_in_range(lo, lo + per_chunk)
        progress_queue.put((i + 1) / chunks)
    progress_queue.put(None)  # sentinel: no more updates


def main(page: ft.Page):
    def start():
        button.disabled = True
        status.value = "Working…"
        page.update()

        # A queue shared between this interpreter and the subinterpreter. Only
        # "shareable" objects cross it (numbers, str, bytes, None, tuples of
        # those, and the queue itself).
        queue = interpreters.create_queue()

        interp = interpreters.create()
        drained = threading.Event()

        # The worker runs the job in the subinterpreter and blocks that thread,
        # so it goes on its own background thread…
        page.run_thread(work, interp, queue, drained)
        # …while a second thread drains progress and drives the UI.
        page.run_thread(drain, queue, drained)

    def work(interp, queue, drained):
        """Run the job in the subinterpreter, then close it once the UI is done.

        On its own thread because interp.call() blocks until the job finishes.
        The interpreter is closed only after `drained` is set — a subinterpreter
        Queue's pending items go invalid the moment its interpreter closes.
        """
        interp.call(stream_primes, queue, 20, 100_000)
        drained.wait()
        interp.close()

    def drain(queue, drained):
        """Forward the worker's progress reports to the UI.

        Runs on a background thread: queue.get() blocks until the worker
        reports again, so it must stay off the UI event loop.
        """
        while (value := queue.get()) is not None:
            progress.value = value
            status.value = f"Counting… {value:.0%}"
            page.update()
        drained.set()
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
