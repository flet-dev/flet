import gc
import tracemalloc

import flet as ft
from flet.controls.base_control import BaseControl
from flet.controls.object_patch import ObjectPatch


def _make_tree(iteration: int, size: int = 36) -> ft.Column:
    controls: list[ft.Text] = []
    offset = iteration % size
    for i in range(size):
        key = (i + offset) % size
        value = f"Item {key}"
        if i == (iteration % 7):
            value = f"{value}*{iteration % 5}"
        controls.append(ft.Text(value=value, key=key))
    return ft.Column(controls=controls)


def _object_patch_size(snapshot: tracemalloc.Snapshot) -> int:
    total = 0
    for stat in snapshot.statistics("filename"):
        frame = stat.traceback[0]
        if frame.filename.endswith("flet/controls/object_patch.py"):
            total += stat.size
    return total


def test_object_diff_churn_memory_growth_is_bounded():
    iterations = 480
    sample_step = 80
    warmup = 160

    previous = _make_tree(0)
    previous._frozen = True

    tracemalloc.start(10)
    samples: list[int] = []
    try:
        for i in range(1, iterations + 1):
            current = _make_tree(i)
            ObjectPatch.from_diff(previous, current, control_cls=BaseControl)
            previous = current
            previous._frozen = True

            if i % sample_step == 0:
                gc.collect()
                samples.append(_object_patch_size(tracemalloc.take_snapshot()))
    finally:
        tracemalloc.stop()

    steady_state = [
        size for idx, size in enumerate(samples, start=1) if idx * sample_step >= warmup
    ]
    assert steady_state, samples

    baseline = steady_state[0]
    final = steady_state[-1]
    max_steady = max(steady_state)

    # In steady state this should stay near a plateau, not grow linearly with churn.
    assert final - baseline < 500_000, (baseline, final, steady_state)
    assert max_steady - baseline < 700_000, (baseline, max_steady, steady_state)
