import weakref

import pytest

import flet as ft
from flet.components.component import Component, Renderer
from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page
from flet.controls.control_event import ControlEvent
from flet.messaging.protocol import configure_encode_object_for_msgpack


class FakeSession:
    def __init__(self):
        self.patch_calls: list[tuple[object, dict]] = []
        self.scheduled_updates: list[object] = []
        self.index: dict[int, object] = {}

    def patch_control(self, control, **kwargs):
        self.patch_calls.append((control, kwargs))
        control_id = getattr(control, "_i", None)
        if control_id is not None:
            self.index[control_id] = control

    def schedule_update(self, control):
        self.scheduled_updates.append(control)

    def schedule_effect(self, hook, is_cleanup):
        pass

    async def after_event(self, control):
        pass


def render_component(component: Component, page: ft.Page) -> None:
    component._state.hook_cursor = 0
    token = _context_page.set(page)
    try:
        renderer = Renderer(component)
        with renderer.with_context(), renderer._Frame(renderer, component):
            component.fn(*component.args, **component.kwargs)
    finally:
        _context_page.reset(token)


def create_page() -> tuple[ft.Page, FakeSession]:
    session = FakeSession()
    page = ft.Page(sess=session)
    page._dialogs._parent = weakref.ref(page)
    return page, session


@pytest.mark.asyncio
async def test_use_dialog_waits_for_dismiss_before_removing_dialog():
    page, session = create_page()
    show = True
    dismiss_calls: list[str] = []

    def body():
        ft.use_dialog(
            ft.AlertDialog(
                title=ft.Text("Hello"),
                on_dismiss=lambda e: dismiss_calls.append(e.name),
            )
            if show
            else None
        )

    component = Component(fn=body, args=(), kwargs={})

    render_component(component, page)

    assert session.scheduled_updates == [page._dialogs]
    assert len(page._dialogs.controls) == 1

    dialog = page._dialogs.controls[0]
    session.patch_calls.clear()
    session.scheduled_updates.clear()

    show = False
    render_component(component, page)

    assert page._dialogs.controls == [dialog]
    assert dialog.open is False
    assert session.patch_calls == [(dialog, {})]
    assert session.scheduled_updates == []

    await dialog.on_dismiss(ControlEvent(control=dialog, name="dismiss", data=None))

    assert page._dialogs.controls == []
    assert dismiss_calls == ["dismiss"]
    assert session.patch_calls[-1] == (page._dialogs, {})


@pytest.mark.asyncio
async def test_use_dialog_unmount_keeps_dialog_until_dismiss_event():
    page, session = create_page()
    dismiss_calls: list[str] = []

    def body():
        ft.use_dialog(
            ft.AlertDialog(
                title=ft.Text("Hello"),
                on_dismiss=lambda e: dismiss_calls.append(e.name),
            )
        )

    component = Component(fn=body, args=(), kwargs={})
    render_component(component, page)

    dialog = page._dialogs.controls[0]
    session.patch_calls.clear()
    session.scheduled_updates.clear()
    component._schedule_effect = lambda hook, is_cleanup=False: (
        hook.cleanup() if is_cleanup and hook.cleanup else None
    )

    component.will_unmount()

    assert page._dialogs.controls == [dialog]
    assert dialog.open is False
    assert session.patch_calls == [(dialog, {})]
    assert session.scheduled_updates == []

    await dialog.on_dismiss(ControlEvent(control=dialog, name="dismiss", data=None))

    assert page._dialogs.controls == []
    assert dismiss_calls == ["dismiss"]
    assert session.patch_calls[-1] == (page._dialogs, {})


@pytest.mark.asyncio
async def test_show_dialog_still_removes_dialog_on_dismiss():
    page, session = create_page()
    dismiss_calls: list[str] = []
    dialog = ft.AlertDialog(
        title=ft.Text("Hello"),
        on_dismiss=lambda e: dismiss_calls.append(e.name),
    )

    page.show_dialog(dialog)

    assert page._dialogs.controls == [dialog]
    assert dialog.open is True
    assert session.patch_calls == [(page._dialogs, {})]

    await dialog.on_dismiss(ControlEvent(control=dialog, name="dismiss", data=None))

    assert page._dialogs.controls == []
    assert dismiss_calls == ["dismiss"]
    assert session.patch_calls[-1] == (page._dialogs, {})


def test_prepare_dialog_does_not_store_callbacks_in_serialized_fields():
    page, _ = create_page()
    dialog = ft.AlertDialog(
        title=ft.Text("Hello"),
        on_dismiss=lambda e: None,
    )

    page._prepare_dialog(dialog)

    encoded = configure_encode_object_for_msgpack(BaseControl)(dialog)

    assert encoded["on_dismiss"] is True
    assert "_internals" not in encoded
