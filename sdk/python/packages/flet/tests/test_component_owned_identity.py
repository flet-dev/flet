"""Regression tests for #6776.

`ComponentOwned` and its subclasses (`Hook`, `ObservableSubscription`) are
lifecycle objects tracked in lists and matched with ``in`` / ``list.remove``.
They are dataclasses whose only declared fields are ``InitVar``s, so a generated
``__eq__`` compares no fields and makes every instance compare equal — which made
``_detach_observable_subscription`` detach the wrong subscription (a leak). They
must use identity equality (``eq=False``).
"""

import flet as ft
from flet.components.component_owned import ComponentOwned
from flet.components.hooks.hook import Hook
from flet.components.observable import ObservableSubscription


class _Owner:
    """Minimal stand-in for a Component owner (only needs to be weak-referenceable)."""


class _Obs(ft.Observable):
    value: int = 0


def test_component_owned_uses_identity_equality():
    owner = _Owner()
    a = ComponentOwned(owner)
    b = ComponentOwned(owner)
    assert a != b
    assert a == a
    assert b not in [a]
    assert hash(a) != hash(b)


def test_hook_uses_identity_equality():
    owner = _Owner()
    h1 = Hook(owner)
    h2 = Hook(owner)
    assert h1 != h2
    # `in` and `remove` must operate on the exact instance.
    hooks = [h1, h2]
    assert h1 in hooks
    hooks.remove(h2)
    assert hooks == [h1]
    assert h2 not in hooks


def test_observable_subscription_detaches_the_correct_instance():
    owner = _Owner()
    s1 = ObservableSubscription(owner, _Obs())
    s2 = ObservableSubscription(owner, _Obs())

    assert s1 != s2
    assert s2 not in [s1]

    subs = [s1, s2]
    # Removing s2 must leave s1 attached (the bug removed s1 instead).
    subs.remove(s2)
    assert s1 in subs
    assert s2 not in subs
    assert len(subs) == 1
