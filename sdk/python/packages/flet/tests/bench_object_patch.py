"""
Standalone benchmark for object_patch performance.
Run with: python bench_object_patch.py

Measures several scenarios before and after optimisations.
"""

import math
import random
import sys
import time
from typing import Optional

import flet as ft
from flet.controls.base_control import BaseControl, control
from flet.controls.object_patch import ObjectPatch

# ---------------------------------------------------------------------------
# Control fixtures
# ---------------------------------------------------------------------------


@control("BenchText")
class BenchText(BaseControl):
    value: str = ""


@control("BenchCard")
class BenchCard(BaseControl):
    title: str = ""
    subtitle: str = ""
    badge: str = ""
    enabled: bool = True
    selected: bool = False
    width: Optional[float] = None
    height: Optional[float] = None
    color: Optional[str] = None
    bgcolor: Optional[str] = None
    border_radius: Optional[float] = None
    padding: Optional[float] = None
    margin: Optional[float] = None
    opacity: float = 1.0
    tooltip: Optional[str] = None
    visible: bool = True
    expand: bool = False
    tag: Optional[str] = None
    rank: int = 0
    score: float = 0.0
    category: Optional[str] = None


# ---------------------------------------------------------------------------
# Timing helper
# ---------------------------------------------------------------------------


def _bench(label: str, factory, runs: int = 5) -> float:
    durations = []
    for _ in range(runs):
        old, new = factory()
        t0 = time.perf_counter()
        ObjectPatch.from_diff(old, new, control_cls=BaseControl)
        durations.append(time.perf_counter() - t0)
    best = min(durations)
    avg = sum(durations) / len(durations)
    print(f"  {label:<55} best={best * 1000:7.3f} ms  avg={avg * 1000:7.3f} ms")
    return best


# ---------------------------------------------------------------------------
# Scenario 1: frozen, all-keyed list (existing strong path)
# ---------------------------------------------------------------------------


def _frozen_all_keyed(size: int):
    rng = random.Random(42)
    src_items = [BenchText(value=f"item-{i}", key=i) for i in range(size)]
    order = list(range(size))
    rng.shuffle(order)
    dst_items = [
        BenchText(value=f"item-{i}" if i % 7 else f"item-{i}*", key=i) for i in order
    ]
    old = ft.Column(src_items)
    old._frozen = True
    new = ft.Column(dst_items)
    return old, new


# ---------------------------------------------------------------------------
# Scenario 2: frozen, mixed keyed/unkeyed list (currently degrades to positional)
# ---------------------------------------------------------------------------


def _frozen_mixed_keyed(size: int, keyed_fraction: float = 0.5):
    rng = random.Random(99)
    threshold = int(size * keyed_fraction)

    def make_items(shuffled=False):
        items = []
        for i in range(size):
            k = i if i < threshold else None
            items.append(BenchText(value=f"item-{i}", key=k))
        if shuffled:
            # Shuffle only the keyed items (to force moves in a correct impl)
            keyed = [(j, x) for j, x in enumerate(items) if x.key is not None]
            rng.shuffle(keyed)
            for _new_pos, (orig_pos, item) in enumerate(keyed):
                items[orig_pos] = item
        return items

    old = ft.Column(make_items(shuffled=False))
    old._frozen = True
    new = ft.Column(make_items(shuffled=True))
    return old, new


# ---------------------------------------------------------------------------
# Scenario 3: frozen, control with many fields, only a few differ
# ---------------------------------------------------------------------------


def _frozen_many_fields(n_controls: int, n_changed: int = 2):
    """
    Simulates a list of BenchCard controls where only n_changed fields differ
    between old and new. This measures the cost of the full field-scan in frozen
    mode (current) vs a future _values-union fast path.
    """

    def make_card(i, mutate=False):
        c = BenchCard(
            key=i,
            title=f"Card {i}",
            subtitle=f"Sub {i}",
            enabled=True,
            rank=i,
            score=float(i),
        )
        if mutate:
            c = BenchCard(
                key=i,
                title=f"Card {i}",
                subtitle=f"Sub {i}",
                enabled=True,
                rank=i,
                score=float(i),
                badge="NEW" if i % 10 == 0 else "",  # changed
                selected=i % 5 == 0,  # changed
            )
        return c

    src = [make_card(i, mutate=False) for i in range(n_controls)]
    dst = [make_card(i, mutate=True) for i in range(n_controls)]
    old = ft.Column(src)
    old._frozen = True
    new = ft.Column(dst)
    return old, new


# ---------------------------------------------------------------------------
# Scenario 4: non-frozen, list rebuilt each update with same explicit keys
# ---------------------------------------------------------------------------


