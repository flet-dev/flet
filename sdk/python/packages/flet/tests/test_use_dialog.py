import asyncio
import weakref
from dataclasses import dataclass

import pytest

import flet as ft
from flet.components.component import Component, Renderer
from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page
from flet.controls.control_event import ControlEvent
from flet.messaging.connection import Connection
from flet.messaging.protocol import ClientAction, configure_encode_object_for_msgpack
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


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


class _RecordingConnection(Connection):
    def __init__(self):
        super().__init__()
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)


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


async def flush_async(turns: int = 5) -> None:
    for _ in range(turns):
        await asyncio.sleep(0)


def crash_messages(conn: _RecordingConnection):
    return [m for m in conn.messages if m.action == ClientAction.SESSION_CRASHED]


def find_filled_button(session: Session, label: str) -> ft.FilledButton:
    matches = [
        c
        for c in session.index.values()
        if isinstance(c, ft.FilledButton) and c.content == label
    ]
    assert len(matches) == 1
    return matches[0]


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
    # Dismiss patches the dialog directly — `open=False` is a single op on
    # the dialog's own `_i`, which both (a) avoids a list-diff on
    # `_dialogs.controls` (whose `__prev_lists` snapshot may be out of
    # sync after an intervening frozen-diff `_i` migration), and (b) gives
    # Flutter an unambiguous "this dialog is closing" signal.
    assert len(session.patch_calls) == 1
    assert session.patch_calls[0] == (dialog, {})

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
    # Unmount cleanup patches the dialog directly — same approach as the
    # regular dismiss path, for the same reason.
    assert len(session.patch_calls) == 1
    assert session.patch_calls[0] == (dialog, {})

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


@pytest.mark.asyncio
async def test_use_dialog_dismiss_and_show_in_same_tick_each_emit_their_own_patch():
    """Regression: two sibling `use_dialog` hosts rendering in the same tick —
    one dismissing, one showing — each emit their own patch:
    - The dismissing host patches its dialog directly with `open=False`.
    - The showing host appends to `_dialogs.controls` and schedules a
      `_dialogs` update to flush the new entry to Flutter.

    These are non-conflicting writers (disjoint `_i`s on the Dart side),
    so landing them as separate messages is safe.
    """
    page, session = create_page()
    alert_open = True
    toast_text: str | None = None

    def alert_host():
        ft.use_dialog(ft.AlertDialog(title=ft.Text("alert")) if alert_open else None)

    def toast_host():
        ft.use_dialog(ft.SnackBar(content=ft.Text(toast_text)) if toast_text else None)

    alert_c = Component(fn=alert_host, args=(), kwargs={})
    toast_c = Component(fn=toast_host, args=(), kwargs={})

    # Initial render: alert shown, toast absent.
    render_component(alert_c, page)
    render_component(toast_c, page)

    alert_dialog = page._dialogs.controls[0]
    assert alert_dialog.open is True
    session.patch_calls.clear()
    session.scheduled_updates.clear()

    # Same-tick flip: dismiss the alert AND show the toast.
    alert_open = False
    toast_text = "hello"
    render_component(alert_c, page)
    render_component(toast_c, page)

    # The alert is still present (waiting for Flutter's dismiss event) but
    # its `open` is False.
    assert alert_dialog in page._dialogs.controls
    assert alert_dialog.open is False
    # The snackbar was appended.
    assert len(page._dialogs.controls) == 2
    snackbar = page._dialogs.controls[1]
    assert snackbar.open is True

    # Dismiss patches the alert directly with open=False.
    assert session.patch_calls == [(alert_dialog, {})]
    # Show schedules the `_dialogs` list for update so the new snackbar
    # entry is flushed to Flutter.
    assert session.scheduled_updates == [page._dialogs]


def test_use_dialog_reopen_while_dismissing_appends_fresh_dialog():
    """Regression: if a new dialog is passed *while the previous one is
    still dismissing* (client hasn't finished the pop animation so the old
    dialog is still in `_dialogs.controls` with `open=False`), the hook
    must append the new dialog as a fresh entry instead of reusing the
    old one's `_i`.  Otherwise Flutter's AlertDialogControl — still
    holding `_open=True` from the dismissing one — sees
    `open == True == lastOpen` and never re-runs `showDialog`, so the new
    dialog is stuck off-screen until Flutter garbage-collects the old
    route (or never).
    """
    page, _ = create_page()
    first = True

    def body():
        ft.use_dialog(
            ft.AlertDialog(
                title=ft.Text("first" if first else "second"),
            )
        )

    component = Component(fn=body, args=(), kwargs={})

    # Initial render — dialog #1 is open.
    render_component(component, page)
    first_dialog = page._dialogs.controls[0]
    assert first_dialog.open is True

    # Simulate the server-side dismiss path used by this hook: flip the
    # open flag but leave the dialog in `_dialogs.controls` (Flutter's
    # dismiss animation owns the removal).
    first_dialog.open = False

    # User opens a new dialog while #1 is still dismissing.
    first = False
    render_component(component, page)

    # Both dialogs coexist — dismissing + freshly showing — so they must
    # have distinct `_i` values and the new one must be live and open.
    assert first_dialog in page._dialogs.controls
    assert first_dialog.open is False
    assert len(page._dialogs.controls) == 2
    second_dialog = page._dialogs.controls[1]
    assert second_dialog is not first_dialog
    assert second_dialog._i != first_dialog._i
    assert second_dialog.open is True


