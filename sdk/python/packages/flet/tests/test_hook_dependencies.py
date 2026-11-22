"""Observable lists and dicts as `use_memo` and `use_effect` dependencies."""

import pytest

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


@pytest.fixture(params=["memo", "effect"])
def render_hook(request):
    """Return a render function that counts memo calculations or effect setups."""

    def create(dependency):
        runs = []

        def body():
            hook = ft.use_memo if request.param == "memo" else ft.use_effect
            hook(lambda: runs.append(1), [dependency()])

        component = Component(fn=body, args=(), kwargs={})
        component._schedule_effect = lambda hook, is_cleanup=False: hook.setup()

        def render_and_count():
            render(component)
            if component._state.mounted:
                component._run_render_effects()
            else:
                component._state.mounted = True
                component._run_mount_effects()
            return len(runs)

        return render_and_count

    return create


def test_mutation_followed_by_equal_copy(render_hook):
    store = Store()
    count = render_hook(lambda: store.items)
    assert count() == 1
    store.items.append(3)
    store.items = list(store.items)
    assert count() == 2
    assert count() == 2


def test_equal_replacement_becomes_the_watched_collection(render_hook):
    store = Store()
    count = render_hook(lambda: store.items)
    assert count() == 1
    old_items = store.items
    store.items = list(old_items)
    assert count() == 1
    old_items.append(3)
    assert count() == 1
    store.notify()
    assert count() == 2


@pytest.mark.parametrize("field", ["items", "totals"])
def test_equal_plain_and_observable_dependencies(render_hook, field):
    store = Store()
    value = getattr(store, field)
    count = render_hook(lambda: value)
    assert count() == 1
    value = value.copy()
    assert count() == 1
    value = getattr(store, field)
    assert count() == 1


def test_nested_dependency_tracks_only_reachable_collections(render_hook):
    store = Store()
    shared = []
    group = {"left": shared, "right": shared}
    group["cycle"] = group
    store.groups = [group, []]
    count = render_hook(lambda: store.groups[0])
    assert count() == 1
    store.groups[1].append(1)
    assert count() == 1
    watched = store.groups[0]
    detached = watched.pop("left")
    assert count() == 2
    detached.append(1)  # still reachable through "right"
    assert count() == 3
    del watched["right"]
    assert count() == 4
    detached.append(2)
    assert count() == 4


def test_false_valued_owner_notifies_and_invalidates_nested_hooks(render_hook):
    @ft.observable
    class EmptyStore:
        def __bool__(self):
            return False

    store = EmptyStore()
    store.items = []
    count = render_hook(lambda: store.items)
    changes = []

    def listener(sender, field):
        changes.append(field)

    store.subscribe(listener)
    assert count() == 1
    store.items.append({})
    assert count() == 2
    store.items[0]["a"] = 1
    assert count() == 3
    store.notify()
    assert count() == 4
    assert changes == ["items", "items", None]
