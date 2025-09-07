from __future__ import annotations

import contextvars
import logging
import weakref
from dataclasses import dataclass, field
from typing import Any, Callable

from flet.components.hooks import EffectHook
from flet.components.observable import Observable
from flet.controls.base_control import BaseControl, control
from flet.controls.context import context

logger = logging.getLogger("flet_components")
logger.setLevel(logging.INFO)


@dataclass
class _ComponentState:
    hooks: list[Any] = field(default_factory=list)
    hook_cursor: int = 0
    mounted: bool = False
    is_dirty: bool = False
    subscription_disposers: list[Callable[[], Any]] = field(default_factory=list)
    last_args: tuple[Any, ...] = field(default_factory=tuple)
    last_kwargs: dict[str, Any] = field(default_factory=dict)
    last_b: Any = None

    def change_owner(self, new_owner: Any):
        # change owner for all disposers
        # for disposer in self.subscription_disposers:
        #     if hasattr(disposer, "change_owner"):
        #         disposer.change_owner(new_owner)
        pass


@control("C")
class Component(BaseControl):
    fn: Callable[..., Any] = field(metadata={"skip": True})
    args: tuple[Any, ...] = field(default_factory=tuple, metadata={"skip": True})
    kwargs: dict[str, Any] = field(default_factory=dict, metadata={"skip": True})
    _parent_component: weakref.ref[Component] | None = field(
        default=None, metadata={"skip": True}
    )

    _state: _ComponentState = field(
        default_factory=_ComponentState, metadata={"skip": True}
    )

    _b: Any = None  # body

    def _migrate_state(self, other: BaseControl):
        super()._migrate_state(other)
        if not isinstance(other, Component):
            return
        self._state = other._state
        self._state.change_owner(self)

    def update(self):
        logger.debug(
            "%s.update(), memo: %s",
            self,
            self._is_memo(),
        )

        logger.debug("self.parent: %s", self.parent)

        # new rendering
        self._reset_hook_cursor()
        self._detach_subscriptions()
        self._subscribe_observable_args(self.args, self.kwargs)

        b = Renderer(self).render(self.fn, *self.args, **self.kwargs)

        for item in b if isinstance(b, list) else [b] if b is not None else []:
            object.__setattr__(item, "_frozen", True)

        if self._is_memo() and b is not None:
            logger.debug("%s(%d).update(): memoizing", self.fn.__name__, self._i)
            self._state.last_b = b
            self._state.last_args = self.args
            self._state.last_kwargs = self.kwargs

        # patch component
        if b is not None:
            context.page.get_session().patch_control(
                prev_control=self._b, control=b, parent=self, path=["_b"], frozen=True
            )

        self._b = b
        self._run_render_effects()

    def before_update(self):
        logger.debug(
            "%s.before_update(), memo: %s",
            self,
            self._is_memo(),
        )
        is_dirty = self._state.is_dirty
        self._state.is_dirty = False

        self._detach_subscriptions()
        self._subscribe_observable_args(self.args, self.kwargs)

        if (
            self._is_memo()
            and not is_dirty
            and self._compare_args(
                self._state.last_args, self._state.last_kwargs, self.args, self.kwargs
            )
        ):
            logger.debug("%s.before_update(): skipping (memo)", self)
            self._b = self._state.last_b

            # restore parent?
            print("\n\nSELF.PARENT:", self.parent)
            for item in self._b if isinstance(self._b, list) else [self._b]:
                object.__setattr__(item, "_parent", weakref.ref(self))
            return

        self._reset_hook_cursor()
        b = Renderer(self).render(self.fn, *self.args, **self.kwargs)

        for item in b if isinstance(b, list) else [b] if b is not None else []:
            object.__setattr__(item, "_frozen", True)

        if self._is_memo() and b is not None:
            logger.debug("%s.before_update(): memoizing", self)
            self._state.last_b = b
            self._state.last_args = self.args
            self._state.last_kwargs = self.kwargs

        self._b = b
        self._run_render_effects()

    def _is_memo(self):
        return getattr(self.fn, "__is_memo__", False)

    def _schedule_update(self):
        logger.debug("%s.schedule_update()", self)
        self._state.is_dirty = True
        context.page.get_session().schedule_update(self)

    def _schedule_effect(self, hook: EffectHook, fn: Callable):
        logger.debug("%s.schedule_effect(%s)", self, fn.__name__)
        context.page.get_session().schedule_effect(hook, fn)

    def _subscribe_observable_args(self, args: tuple[Any, ...], kwargs: dict[str, Any]):
        for a in args:
            if isinstance(a, Observable):
                self._attach_subscription(a)
        for v in kwargs.values():
            if isinstance(v, Observable):
                self._attach_subscription(v)

    def _attach_subscription(self, observable: Observable):
        # Use weak refs to avoid cycles
        logger.debug("%d._attach_subscription(%s)", self, observable)
        rself = weakref.ref(self)

        def on_change(_sender, _field):
            r = rself()
            if not r:
                return
            r._schedule_update()

        dispose = observable.subscribe(on_change)
        self._state.subscription_disposers.append(dispose)
        return dispose

    def _detach_subscription(self, dispose: Callable[[], Any]):
        if dispose in self._state.subscription_disposers:
            dispose()
            self._state.subscription_disposers.remove(dispose)

    def _detach_subscriptions(self):
        for dispose in self._state.subscription_disposers:
            dispose()
        self._state.subscription_disposers.clear()

    def _reset_hook_cursor(self):
        self._state.hook_cursor = 0

    def use_hook(self, default: Callable[..., Any]):
        hook_cursor = self._state.hook_cursor

        i = hook_cursor
        hook_cursor += 1

        if i >= len(self._state.hooks):
            self._state.hooks.append(default())

        self._state.hook_cursor = hook_cursor
        return self._state.hooks[i]

    def _run_mount_effects(self):
        logger.debug("%s._run_mount_effects()", self)
        for hook in self._state.hooks:
            if isinstance(hook, EffectHook):
                # all effects are running on mount
                self._schedule_effect(hook, hook.fn)

    def _run_render_effects(self):
        logger.debug("%s._run_render_effects()", self)
        if not self._state.mounted:
            return
        for hook in self._state.hooks:
            if isinstance(hook, EffectHook) and hook.deps != []:
                if callable(hook.cleanup):
                    self._schedule_effect(hook, hook.cleanup)
                if (
                    hook.deps is None
                    or hook.prev_deps is None
                    or hook.deps != hook.prev_deps
                ):
                    self._schedule_effect(hook, hook.fn)

    def _run_unmount_effects(self):
        logger.debug("%s._run_unmount_effects()", self)
        for hook in self._state.hooks:
            # all effects are running on unmount
            if isinstance(hook, EffectHook) and callable(hook.cleanup):
                self._schedule_effect(hook, hook.cleanup)

    def did_mount(self):
        super().did_mount()
        self._state.mounted = True
        self._run_mount_effects()

    def will_unmount(self):
        super().will_unmount()
        self._state.mounted = False
        self._detach_subscriptions()
        self._run_unmount_effects()

    def _compare_args(
        self,
        prev_args: tuple[Any, ...],
        prev_kwargs: dict[str, Any],
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ):
        if len(prev_args) != len(args):
            return False
        for pa, a in zip(prev_args, args):
            if (
                not isinstance(pa, type(a))
                or (
                    isinstance(pa, Observable)
                    and isinstance(a, Observable)
                    and pa.__version__ != a.__version__
                )
                or pa != a
            ):
                return False
        if len(prev_kwargs) != len(kwargs):
            return False
        for k, v in kwargs.items():
            if k not in prev_kwargs or (
                not isinstance(prev_kwargs[k], type(v))
                or (
                    prev_kwargs[k] is v
                    and isinstance(prev_kwargs[k], Observable)
                    and isinstance(v, Observable)
                    and prev_kwargs[k].__version__ != v.__version__
                )
                or prev_kwargs[k] != v
            ):
                return False
        return True

    def __str__(self):
        return f"{self._c}:{self.fn.__name__}({self._i} - {id(self)})"


