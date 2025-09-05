from __future__ import annotations

import contextvars
import weakref
from dataclasses import dataclass, field
from typing import Any, Callable, TypeVar

from flet.components.observable import Observable
from flet.controls.base_control import BaseControl, control


@control("C")
class _Component(BaseControl):
    _fn: Callable[..., Any] = field(metadata={"skip": True})
    _args: tuple[Any, ...] = field(metadata={"skip": True})
    _kwargs: dict[str, Any] = field(metadata={"skip": True})
    _parent_component: weakref.ref[_Component] | None = field(
        default=None, metadata={"skip": True}
    )

    _b: Any = None  # body

    def schedule_update(self):
        # print("Schedule update:", self._i)
        self.page.get_session().schedule_update(self)

    def update(self):
        print("Component.update() called:", self._i)

        # new rendering
        self._reset_hook_cursor()
        # self._detach_subscriptions()
        b = Renderer(self).render(self._fn, *self._args, **self._kwargs)

        # print("\n\n** UPDATE ***:\n\n", b)

        # patch component
        self.page.get_session().patch_control(
            prev_control=self._b, control=b, parent=self, path=["_b"], frozen=True
        )

        self._b = b

    def before_update(self):
        # print(
        #     f"_Component.before_update: {self._i}", self._fn, self._args, self._kwargs
        # )
        if self._b is None:
            self._reset_hook_cursor()
            self._detach_subscriptions()
            self._subscribe_observable_args(self._args, self._kwargs)
            # print("DISPOSERS:", len(self.get_subscription_disposers()))
            b = Renderer(self).render(self._fn, *self._args, **self._kwargs)
            # if self._after_fn:
            #     b = self._after_fn(b, *self._args, **self._kwargs)
            # print("\n\n*** NEW ***:\n\n", b)
            if isinstance(b, list):
                for item in b:
                    object.__setattr__(item, "_frozen", True)
            elif b:
                object.__setattr__(b, "_frozen", True)
            self._b = b

    def _subscribe_observable_args(self, args: tuple[Any, ...], kwargs: dict[str, Any]):
        for a in args:
            if isinstance(a, Observable):
                self._attach_subscription(a)
        for v in kwargs.values():
            if isinstance(v, Observable):
                self._attach_subscription(v)

    def _attach_subscription(self, observable: Observable):
        # Use weak refs to avoid cycles
        # print("Attaching subscription to observable:", observable)
        rself = weakref.ref(self)

        def on_change(_sender, _field):
            # print("Observable changed:", _sender, _field)
            r = rself()
            if not r:
                return
            r.schedule_update()

        dispose = observable.subscribe(on_change)
        self.get_subscription_disposers().append(dispose)

    def get_subscription_disposers(self):
        return self._state.setdefault("_subscription_disposers", [])

    def _detach_subscriptions(self):
        for dispose in self.get_subscription_disposers():
            dispose()
        self.get_subscription_disposers().clear()

    def _reset_hook_cursor(self):
        self._state["_hook_cursor"] = 0

    def use_hook(self, default: Callable[..., Any]):
        hook_cursor = self._state.setdefault("_hook_cursor", 0)
        hooks = self._state.setdefault("_hooks", [])

        i = hook_cursor
        hook_cursor += 1

        if i >= len(hooks):
            hooks.append(default())

        self._state["_hook_cursor"] = hook_cursor
        return hooks[i]

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

    def __init__(self, root_component=None):
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

        def __init__(self, renderer: Renderer, c: _Component | None = None):
            self.r = renderer
            self.c = c
            # if self.c:
            #     print("\n\nFRAME CREATED:", self.c._fn.__name__)

        def __enter__(self):
            if self.c:
                self.r._render_stack.append(self.c)
            return self.c

        def __exit__(self, exc_type, exc, tb):
            if self.c:
                self.r._render_stack.pop()

    def _render_component(
        self,
        fn: Callable[..., Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
        key=None,
    ):
        parent_component = len(self._render_stack) and self._render_stack[-1]
        # print("\n\nParent component:", parent_component)

        c = _Component(
            _fn=fn,
            _args=args,
            _kwargs=kwargs,
            _parent_component=weakref.ref(parent_component)
            if parent_component
            else None,
            key=key,
        )

        # (re)subscribe to observable args for this fiber
        # fiber.clear_subscriptions()
        # self._subscribe_observable_args(fiber, args, kwargs)

        # if len(self._render_stack) < 1:
        #     with self._Frame(self, c):
        #         c._b = fn(*args, **kwargs)
        #         return c
        return c


# -----------------------------
# Hooks (renderer-aware via contextvar)
# -----------------------------


@dataclass
class StateCell:
    value: Any
    version: int = 0


UseStateT = TypeVar("UseStateT")


def _current_component() -> _Component:
    r = _get_renderer()
    if not r._render_stack:
        raise RuntimeError("Hooks must be called inside a component render.")
    return r._render_stack[-1]


def use_state(initial: UseStateT) -> tuple[UseStateT, Callable[[UseStateT], None]]:
    component = _current_component()
    hook = component.use_hook(lambda: StateCell(initial))

    def set_state(new_value: Any):
        # shallow equality; swap to "is" or custom comparator if needed
        if new_value != hook.value:
            hook.value = new_value
            hook.version += 1
            component.schedule_update()

    return hook.value, set_state
