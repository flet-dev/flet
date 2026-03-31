import inspect
from unittest.mock import AsyncMock, patch

import pytest

import flet as ft
from flet.controls.control_event import get_event_field_type
from flet.controls.page import Page, ViewsPopUntilEvent
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


def _make_page() -> Page:
    conn = Connection()
    conn.pubsubhub = PubSubHub()
    return Page(sess=Session(conn))


def test_views_pop_until_event_creation():
    page = _make_page()
    evt = ViewsPopUntilEvent(
        name="views_pop_until",
        control=page,
        route="/",
        result="test_result",
    )
    assert evt.route == "/"
    assert evt.result == "test_result"
    assert evt.view is None
    assert evt.name == "views_pop_until"


def test_views_pop_until_event_default_result():
    page = _make_page()
    evt = ViewsPopUntilEvent(
        name="views_pop_until",
        control=page,
        route="/home",
    )
    assert evt.result is None


def test_get_event_field_type_on_views_pop_until():
    page = _make_page()
    event_type = get_event_field_type(page, "on_views_pop_until")
    assert event_type == ViewsPopUntilEvent


def test_views_pop_until_event_importable_from_flet():
    assert hasattr(ft, "ViewsPopUntilEvent")
    assert ft.ViewsPopUntilEvent is ViewsPopUntilEvent


def test_page_has_on_views_pop_until_attribute():
    page = _make_page()
    assert hasattr(page, "on_views_pop_until")
    assert page.on_views_pop_until is None


def test_page_has_pop_views_until_method():
    page = _make_page()
    assert hasattr(page, "pop_views_until")
    assert inspect.iscoroutinefunction(page.pop_views_until)


@pytest.mark.asyncio
async def test_pop_views_until_raises_on_missing_route():
    page = _make_page()
    page.views = [ft.View(route="/")]

    with pytest.raises(ValueError, match="No view found with route '/nonexistent'"):
        await page.pop_views_until("/nonexistent")


@pytest.mark.asyncio
async def test_pop_views_until_removes_views_above_target():
    page = _make_page()
    page.views = [
        ft.View(route="/"),
        ft.View(route="/step1"),
        ft.View(route="/step2"),
        ft.View(route="/step3"),
    ]

    with (
        patch.object(page, "_invoke_method", new_callable=AsyncMock),
        patch.object(page, "update"),
    ):
        await page.pop_views_until("/", result="done")

    assert len(page.views) == 1
    assert page.views[0].route == "/"


@pytest.mark.asyncio
async def test_pop_views_until_removes_to_middle_view():
    page = _make_page()
    page.views = [
        ft.View(route="/"),
        ft.View(route="/step1"),
        ft.View(route="/step2"),
    ]

    with (
        patch.object(page, "_invoke_method", new_callable=AsyncMock),
        patch.object(page, "update"),
    ):
        await page.pop_views_until("/step1", result="partial")

    assert len(page.views) == 2
    assert page.views[0].route == "/"
    assert page.views[1].route == "/step1"


@pytest.mark.asyncio
async def test_pop_views_until_no_op_when_target_is_top():
    page = _make_page()
    page.views = [
        ft.View(route="/"),
        ft.View(route="/current"),
    ]

    with (
        patch.object(page, "_invoke_method", new_callable=AsyncMock),
        patch.object(page, "update"),
    ):
        await page.pop_views_until("/current", result="same")

    assert len(page.views) == 2
    assert page.views[-1].route == "/current"


@pytest.mark.asyncio
async def test_pop_views_until_fires_only_views_pop_until():
    page = _make_page()
    page.views = [
        ft.View(route="/"),
        ft.View(route="/step1"),
        ft.View(route="/step2"),
    ]

    page.on_views_pop_until = lambda e: None

    with (
        patch.object(page, "_invoke_method", new_callable=AsyncMock),
        patch.object(page, "update"),
        patch.object(page, "_trigger_event", new_callable=AsyncMock) as mock_trigger,
    ):
        await page.pop_views_until("/", result="finished")

    trigger_calls = [call.args[0] for call in mock_trigger.call_args_list]
    # on_view_pop should NOT be fired — pop_views_until handles removal
    assert "view_pop" not in trigger_calls
    # on_views_pop_until SHOULD be fired for the destination view
    assert "views_pop_until" in trigger_calls


@pytest.mark.asyncio
async def test_pop_views_until_no_event_when_no_handler():
    page = _make_page()
    page.views = [
        ft.View(route="/"),
        ft.View(route="/step1"),
    ]

    # No on_views_pop_until handler set
    with (
        patch.object(page, "_invoke_method", new_callable=AsyncMock),
        patch.object(page, "update"),
        patch.object(page, "_trigger_event", new_callable=AsyncMock) as mock_trigger,
    ):
        await page.pop_views_until("/", result="done")

    assert mock_trigger.call_count == 0