def test_use_dialog_sibling_rerender_emits_frozen_diff():
    """Regression: when a component re-renders with a fresh dialog instance
    that has the same content, the hook must emit a *frozen* diff against
    the previous dialog. The frozen path migrates `_i` from the previous
    instance onto the new one (via `_migrate_state`), so Flutter sees the
    same Control on both sides — preserving the dialog route, TextField
    cursor, animation state, etc.
    """
    page, session = create_page()

    def body():
        ft.use_dialog(ft.AlertDialog(title=ft.Text("Hello")))

    component = Component(fn=body, args=(), kwargs={})
    render_component(component, page)

    first_dialog = page._dialogs.controls[0]
    session.patch_calls.clear()
    session.scheduled_updates.clear()

    # Sibling re-render: same component body, fresh dialog instance.
    render_component(component, page)

    # Overlay list still has exactly one dialog at the same index.
    assert len(page._dialogs.controls) == 1
    # Exactly one frozen diff call — against the previous dialog — so
    # `_migrate_state` takes the `_i` off `first_dialog` onto the new
    # instance. No separate `schedule_update` (the frozen patch is the
    # only message).
    assert len(session.patch_calls) == 1
    patched, kwargs = session.patch_calls[0]
    assert patched is page._dialogs.controls[0]
    assert kwargs.get("prev_control") is first_dialog
    assert kwargs.get("frozen") is True
    assert session.scheduled_updates == []


def test_use_dialog_open_rerender_updates_live_dialog_content():
    """Regression: re-rendering with updated props/closures while the
    dialog is open must propagate to the mounted overlay entry so the
    live dialog sees the latest `disabled`, `on_click` closure, etc.

    The frozen diff both emits the field deltas (Dart side) and updates
    the Python list entry to point at the fresh dialog (whose `_i` has
    been migrated from the previous instance), so subsequent event
    dispatch reaches the live closures.
    """
    page, _session = create_page()
    comment = ""
    submitted: list[str] = []

    def body():
        ft.use_dialog(
            ft.AlertDialog(
                title=ft.Text("Compose"),
                actions=[
                    ft.TextButton(
                        "Save",
                        disabled=not comment.strip(),
                        on_click=lambda: submitted.append(comment),
                    )
                ],
            )
        )

    component = Component(fn=body, args=(), kwargs={})

    render_component(component, page)

    first_dialog = page._dialogs.controls[0]
    assert first_dialog.actions[0].disabled is True

    comment = "Ship it"
    render_component(component, page)

    # Overlay still has exactly one dialog. The entry now points at the
    # fresh instance whose closures reflect the latest render.
    assert len(page._dialogs.controls) == 1
    mounted = page._dialogs.controls[0]
    assert mounted.actions[0].disabled is False
    mounted.actions[0].on_click()
    assert submitted == ["Ship it"]


