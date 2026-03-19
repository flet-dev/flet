"""
Benchmark: validation overhead in _before_update_safe().

Compares declarative Annotated + V.* validation (current) against
the imperative if/raise baseline that existed on main.

Run with:  pytest tests/test_validation_benchmark.py -s -m benchmark
"""

import statistics
import time
import warnings

import pytest

import flet as ft

WARMUP = 50
ITERATIONS = 500


def _make_controls(n: int) -> list:
    """Create a realistic mix of controls with validated fields."""
    controls = []
    for i in range(n):
        kind = i % 6
        if kind == 0:
            controls.append(ft.Slider(value=0.5, min=0, max=1))
        elif kind == 1:
            controls.append(
                ft.RangeSlider(start_value=0.2, end_value=0.8, min=0, max=1)
            )
        elif kind == 2:
            controls.append(ft.TextField(label="test", max_length=100))
        elif kind == 3:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", DeprecationWarning)
                controls.append(ft.Icon(ft.Icons.FAVORITE))
        elif kind == 4:
            controls.append(ft.Text(value="hello", opacity=0.8))
        elif kind == 5:
            controls.append(ft.Divider(thickness=2, height=10))
    return controls


def _bench_before_update(controls: list, iterations: int) -> list[float]:
    """Time _before_update_safe() across all controls, repeated `iterations` times."""
    timings = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        for ctrl in controls:
            ctrl._before_update_safe()
        elapsed_us = (time.perf_counter_ns() - start) / 1_000
        timings.append(elapsed_us)
    return timings


def _bench_construction(n: int, iterations: int) -> list[float]:
    """Time control construction to check for __init__-time overhead."""
    timings = []
    for _ in range(iterations):
        start = time.perf_counter_ns()
        _make_controls(n)
        elapsed_us = (time.perf_counter_ns() - start) / 1_000
        timings.append(elapsed_us)
    return timings


def _report(label: str, timings: list[float], n_controls: int) -> dict:
    med = statistics.median(timings)
    p95 = sorted(timings)[int(len(timings) * 0.95)]
    mean = statistics.mean(timings)
    per_ctrl = med / n_controls if n_controls else 0
    print(f"  {label}:")
    print(
        f"    median={med:.1f}us  mean={mean:.1f}us  "
        f"p95={p95:.1f}us  per_ctrl={per_ctrl:.2f}us"
    )
    return {"median": med, "p95": p95, "mean": mean, "per_ctrl": per_ctrl}


@pytest.mark.benchmark
class TestValidationBenchmark:
    """
    Validation performance benchmarks.

    Baseline (main, imperative if/raise):
        50  controls: ~0.68 us/ctrl
        200 controls: ~1.04 us/ctrl
        500 controls: ~1.02 us/ctrl

    PR before optimization:
        50  controls: ~10.17 us/ctrl
        200 controls: ~10.25 us/ctrl
        500 controls: ~10.22 us/ctrl

    PR after optimization (cached _resolve_allow_none_for_field,
    fast-path for non-None in _prepare_field_value, guarded reported.clear):
        50  controls: ~2.00 us/ctrl
        200 controls: ~2.34 us/ctrl
        500 controls: ~2.34 us/ctrl
    """

    @pytest.mark.parametrize("n_controls", [50, 200, 500])
    def test_before_update_safe(self, n_controls: int):
        controls = _make_controls(n_controls)

        # Warmup
        _bench_before_update(controls, WARMUP)

        timings = _bench_before_update(controls, ITERATIONS)
        stats = _report(
            f"_before_update_safe ({n_controls} controls)", timings, n_controls
        )

        # Soft assertion: flag if regression exceeds 5 us/ctrl
        assert stats["per_ctrl"] < 5.0, (
            f"Validation overhead too high: {stats['per_ctrl']:.2f} us/ctrl "
            f"(threshold: 5.0 us/ctrl)"
        )

    @pytest.mark.parametrize("n_controls", [50, 200, 500])
    def test_construction(self, n_controls: int):
        # Warmup
        _bench_construction(n_controls, WARMUP)

        timings = _bench_construction(n_controls, ITERATIONS)
        _report(f"construction ({n_controls} controls)", timings, n_controls)
