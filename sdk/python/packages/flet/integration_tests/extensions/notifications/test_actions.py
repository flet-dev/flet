"""Tests for notification actions and shared helpers."""

import pytest

from flet_notifications import NotificationAction, NotificationActionInput
from flet_notifications.base import NotificationError, check_result, to_bool


def test_action_defaults():
    action = NotificationAction(id="open", title="Open")
    assert action.destructive is False
    assert action.foreground is True
    assert action.cancel_notification is True
    assert action.input is None


def test_action_to_dict():
    action = NotificationAction(
        id="delete",
        title="Delete",
        destructive=True,
        foreground=False,
        cancel_notification=False,
    )
    assert action.to_dict() == {
        "id": "delete",
        "title": "Delete",
        "destructive": True,
        "foreground": False,
        "cancel_notification": False,
        "input": None,
    }


def test_action_with_input_to_dict():
    action = NotificationAction(
        id="reply",
        title="Reply",
        input=NotificationActionInput(
            label="Type here",
            choices=["Yes", "No"],
            allow_free_form_input=True,
            allowed_mime_types=["image/png"],
        ),
    )
    d = action.to_dict()
    assert d["input"] == {
        "label": "Type here",
        "choices": ["Yes", "No"],
        "allow_free_form_input": True,
        "allowed_mime_types": ["image/png"],
    }


def test_input_defaults():
    inp = NotificationActionInput()
    d = inp.to_dict()
    assert d == {
        "label": "",
        "choices": [],
        "allow_free_form_input": True,
        "allowed_mime_types": [],
    }


def test_check_result_ok():
    check_result("ok")  # must not raise
    check_result("true")
    check_result(None)


def test_check_result_error():
    with pytest.raises(NotificationError) as exc:
        check_result("error:cancel_failed:no such id")
    assert exc.value.code == "cancel_failed"
    assert exc.value.message == "no such id"


def test_check_result_error_without_message():
    with pytest.raises(NotificationError) as exc:
        check_result("error:init_failed")
    assert exc.value.code == "init_failed"
    assert exc.value.message == ""


def test_to_bool_variants():
    assert to_bool("true") is True
    assert to_bool("false") is False
    assert to_bool(True) is True
    assert to_bool(False) is False


def test_notification_error_repr():
    err = NotificationError("show_failed", "boom")
    assert "show_failed" in repr(err)
    assert "boom" in repr(err)