#
# Component decorator
#


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
    wrapper.__component_impl__ = fn
    return wrapper


#
# Renderer
#


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


def current_component() -> Component:
    r = _get_renderer()
    if not r._render_stack:
        raise RuntimeError("Hooks must be called inside a component render.")
    return r._render_stack[-1]


class Renderer:
    """Owns fibers, stacks, and scheduling for a single session/page."""

    _ROOT_TOKEN = ("__root__",)

    def __init__(self, root_component=None):
        self._root_component = root_component
        self._render_stack: list[Component] = []

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

        def __init__(self, renderer: Renderer, c: Component | None = None):
            self.r = renderer
            self.c = c

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

        if not hasattr(fn, "__is_component__"):
            raise ValueError(f"Function {fn} is not a component (missing @component?)")

        c = Component(
            fn=fn,
            args=args,
            kwargs=kwargs,
            _parent_component=weakref.ref(parent_component)
            if parent_component
            else None,
            key=key,
        )
        c._frozen = True

        # (re)subscribe to observable args for this fiber
        # fiber.clear_subscriptions()
        # self._subscribe_observable_args(fiber, args, kwargs)

        # if len(self._render_stack) < 1:
        #     with self._Frame(self, c):
        #         c._b = fn(*args, **kwargs)
        #         return c
        return c