def test_use_dialog_rerender_preserves_dialogs_prev_lists_snapshot():
    """Regression: after a frozen-patch re-render swaps the dialog instance
    in `_dialogs.controls[idx]`, `_dialogs.__prev_lists['controls']` must
    keep pointing at the live list contents — not at the now-discarded
    previous Python object.

    If it falls out of sync, a later `_dialogs.update()` triggered by an
    unrelated caller (e.g. `page.show_dialog(SnackBar)` from a toast)
    diffs the fresh list against the stale snapshot, sees different
    `id()` for the same logical dialog, and emits a full REPLACE. On
    Dart that creates a new Control with `_open` unset, the next build
    re-enters the show branch and pushes a second DialogRoute on top of
    the existing one, and subsequent `open=False` patches only close
    the first — leaving the dialog stuck open with a double-dim barrier.
    """
    page, _ = create_page()

    counter = 0

    def body():
        ft.use_dialog(ft.AlertDialog(title=ft.Text(f"dialog #{counter}")))

    component = Component(fn=body, args=(), kwargs={})

    render_component(component, page)
    mounted = page._dialogs.controls[0]

    # Simulate the MsgPack encoder having serialized `_dialogs` once, which
    # is what populates `__prev_lists` on the real protocol path. Without
    # that, the scenario the regression covers can't arise.
    object.__setattr__(
        page._dialogs, "__prev_lists", {"controls": page._dialogs.controls[:]}
    )

    # Frozen-patch re-render → the hook swaps in a fresh AlertDialog.
    counter += 1
    render_component(component, page)

    swapped = page._dialogs.controls[0]
    assert swapped is not mounted  # instance was replaced

    prev_snapshot = getattr(page._dialogs, "__prev_lists")["controls"]
    # The snapshot must track the live list. If it still holds the old
    # Python object, a later `_dialogs.update()` will diff incorrectly.
    assert prev_snapshot[0] is swapped


@pytest.mark.asyncio
async def test_use_dialog_dispatch_event_survives_reopen_after_sibling_rerender():
    @ft.observable
    @dataclass
    class DialogState:
        toast: str | None = None
        create_count: int = 0

    state = DialogState()
    state_context = ft.create_context(state)

    @ft.component
    def SnackbarHost():
        s = ft.use_context(state_context)
        ft.use_dialog(
            ft.SnackBar(
                content=ft.Text(s.toast),
                on_dismiss=lambda e: setattr(s, "toast", None),
            )
            if s.toast
            else None
        )
        return ft.Container(width=0, height=0)

    @ft.component
    def VersionsHost():
        s = ft.use_context(state_context)
        create_open, set_create_open = ft.use_state(False)
        comment, set_comment = ft.use_state("")

        async def create():
            if not comment.strip():
                return
            s.create_count += 1
            s.toast = f"Created {s.create_count}"
            set_comment("")
            set_create_open(False)

        ft.use_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Create version"),
                actions=[
                    ft.Button(
                        "Cancel",
                        on_click=lambda: set_create_open(False),
                    ),
                    ft.FilledButton(
                        "Create",
                        on_click=lambda: asyncio.create_task(create()),
                    ),
                ],
                on_dismiss=lambda: set_create_open(False),
            )
            if create_open
            else None
        )

        return ft.Column(
            controls=[
                ft.FilledButton(
                    "Create version",
                    on_click=lambda: (set_comment("v"), set_create_open(True)),
                )
            ]
        )

    @ft.component
    def App():
        return state_context(state, lambda: [VersionsHost(), SnackbarHost()])

    conn = _RecordingConnection()
    conn.pubsubhub = PubSubHub()
    session = Session(conn)
    token = _context_page.set(session.page)

    try:
        session.page.render(App)
        session.get_page_patch()
        await flush_async()

        outer = find_filled_button(session, "Create version")
        await session.dispatch_event(outer._i, "click", None)
        await flush_async()
        assert crash_messages(conn) == []

        inner = session.page._dialogs.controls[-1].actions[1]
        await inner._trigger_event("click", None)
        await flush_async()
        assert crash_messages(conn) == []
        assert state.create_count == 1

        outer = find_filled_button(session, "Create version")
        await session.dispatch_event(outer._i, "click", None)
        await flush_async()
        assert crash_messages(conn) == []

        inner = session.page._dialogs.controls[-1].actions[1]
        await inner._trigger_event("click", None)
        await flush_async()
        assert crash_messages(conn) == []
        assert state.create_count == 2
    finally:
        session.close()
        await flush_async()
        _context_page.reset(token)


@pytest.mark.asyncio
async def test_dispatch_event_recovers_live_control_when_index_stale():
    clicks: list[str] = []

    conn = _RecordingConnection()
    conn.pubsubhub = PubSubHub()
    session = Session(conn)

    live_button = ft.FilledButton(
        "Create version", on_click=lambda e: clicks.append("live")
    )
    stale_button = ft.FilledButton(
        "Create version", on_click=lambda e: clicks.append("stale")
    )
    object.__setattr__(live_button, "_i", stale_button._i)
    session.page.controls = [ft.Column(controls=[live_button])]

    token = _context_page.set(session.page)
    try:
        session.get_page_patch()
        session.index[live_button._i] = stale_button

        await session.dispatch_event(live_button._i, "click", None)
        await flush_async()

        assert clicks == ["live"]
        assert crash_messages(conn) == []
        assert session.index[live_button._i] is live_button
    finally:
        session.close()
        await flush_async()
        _context_page.reset(token)


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
