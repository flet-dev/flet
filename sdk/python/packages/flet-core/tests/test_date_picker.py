import datetime

import flet_core as ft
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.DatePicker()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["date_picker"],
            attrs={'state': 'initState'},
            commands=[],
        )
    ], "Test failed"


# pick_date
def test_pick_date():
    r = ft.DatePicker()
    assert r._get_attr("state") == "initState"
    r.update = lambda *_: None  # monkeypatch
    r.pick_date()
    r.state = "pickDate"
    assert r._get_attr("state") == "pickDate"


# value
def test_value():
    some_date = datetime.datetime.now()
    r = ft.DatePicker()
    assert r.value is None
    assert r._get_attr("value") is None

    r = ft.DatePicker(value=some_date)
    r.value = some_date
    assert r._get_attr("value") == some_date.isoformat()


# first_date
def test_first_date():
    some_date = datetime.datetime.now()
    r = ft.DatePicker()
    assert r.first_date is None
    assert r._get_attr("firstDate") is None

    r = ft.DatePicker(first_date=some_date)
    r.first_date = some_date
    assert r._get_attr("firstDate") == some_date.isoformat()


# last_date
def test_last_date():
    some_date = datetime.datetime.now()
    r = ft.DatePicker()
    assert r.last_date is None
    assert r._get_attr("lastDate") is None

    r = ft.DatePicker(last_date=some_date)
    r.last_date = some_date
    assert r._get_attr("lastDate") == some_date.isoformat()


# locale
def test_locale():
    r = ft.DatePicker()
    assert r.locale is None
    assert r._get_attr("locale") is None

    r = ft.DatePicker(locale="be")
    assert r._get_attr("locale") == "be"


# help_text
def test_help_text():
    r = ft.DatePicker()
    assert r.help_text is None
    assert r._get_attr("helpText") is None

    r = ft.DatePicker(help_text="ala ma kota")
    assert r._get_attr("helpText") == "ala ma kota"


# cancel_text
def test_cancel_text():
    r = ft.DatePicker()
    assert r.cancel_text is None
    assert r._get_attr("cancelText") is None

    r = ft.DatePicker(cancel_text="ala ma kota")
    assert r._get_attr("cancelText") == "ala ma kota"


# confirm_text
def test_confirm_text():
    r = ft.DatePicker()
    assert r.confirm_text is None
    assert r._get_attr("confirmText") is None

    r = ft.DatePicker(confirm_text="ala ma kota")
    assert r._get_attr("confirmText") == "ala ma kota"


# keyboard_type
def test_keyboard_type_enum():
    r = ft.DatePicker()
    assert r.keyboard_type is None
    assert r._get_attr("keyboardType") is None

    r = ft.DatePicker(keyboard_type=ft.KeyboardType.NONE)
    assert isinstance(r.keyboard_type, ft.KeyboardType)
    assert r.keyboard_type == ft.KeyboardType.NONE
    assert r._get_attr("keyboardType") == "none"

    r = ft.TextField(keyboard_type="phone")
    assert isinstance(r.keyboard_type, str)
    assert r._get_attr("keyboardType") == "phone"


# date_picker_mode
def test_date_picker_mode_enum():
    r = ft.DatePicker()
    assert r.date_picker_mode is None
    assert r._get_attr("datePickerMode") is None

    r = ft.DatePicker(date_picker_mode=ft.DatePickerMode.YEAR)
    assert isinstance(r.date_picker_mode, ft.DatePickerMode)
    assert r.date_picker_mode == ft.DatePickerMode.YEAR
    assert r._get_attr("datePickerMode") == "year"


# date_picker_entry_mode
def test_date_picker_entry_mode_enum():
    r = ft.DatePicker()
    assert r.date_picker_entry_mode is None
    assert r._get_attr("datePickerEntryMode") is None

    r = ft.DatePicker(date_picker_entry_mode=ft.DatePickerEntryMode.CALENDAR)
    assert isinstance(r.date_picker_entry_mode, ft.DatePickerEntryMode)
    assert r.date_picker_entry_mode == ft.DatePickerEntryMode.CALENDAR
    assert r._get_attr("datePickerEntryMode") == "calendar"
