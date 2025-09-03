from __future__ import annotations

import contextvars
import weakref
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar

from flet.controls.base_control import BaseControl, control


@dataclass
class StateCell:
    value: Any
    version: int = 0


@control("C")
class _Component(BaseControl):
    _fn: Callable[..., Any] = field(metadata={"skip": True})
    _args: tuple[Any, ...] = field(metadata={"skip": True})
    _kwargs: dict[str, Any] = field(metadata={"skip": True})
    _after_fn: Callable[..., Any] | None = field(default=None, metadata={"skip": True})
    _parent_component: weakref.ref[_Component] | None = field(
        default=None, metadata={"skip": True}
    )

    _state_cursor: int = 0
    _state: list[StateCell] = field(default_factory=list, metadata={"skip": True})

    _b: Any = None  # body

    def update(self):
        print("Component.update() called:", self)
        del self._frozen
        super().update()

    def before_update(self):
        print("_Component.before_update:", self._fn, self._args, self._kwargs)
        if self._b is None:
            r = Renderer(self)
            b = r.render(self._fn, *self._args, **self._kwargs)
            if self._after_fn:
                b = self._after_fn(b, *self._args, **self._kwargs)
            if isinstance(b, list):
                for item in b:
                    object.__setattr__(item, "_frozen", True)
            elif b:
                object.__setattr__(b, "_frozen", True)
            self._b = b

    def did_mount(self):
        return super().did_mount()

    def will_unmount(self):
        return super().will_unmount()


# -----------------------------
# Current renderer pointer (per task)
# -----------------------------

_CURRENT_RENDERER: contextvars.ContextVar[Renderer | None] = contextvars.ContextVar(
    "CURRENT_RENDERER", default=None
)


def _get_renderer() -> Renderer:
    r = _CURRENT_RENDERER.get()
    if r is None:
        raise RuntimeError(
            "No current renderer is set. Call via Renderer.render(...) "
            "or Renderer.with_context(...)."
        )
    return r


# -----------------------------
# Component decorator
# -----------------------------


def component(fn: Callable[..., Any]) -> Callable[..., Any]:
    """
    Marks a function as a component. When called, it will render through
    the *current* Renderer.
    """
    fn.__is_component__ = True

    def wrapper(*args, key=None, **kwargs):
        r = _get_renderer()
        return r._render_component(fn, args, kwargs, key=key)

    wrapper.__name__ = fn.__name__
    wrapper.__is_component__ = True
    return wrapper


# -----------------------------
# Renderer (all state is instance-bound)
# -----------------------------


class Renderer:
    """Owns fibers, stacks, and scheduling for a single session/page."""

    _ROOT_TOKEN = ("__root__",)

    def __init__(self, root_component):
        self._root_component = root_component
        self._render_stack: list[_Component] = []

    def with_context(self):
        """Context manager to make this renderer the 'current' one."""

        class _C:
            def __init__(_s, r: Renderer):
                _s._tok = None
                _s._r = r

            def __enter__(_s):
                _s._tok = _CURRENT_RENDERER.set(_s._r)
                return _s._r

            def __exit__(_s, exc_type, exc, tb):
                if _s._tok is not None:
                    _CURRENT_RENDERER.reset(_s._tok)

        return _C(self)

    def render(self, root_fn: Callable[..., Any], *args, **kwargs):
        # run with this renderer bound as current
        with self.with_context(), self._Frame(self, self._root_component):
            return root_fn(*args, **kwargs)

    class _Frame:
        """Context around entering a component; pushes/pops on renderer's stack."""

        def __init__(self, renderer: Renderer, c: _Component):
            self.r = renderer
            self.c = c
            print("\n\nFRAME CREATED:", self.c._fn.__name__)

        def __enter__(self):
            self.r._render_stack.append(self.c)
            return self.c

        def __exit__(self, exc_type, exc, tb):
            self.r._render_stack.pop()

    def _render_component(
        self,
        fn: Callable[..., Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        key=None,
    ):
        c = _Component(
            _fn=fn,
            _args=args,
            _kwargs=kwargs,
            _parent_component=weakref.ref(self._render_stack[-1]),
            key=key,
        )

        # (re)subscribe to observable args for this fiber
        # fiber.clear_subscriptions()
        # self._subscribe_observable_args(fiber, args, kwargs)

        with self._Frame(self, c):
            c._b = fn(*args, **kwargs)
            return c

    # def _subscribe_observable_args(
    #     self, fiber: Fiber, args: tuple[Any, ...], kwargs: dict[str, Any]
    # ):
    #     """
    #     If an arg is an Observable (duck-typed: has .subscribe),
    #     subscribe and mark this fiber dirty on notify.
    #     """

    #     def is_observable(o: Any) -> bool:
    #         return hasattr(o, "subscribe") and callable(o.subscribe)

    #     for a in args:
    #         if is_observable(a):
    #             self._attach_subscription(fiber, a)
    #     for v in kwargs.values():
    #         if is_observable(v):
    #             self._attach_subscription(fiber, v)

    def _attach_subscription(self, fiber: _Component, observable: Any):
        # Use weak refs to avoid cycles
        print("Attaching subscription to observable:", observable)
        rfiber = weakref.ref(fiber)
        rself = weakref.ref(self)

        def on_change(_sender, _field):
            print("Observable changed:", _sender, _field)
            r = rself()
            f = rfiber()
            if not r or not f:
                return
            r.mark_dirty(f)

        try:
            dispose = observable.subscribe(on_change)
            fiber._disposers.append(dispose)
        except Exception:
            # If it's not exactly our Observable but has compatible API,
            # ignore failures gracefully.
            pass

    def mark_dirty(self, component: _Component):
        print("Marking _Component as dirty:", _Component._i)
        # self._pending.add(fiber.identity)
        # cb = self._schedule_render_cb
        # if cb:
        #     with contextlib.suppress(Exception):
        #         cb()


# -----------------------------
# Hooks (renderer-aware via contextvar)
# -----------------------------


UseStateT = TypeVar("UseStateT")


def _current_component() -> _Component:
    r = _get_renderer()
    if not r._render_stack:
        raise RuntimeError("Hooks must be called inside a component render.")
    return r._render_stack[-1]


def use_state(initial: UseStateT) -> tuple[UseStateT, Callable[[UseStateT], None]]:
    component = _current_component()
    # r = _get_renderer()
    print("USE_STATE HOOK CALLED:", component)

    i = component._state_cursor
    component._state_cursor += 1

    if i >= len(component._state):
        component._state.append(StateCell(initial))

    cell = component._state[i]

    def set_state(new_value: Any):
        # shallow equality; swap to "is" or custom comparator if needed
        if new_value != cell.value:
            cell.value = new_value
            cell.version += 1
            component.update()

    return cell.value, set_state
