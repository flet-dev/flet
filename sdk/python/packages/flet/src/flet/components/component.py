from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar

# -----------------------------
# Core fiber/runtime structures
# -----------------------------


@dataclass
class StateCell:
    value: Any
    version: int = 0


@dataclass
class Fiber:
    fn: Callable[..., Any]  # component function
    identity: tuple[Any, ...]  # (parent_id, fn, key)
    parent_id: int | None
    key: Any
    state: list[StateCell] = field(default_factory=list)
    cursor: int = 0  # where the next hook reads/writes
    seen: bool = False  # mark in current render
    children_count: int = 0  # incremental index for child identities


# Global, single-threaded “renderer” state
_fibers: dict[tuple[Any, ...], Fiber] = {}
_render_stack: list[Fiber] = []
_schedule_render: Callable[[], None] | None = None


def install_scheduler(schedule_render: Callable[[], None]) -> None:
    """Give the runtime a way to trigger a re-render."""
    global _schedule_render
    _schedule_render = schedule_render


# -----------------------------
# Component decorator
# -----------------------------


def component(fn: Callable[..., Any]) -> Callable[..., Any]:
    fn.__is_component__ = True  # marker (useful if you want to distinguish later)

    def wrapper(*args, key=None, **kwargs):
        return _render_component(fn, args, kwargs, key=key)

    wrapper.__name__ = fn.__name__
    wrapper.__is_component__ = True
    return wrapper


# -----------------------------
# Rendering + reconciliation
# -----------------------------


class _Frame:
    """Context around entering a component (push/pop on _render_stack)."""

    def __init__(self, fiber: Fiber):
        self.fiber = fiber
        print("ENTER FRAME:", fiber.identity)

    def __enter__(self):
        self.fiber.cursor = 0
        self.fiber.children_count = 0
        self.fiber.seen = True
        _render_stack.append(self.fiber)
        return self.fiber

    def __exit__(self, exc_type, exc, tb):
        _render_stack.pop()


def _render_component(fn: Callable[..., Any], args: tuple, kwargs: dict, key=None):
    parent = _render_stack[-1] if _render_stack else None

    auto_index = parent.children_count if parent else 0
    if parent:
        parent.children_count += 1

    # use parent's stable identity token
    parent_token = parent.identity if parent else _ROOT_ID
    child_key = key if key is not None else auto_index
    identity = (parent_token, fn, child_key)

    fiber = _fibers.get(identity)
    if fiber is None:
        fiber = Fiber(
            fn=fn,
            identity=identity,
            parent_id=id(parent) if parent else None,  # optional, not used for identity
            key=key,
        )
        _fibers[identity] = fiber

    with _Frame(fiber):
        return fn(*args, **kwargs)


# 1) Make a single, stable synthetic root identity
_ROOT_ID = ("__root__",)  # constant, hashable

# Create one synthetic root fiber and reuse it
_root_fiber: Fiber | None = None


def render(root_fn: Callable[..., Any], *args, **kwargs):
    global _root_fiber

    # mark all unseen
    for f in _fibers.values():
        f.seen = False

    # create once; reuse each render so identity is stable
    if _root_fiber is None:
        _root_fiber = Fiber(
            fn=lambda: None,
            identity=_ROOT_ID,
            parent_id=None,
            key="__root__",
        )

    with _Frame(_root_fiber):
        tree = _render_component(root_fn, args, kwargs, key="__app__")

    _sweep_unseen()
    return tree


def _sweep_unseen():
    """Remove state for fibers not visited this render (simple global mark/sweep)."""
    # Optional: two-pass to avoid mutating dict during iteration
    to_delete = [identity for identity, f in _fibers.items() if not f.seen]
    for identity in to_delete:
        print("SWEEPING:", identity)
        del _fibers[identity]


# -----------------------------
# Hooks
# -----------------------------


def _current_fiber() -> Fiber:
    if not _render_stack:
        raise RuntimeError("Hooks must be called inside a component render.")
    return _render_stack[-1]


UseStateT = TypeVar("UseStateT")


def use_state(initial: UseStateT) -> tuple[UseStateT, Callable[[UseStateT], None]]:
    fiber = _current_fiber()
    i = fiber.cursor
    fiber.cursor += 1

    # Grow the state list as needed
    if i >= len(fiber.state):
        fiber.state.append(StateCell(initial))

    cell = fiber.state[i]

    def set_state(new_value: Any):
        # Shallow equality; customize if needed
        if new_value != cell.value:
            cell.value = new_value
            cell.version += 1
            if _schedule_render:
                _schedule_render()

    return cell.value, set_state
