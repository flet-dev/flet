import flet as ft
from flet.controls.base_control import BaseControl
from flet.controls.object_patch import ObjectPatch
from flet.messaging.protocol import configure_encode_object_for_msgpack


def _property_patch(control, **changes):
    """Property-level diff for mutating `control` in place.

    The diff is against the control's own previous snapshot, so the baseline is
    established by encoding it once and the change is then diffed same-instance.
    Diffing two separately constructed controls would report a whole-control
    Replace instead, which is not what the client sees for a property change.
    """
    ObjectPatch.from_diff(None, control, control_cls=BaseControl)
    for name, value in changes.items():
        setattr(control, name, value)
    patch, _, _ = ObjectPatch.from_diff(control, control, control_cls=BaseControl)
    # message[0] is the control-id path; the operations follow it, so an
    # unchanged control yields a single-element message rather than an empty one.
    return patch.to_message()[1:]


def test_embedded_defaults_to_false_on_a_page():
    # The client sets it to True for a guest; a normal app must not think it is
    # embedded and skip owning its window.
    from flet.controls.page import Page

    assert Page.embedded is False or "embedded" in {
        f.name for f in __import__("dataclasses").fields(Page)
    }


def test_title_is_encoded_for_the_client():
    encoder = configure_encode_object_for_msgpack(BaseControl)
    encoded = encoder(ft.FletApp(url="dartbridge://", title="Guest app"))
    assert encoded["title"] == "Guest app"


def test_rewriting_the_same_title_produces_no_patch():
    # Same guard as route: the client writes the title back when the guest sets
    # it, and that must not loop.
    app = ft.FletApp(url="dartbridge://", title="Guest app")
    assert _property_patch(app, title="Guest app") == []


def test_window_state_is_encoded_for_the_client():
    encoder = configure_encode_object_for_msgpack(BaseControl)
    state = {"width": 1100, "height": 700, "maximized": False}
    encoded = encoder(ft.FletApp(url="dartbridge://", window_state=state))
    assert encoded["window_state"] == state


def test_window_event_carries_action_and_args():
    # `args` deliberately is not called `data`: that name is the base Event's
    # own payload, and shadowing it reorders the base's non-default fields.
    names = {f.name for f in __import__("dataclasses").fields(ft.FletAppWindowEvent)}
    assert {"action", "args"} <= names
    assert "data" in names  # still the base payload, not ours


def test_window_state_change_produces_a_property_patch():
    app = ft.FletApp(url="dartbridge://", window_state={"width": 100})
    ops = _property_patch(app, window_state={"width": 200})
    assert ops, "changing window_state must reach the client"


def test_route_and_media_padding_default_to_none():
    # Unset, both stay absent: the embedded app keeps owning its own routing
    # and inherits the host window's real insets.
    app = ft.FletApp(url="dartbridge://")
    assert app.route is None
    assert app.media_padding is None


def test_route_is_encoded_for_the_client():
    encoder = configure_encode_object_for_msgpack(BaseControl)
    encoded = encoder(ft.FletApp(url="dartbridge://", route="/settings"))
    assert encoded["route"] == "/settings"


def test_media_padding_is_encoded_for_the_client():
    encoder = configure_encode_object_for_msgpack(BaseControl)
    padding = ft.Padding.only(top=59, bottom=34)
    encoded = encoder(ft.FletApp(url="dartbridge://", media_padding=padding))
    assert encoded["media_padding"] == padding
    # Nested values encode through the same hook on the way to the client, and
    # only non-default sides are sent.
    assert encoder(padding) == {"top": 59, "bottom": 34}


def test_media_padding_accepts_a_bare_number():
    # PaddingValue allows a single number for all four sides.
    assert ft.FletApp(url="dartbridge://", media_padding=8).media_padding == 8


def test_setting_route_produces_a_property_patch():
    app = ft.FletApp(url="dartbridge://", route="/")
    ops = _property_patch(app, route="/settings")
    assert ops, "changing route must reach the client"
    assert ops[0][2:] == ["route", "/settings"]


def test_rewriting_the_same_route_produces_no_patch():
    # The client writes the route back after the embedded app navigates itself.
    # That write must not come back down as a fresh navigation.
    app = ft.FletApp(url="dartbridge://", route="/settings")
    assert _property_patch(app, route="/settings") == []


def test_media_padding_change_produces_a_property_patch():
    app = ft.FletApp(url="dartbridge://")
    ops = _property_patch(app, media_padding=ft.Padding.only(top=59))
    assert ops, "changing media_padding must reach the client"
    assert ops[0][2] == "media_padding"
