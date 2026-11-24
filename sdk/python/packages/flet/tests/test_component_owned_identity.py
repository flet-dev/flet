"""Regression tests for #6776.

`ComponentOwned` and its subclasses (`Hook`, the concrete hooks and
`ObservableSubscription`) are lifecycle objects tracked in lists and matched with
`in` / `list.remove`. Their only declared fields are `InitVar`s or per-hook
payloads, so a generated `__eq__` makes distinct instances compare equal - which
made `_detach_observable_subscription` detach the wrong subscription and leak the
other. They must use identity equality (`eq=False`).
"""

import pytest

import flet as ft
from flet.components.component import Component
from flet.components.component_owned import ComponentOwned
from flet.components.hooks.hook import Hook
from flet.components.hooks.use_context import ContextHook
from flet.components.hooks.use_effect import EffectHook
from flet.components.hooks.use_memo import MemoHook
from flet.components.hooks.use_ref import MutableRef, RefHook
from flet.components.hooks.use_state import StateHook
from flet.components.observable import ObservableSubscription


class _Owner:
    """Minimal stand-in for a Component owner (only needs to be weak-referenceable)."""


class _Obs(ft.Observable):
    value: int = 0


def _make_pair(cls):
    """Build two distinct instances of a ComponentOwned subclass with equal fields."""
    owner = _Owner()
    if cls is ObservableSubscription:
        return cls(owner, _Obs()), cls(owner, _Obs())
    if cls is StateHook:
        return cls(owner, 5), cls(owner, 5)
    if cls is EffectHook:

        def setup():
            """Shared callable, so the two hooks differ only by identity."""

        return cls(owner, setup), cls(owner, setup)
    if cls is RefHook:
        return cls(owner, MutableRef(1)), cls(owner, MutableRef(1))
    return cls(owner), cls(owner)


# Every ComponentOwned subclass must repeat `eq=False`, because `@dataclass`
# regenerates `__eq__` and does not inherit the base class setting.
@pytest.mark.parametrize(
    "cls",
    [
        ComponentOwned,
        Hook,
        ContextHook,
        EffectHook,
        MemoHook,
        RefHook,
        StateHook,
        ObservableSubscription,
    ],
    ids=lambda c: c.__name__,
)
def test_component_owned_subclasses_use_identity_equality(cls):
    a, b = _make_pair(cls)

    assert a == a
    assert a != b
    # `in` and `remove` must operate on the exact instance.
    assert b not in [a]
    items = [a, b]
    items.remove(b)
    assert items == [a]
    # eq=False also restores object.__hash__, which @dataclass(eq=True) removes.
    assert cls.__hash__ is not None
    assert len({a, b}) == 2


def test_detach_removes_the_requested_subscription():
    """`_detach_observable_subscription` must untrack the exact instance passed."""
    component = Component(fn=lambda: None)
    obs_a, obs_b = _Obs(), _Obs()

    sub_a = component._attach_observable_subscription(obs_a)
    sub_b = component._attach_observable_subscription(obs_b)
    assert len(component._state.observable_subscriptions) == 2

    component._detach_observable_subscription(sub_b)

    # The bug removed sub_a here, leaving sub_a untracked and never disposed.
    tracked = component._state.observable_subscriptions
    assert len(tracked) == 1
    assert tracked[0] is sub_a


def test_unmount_disposes_every_attached_subscription():
    """No subscription may survive teardown, or it keeps updating a dead component."""
    component = Component(fn=lambda: None)
    obs_a, obs_b = _Obs(), _Obs()

    component._attach_observable_subscription(obs_a)
    sub_b = component._attach_observable_subscription(obs_b)

    # Mirrors use_state's update_subscription: detach one, then tear the rest down.
    component._detach_observable_subscription(sub_b)
    component._detach_observable_subscriptions()

    assert component._state.observable_subscriptions == []
    # Both observables must be free of listeners; sub_a leaked one before the fix.
    for obs in (obs_a, obs_b):
        listeners = getattr(obs, "_Observable__listeners_storage", ())
        assert len(listeners) == 0

    # Nothing is scheduled after teardown.
    obs_a.value = 1
    obs_b.value = 1
    assert not component._state.is_dirty
