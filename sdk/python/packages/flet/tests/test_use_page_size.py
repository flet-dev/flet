"""`ft.use_page_size()` and the page's resize listeners."""

import weakref

import pytest

import flet as ft
from flet.components.component import Component, Renderer
from flet.components.hooks.use_effect import EffectHook
from flet.controls.base_page import PageResizeEvent
from flet.controls.context import _context_page


class FakeSession:
    def patch_control(self, control, **kwargs):
        pass

    def schedule_update(self, control):
        pass

    def schedule_effect(self, hook, is_cleanup):
        pass

    async def after_event(self, control):
        pass

    @property
    def index(self):
        return {}


def create_page(width=1000, height=800) -> ft.Page:
    session = FakeSession()
    page = ft.Page(sess=session)
    vars(page)["_test_session"] = session  # the page holds it weakly
    page._dialogs._parent = weakref.ref(page)
    page.width = width
    page.height = height
    return page


def resize(page: ft.Page, width: float, height: float) -> None:
    page.width, page.height = width, height
    page.before_event(
        PageResizeEvent(name="resize", control=page, width=width, height=height)
    )


class Harness:
    """Renders a component by hand, runs its effects and counts re-renders."""

    def __init__(self, page: ft.Page, body):
        self.page = page
        self.result = None
        self.updates = 0

        def fn():
            self.result = body()

        self.component = Component(fn=fn, args=(), kwargs={})
        self.component._schedule_update = self._count_update  # type: ignore[method-assign]

    def _count_update(self):
        self.updates += 1

    def render(self):
        self.component._state.hook_cursor = 0
        token = _context_page.set(self.page)
        try:
            renderer = Renderer(self.component)
            with renderer.with_context(), renderer._Frame(renderer, self.component):
                self.component.fn()
        finally:
            _context_page.reset(token)
        return self.result

    def mount(self):
        self.render()
        self.component._state.mounted = True
        for hook in self.component._state.hooks:
            if isinstance(hook, EffectHook):
                hook._returned_cleanup = hook.setup()
        return self.result

    def unmount(self):
        for hook in self.component._state.hooks:
            if isinstance(hook, EffectHook) and hook._returned_cleanup:
                hook._returned_cleanup()


def test_returns_page_size_and_rerenders_on_resize():
    page = create_page(1000, 800)
    h = Harness(page, ft.use_page_size)

    assert h.mount() == ft.Size(1000, 800)

    resize(page, 500, 700)
    assert h.updates == 1
    assert h.render() == ft.Size(500, 700)


def test_select_rerenders_only_when_selected_value_changes():
    page = create_page(1000, 800)
    h = Harness(page, lambda: ft.use_page_size(lambda s: s.width < 600))

    assert h.mount() is False

    resize(page, 900, 800)
    resize(page, 700, 600)
    assert h.updates == 0

    resize(page, 500, 600)
    assert h.updates == 1
    assert h.render() is True


def test_new_select_applies_on_render_and_on_the_next_resize():
    page = create_page(700, 800)
    breakpoint = 600

    def layout(limit):
        return ft.use_page_size(lambda s: s.width < limit)

    h = Harness(page, lambda: layout(breakpoint))
    assert h.mount() is False

    breakpoint = 800
    assert h.render() is True

    resize(page, 900, 800)
    assert h.updates == 1
    assert h.render() is False


def test_select_can_return_a_callback():
    def compact():
        pytest.fail("The hook invoked the compact callback")

    def wide():
        pytest.fail("The hook invoked the wide callback")

    def select(size):
        return compact if size.width < 600 else wide

    page = create_page(700, 800)
    h = Harness(page, lambda: ft.use_page_size(select))
    assert h.mount() is wide
    resize(page, 650, 800)
    assert h.updates == 0

    resize(page, 500, 800)
    assert h.updates == 1
    assert h.render() is compact


@pytest.mark.asyncio
@pytest.mark.parametrize("with_handler", [True, False], ids=["on_resize", "no_handler"])
async def test_resize_event_reaches_every_component_and_on_resize(with_handler):
    page = create_page(1000, 800)
    handler_calls = []
    if with_handler:
        page.on_resize = lambda e: handler_calls.append((e.width, e.height))
    first = Harness(page, ft.use_page_size)
    second = Harness(page, lambda: ft.use_page_size(lambda s: s.width))
    first.mount()
    second.mount()

    page.width, page.height = 400, 800
    await page._trigger_event("resize", {"width": 400, "height": 800})

    assert first.updates == 1
    assert second.updates == 1
    assert second.render() == 400
    assert handler_calls == ([(400, 800)] if with_handler else [])


def test_unmount_removes_listener():
    page = create_page(1000, 800)
    h = Harness(page, ft.use_page_size)
    h.mount()
    h.unmount()

    resize(page, 400, 800)

    assert h.updates == 0
    assert vars(page)["_resize_listeners"] == []


def test_missing_page_size_reads_as_zero():
    page = create_page(None, None)
    h = Harness(page, ft.use_page_size)

    assert h.mount() == ft.Size(0, 0)
