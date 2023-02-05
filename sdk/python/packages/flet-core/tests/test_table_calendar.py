import datetime

import flet_core as ft
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.TableCalendar()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["tablecalendar"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


# first_date
def test_first_day():
    some_date = datetime.datetime.now()
    r = ft.TableCalendar()
    assert r.first_day is None
    assert r._get_attr("firstDay") is None

    r = ft.TableCalendar(first_day=some_date)
    r.first_day = some_date
    assert r._get_attr("firstDay") == some_date.isoformat()


# last_date
def test_last_day():
    some_date = datetime.datetime.now()
    r = ft.TableCalendar()
    assert r.last_day is None
    assert r._get_attr("lastDay") is None

    r = ft.TableCalendar(last_day=some_date)
    r.last_date = some_date
    assert r._get_attr("lastDay") == some_date.isoformat()


# locale
def test_locale():
    r = ft.TableCalendar()
    assert r.locale is None
    assert r._get_attr("locale") is None

    r = ft.DatePicker(locale="be")
    assert r._get_attr("locale") == "be"
