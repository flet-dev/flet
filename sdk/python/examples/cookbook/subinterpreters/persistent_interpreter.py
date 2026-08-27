import atexit
import time
from concurrent import interpreters

import flet as ft

_UPPER = 2_000_000
_primes: list[int] | None = None


def _is_prime(n: int) -> bool:
    """Returns True if `n` is prime."""
    if n < 2:
        return False
    for d in range(2, int(n**0.5) + 1):
        if n % d == 0:
            return False
    return True


def nth_prime(n: int) -> dict:
    """Returns the n-th prime (1-indexed), building a prime table on first call.

    Runs in a long-lived subinterpreter that keeps its state across calls, so
    the table is built once (cached in a module global) and reused after that.
    The build stands in for genuinely expensive setup — loading a model, opening
    a dataset, warming a cache.
    """
    global _primes
    built = _primes is None
    if built:
        table = []
        for x in range(2, _UPPER):
            if _is_prime(x):
                table.append(x)
        _primes = table
    return {
        "prime": _primes[n - 1],
        "built_this_call": built,
        "table_size": len(_primes),
    }


def main(page: ft.Page):
    # One long-lived subinterpreter, created once and reused for every query,
    # so its cached state survives.
    interp = interpreters.create()
    atexit.register(interp.close)  # close it at exit

    def query():
        button.disabled = True
        page.update()
        page.run_thread(run)

    def run():
        """Call the interpreter on a background thread and show the result."""
        started = time.perf_counter()
        result = interp.call(nth_prime, 100_000)
        elapsed = time.perf_counter() - started
        how = "built the table" if result["built_this_call"] else "reused cache"
        status.value = f"100,000th prime = {result['prime']}\n{how} in {elapsed:.2f}s"
        button.disabled = False
        page.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Click twice: the first query builds a prime table, the "
                        "second reuses it from the live interpreter."
                    ),
                    button := ft.Button("Find the 100,000th prime", on_click=query),
                    status := ft.Text(),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