def _nonfrozen_rebuilt_keyed(size: int):
    """
    Simulates a declarative-style non-frozen update where the child list is
    rebuilt from scratch each time but items carry explicit keys.
    Currently: all items are treated as remove+add (identity lost).
    After fix: items matched by explicit key and compared in place.
    """

    def make_list(mutate: bool):
        items = []
        for i in range(size):
            items.append(
                BenchText(
                    value=f"item-{i}" if not mutate or i % 8 else f"item-{i}!",
                    key=i,
                )
            )
        return items

    # Build the "old" list and configure it (simulate it being previously on the page)
    old_items = make_list(mutate=False)
    old_col = ft.Column(old_items)
    # Seed __prev_lists as protocol serialisation would (structural list tracking)
    object.__setattr__(old_col, "__prev_lists", {"controls": old_items[:]})
    object.__setattr__(old_col, "__prev_dicts", {})
    object.__setattr__(old_col, "__prev_classes", {})

    # New list: same keys, new Python objects
    new_items = make_list(mutate=True)
    old_col.controls = new_items  # structural reassignment
    new_col = old_col

    return new_col, new_col  # src == dst for in-place diff


# ---------------------------------------------------------------------------
# Scenario 5: non-frozen, sparse changes on a control with many fields
# ---------------------------------------------------------------------------


def _nonfrozen_sparse_changes(n_controls: int):
    """
    Each update only 1-2 fields change per control.  Measures _dirty-based
    Prop tracking overhead (Prop.__set__ → _dirty) vs the old __changes scan.
    """
    cards = []
    for i in range(n_controls):
        c = BenchCard(key=i, title=f"Card {i}", rank=i, score=float(i))
        cards.append(c)

    col = ft.Column(cards)
    object.__setattr__(col, "__prev_lists", {"controls": cards[:]})
    object.__setattr__(col, "__prev_dicts", {})
    object.__setattr__(col, "__prev_classes", {})

    # Mutate 2 fields on every card
    for c in cards:
        c.badge = "!"
        c.selected = not c.selected

    return col, col


# ---------------------------------------------------------------------------
# Scenario 6: sunflower (existing regression test scenario)
# ---------------------------------------------------------------------------


def _sunflower(count: int, max_seeds: int = 500):
    tau = math.pi * 2
    phi = (math.sqrt(5) + 1) / 2

    def make_controls(n_filled):
        ctrls = []
        for i in range(n_filled):
            theta = i * tau / phi
            r = math.sqrt(i) / 40
            ctrls.append(
                ft.Container(
                    key=i,
                    width=5,
                    height=5,
                    bgcolor=ft.Colors.ORANGE,
                    align=ft.Alignment(r * math.cos(theta), -r * math.sin(theta)),
                )
            )
        for j in range(n_filled, max_seeds):
            ctrls.append(
                ft.Container(
                    key=j,
                    width=5,
                    height=5,
                    bgcolor=ft.Colors.GREY_700,
                    align=ft.Alignment(
                        math.cos(tau * j / (max_seeds - 1)) * 0.9,
                        math.sin(tau * j / (max_seeds - 1)) * 0.9,
                    ),
                )
            )
        return ctrls

    old = ft.Stack(controls=make_controls(count))
    old._frozen = True
    new = ft.Stack(controls=make_controls(count + 10))
    return old, new


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    print(f"\n{'=' * 70}")
    print("object_patch benchmark")
    print(f"Python {sys.version.split()[0]}")
    print(f"{'=' * 70}\n")

    print("--- Scenario 1: frozen, all-keyed list (shuffled) ---")
    _bench("size=150", lambda: _frozen_all_keyed(150))
    _bench("size=300", lambda: _frozen_all_keyed(300))
    _bench("size=500", lambda: _frozen_all_keyed(500))

    print("\n--- Scenario 2: frozen, mixed keyed/unkeyed list (50% keyed) ---")
    _bench("size=150", lambda: _frozen_mixed_keyed(150))
    _bench("size=300", lambda: _frozen_mixed_keyed(300))
    _bench("size=500", lambda: _frozen_mixed_keyed(500))

    print("\n--- Scenario 3: frozen, many-field controls, few fields differ ---")
    _bench("100 controls x 20 fields, 2 changed", lambda: _frozen_many_fields(100))
    _bench("300 controls x 20 fields, 2 changed", lambda: _frozen_many_fields(300))

    print("\n--- Scenario 4: non-frozen, list rebuilt each update (keyed) ---")
    _bench("size=100", lambda: _nonfrozen_rebuilt_keyed(100))
    _bench("size=300", lambda: _nonfrozen_rebuilt_keyed(300))

    print("\n--- Scenario 5: non-frozen, sparse field changes ---")
    _bench(
        "100 controls, 2 fields changed each", lambda: _nonfrozen_sparse_changes(100)
    )
    _bench(
        "300 controls, 2 fields changed each", lambda: _nonfrozen_sparse_changes(300)
    )

    print("\n--- Scenario 6: sunflower (500 seeds, +10 per update) ---")
    _bench("250 filled", lambda: _sunflower(250))
    _bench("400 filled", lambda: _sunflower(400))

    print()


if __name__ == "__main__":
    main()
