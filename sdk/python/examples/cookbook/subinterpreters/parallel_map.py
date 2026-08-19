import time
from concurrent.futures import InterpreterPoolExecutor, as_completed

import flet as ft


def _is_prime(n: int) -> bool:
    """Returns True if `n` is prime."""
    if n < 2:
        return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            return False
    return True


def count_primes(limit: int) -> int:
    """Count the primes below `limit` (CPU-bound, pure Python)."""
    count = 0
    for n in range(2, limit):
        if _is_prime(n):
            count += 1
    return count


def main(page: ft.Page):
    def start():
        button.disabled = True  # block a second run while this one is in flight
        page.update()
        page.run_thread(run)

    def run():
        """Time the same work sequentially and across a pool, then report the
        speedup. Runs on a background thread so the UI stays responsive."""
        limits = [200_000 + i * 30_000 for i in range(8)]

        # Baseline: run every chunk in this one interpreter (one core).
        status.value = "Sequential…"
        progress.value = 0
        page.update()
        started = time.perf_counter()
        for done, limit in enumerate(limits, 1):
            count_primes(limit)
            progress.value = done / len(limits)
            page.update()
        seq_time = time.perf_counter() - started

        # Parallel: one subinterpreter per chunk, each with its own GIL.
        status.value = "Parallel…"
        progress.value = 0
        page.update()
        primes = completed = 0
        started = time.perf_counter()
        with InterpreterPoolExecutor() as pool:  # sizes itself to the CPU count
            futures = [pool.submit(count_primes, n) for n in limits]
            for future in as_completed(futures):
                primes += future.result()
                completed += 1
                progress.value = completed / len(futures)
                page.update()
        par_time = time.perf_counter() - started

        status.value = (
            f"{primes} primes · sequential {seq_time:.1f}s · "
            f"parallel {par_time:.1f}s · {seq_time / par_time:.1f}× faster"
        )
        button.disabled = False
        page.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    button := ft.Button(
                        "Count primes: sequential vs parallel",
                        on_click=start,
                    ),
                    progress := ft.ProgressBar(value=0, width=300),
                    status := ft.Text(),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
