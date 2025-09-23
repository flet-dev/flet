import math
import random
import time

import pytest

import flet as ft
from flet.controls.base_control import BaseControl, control
from flet.controls.object_patch import ObjectPatch

MAX_SEEDS = 500


@control("PerfText")
class PerfText(BaseControl):
    value: str


def _keyed_columns(size: int) -> tuple[ft.Column, ft.Column]:
    old_items = [PerfText(value=f"Item {i}", key=i) for i in range(size)]
    new_order = list(range(size))
    random.Random(42).shuffle(new_order)
    new_items = [
        PerfText(value=f"Item {i}" if i % 5 else f"Item {i}*", key=i) for i in new_order
    ]

    old_column = ft.Column(old_items)
    old_column._frozen = True
    new_column = ft.Column(new_items)
    return old_column, new_column


def _literal_columns(size: int) -> tuple[ft.Column, ft.Column]:
    src = list(range(size))
    dst = src[1:] + [size]
    old_column = ft.Column(src)
    old_column._frozen = True
    new_column = ft.Column(dst)
    return old_column, new_column


def _time_diff(factory, runs: int = 3) -> tuple[float, list[float]]:
    durations: list[float] = []
    for _ in range(runs):
        old, new = factory()
        start = time.perf_counter()
        ObjectPatch.from_diff(old, new, control_cls=BaseControl)
        durations.append(time.perf_counter() - start)
    return min(durations), durations


def test_keyed_diff_scaling_is_near_linear():
    small_best, small_all = _time_diff(lambda: _keyed_columns(150))
    large_best, large_all = _time_diff(lambda: _keyed_columns(300))
    print(
        "keyed diff timings",
        {
            "150": [round(d * 1000, 3) for d in small_all],
            "300": [round(d * 1000, 3) for d in large_all],
        },
    )
    assert large_best <= small_best * 4, (small_best, large_best)


def test_literal_diff_scaling_is_near_linear():
    small_best, small_all = _time_diff(lambda: _literal_columns(200))
    large_best, large_all = _time_diff(lambda: _literal_columns(400))
    print(
        "literal diff timings",
        {
            "200": [round(d * 1000, 3) for d in small_all],
            "400": [round(d * 1000, 3) for d in large_all],
        },
    )
    assert large_best <= small_best * 3, (small_best, large_best)


def _sunflower_controls(count: int) -> list[ft.Container]:
    tau = math.pi * 2
    scale_factor = 1 / 40
    phi = (math.sqrt(5) + 1) / 2
    controls: list[ft.Container] = []
    for i in range(count):
        theta = i * tau / phi
        r = math.sqrt(i) * scale_factor
        controls.append(
            ft.Container(
                key=i,
                width=5,
                height=5,
                bgcolor=ft.Colors.ORANGE,
                align=ft.Alignment(r * math.cos(theta), -r * math.sin(theta)),
            )
        )
    for j in range(count, MAX_SEEDS):
        controls.append(
            ft.Container(
                key=j,
                width=5,
                height=5,
                bgcolor=ft.Colors.GREY_700,
                align=ft.Alignment(
                    math.cos(tau * j / (MAX_SEEDS - 1)) * 0.9,
                    math.sin(tau * j / (MAX_SEEDS - 1)) * 0.9,
                ),
            )
        )
    return controls


def _sunflower_stack(count: int) -> tuple[ft.Stack, ft.Stack]:
    old_stack = ft.Stack(controls=_sunflower_controls(count))
    old_stack._frozen = True
    new_stack = ft.Stack(controls=_sunflower_controls(count + 10))
    return old_stack, new_stack


@pytest.mark.skip(reason="Performance test, not a unit test")
def test_sunflower_like_update_is_fast():
    best, runs = _time_diff(lambda: _sunflower_stack(250))
    print("sunflower diff timings", [round(d * 1000, 3) for d in runs])
    # Empirically, anything above ~0.09s is a regression compared to pre-change behavior
    assert best <= 0.09, best
