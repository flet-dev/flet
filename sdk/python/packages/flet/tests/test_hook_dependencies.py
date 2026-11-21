"""Observable lists and dicts as `use_memo` and `use_effect` dependencies."""

import flet as ft
from flet.components.component import Component, Renderer


@ft.observable
class Store:
    def __init__(self):
        self.items = [1, 2]
        self.groups = [[1], [2]]
        self.totals = {"a": 1}
        self.name = "store"


def render(component: Component) -> None:
    component._state.hook_cursor = 0
    renderer = Renderer(component)
    with renderer.with_context(), renderer._Frame(renderer, component):
        component.fn(*component.args, **component.kwargs)


def memo_counter(deps_of):
    """A component that memoizes on `deps_of()` and counts the recomputes."""
    calls = []

    def body():
        ft.use_memo(lambda: calls.append(1), deps_of())

    return Component(fn=body, args=(), kwargs={}), calls


def test_memo_recomputes_after_list_changes_in_place():
    store = Store()
    component, calls = memo_counter(lambda: [store.items])

    render(component)
    render(component)
    assert len(calls) == 1

    store.items.append(3)
    render(component)
    assert len(calls) == 2

    render(component)
    assert len(calls) == 2


def test_memo_recomputes_after_item_replaced_or_removed():
    store = Store()
    component, calls = memo_counter(lambda: [store.items])
    render(component)

    store.items[0] = 10
    render(component)
    store.items.pop()
    render(component)

    assert len(calls) == 3


def test_memo_recomputes_after_nested_list_changes():
    store = Store()
    component, calls = memo_counter(lambda: [store.groups])
    render(component)

    store.groups[0].append(5)
    render(component)

    assert len(calls) == 2


def test_memo_recomputes_after_dict_changes_in_place():
    store = Store()
    component, calls = memo_counter(lambda: [store.totals])
    render(component)

    store.totals["b"] = 2
    render(component)

    assert len(calls) == 2


def test_memo_ignores_changes_to_other_fields():
    store = Store()
    component, calls = memo_counter(lambda: [store.items])
    render(component)

    store.name = "renamed"
    store.totals["b"] = 2
    render(component)

    assert len(calls) == 1


def test_memo_compares_different_lists_by_items():
    store = Store()
    component, calls = memo_counter(lambda: [store.items])
    render(component)

    store.items = [1, 2]  # a new list with the same items
    render(component)
    assert len(calls) == 1

    store.items = [1, 2, 3]
    render(component)
    assert len(calls) == 2


def test_memo_recomputes_after_manual_notify():
    store = Store()
    component, calls = memo_counter(lambda: [store.items])
    render(component)

    store.notify()
    render(component)

    assert len(calls) == 2


def test_effect_reruns_after_list_changes_in_place():
    store = Store()
    scheduled = []

    def body():
        ft.use_effect(lambda: None, [store.items])

    component = Component(fn=body, args=(), kwargs={})
    component._schedule_effect = (  # type: ignore[method-assign]
        lambda hook, is_cleanup=False: scheduled.append(is_cleanup)
    )
    render(component)
    component._state.mounted = True

    render(component)
    component._run_render_effects()
    assert scheduled == []

    store.items.append(3)
    render(component)
    component._run_render_effects()
    assert scheduled == [False]
