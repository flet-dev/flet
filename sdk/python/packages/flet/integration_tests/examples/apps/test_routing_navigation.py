import pytest

import flet.testing as ftt
from examples.apps.routing_navigation import (
    home_store,
    initial_route,
    pop_view_confirm,
    route_change_event,
)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": initial_route.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_initial_route(flet_app_function: ftt.FletTestApp):
    text = await flet_app_function.tester.find_by_text("Initial route: /")
    assert text.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": route_change_event.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_route_change_event(flet_app_function: ftt.FletTestApp):
    text = await flet_app_function.tester.find_by_text("Initial route: /")
    assert text.count == 1
    await flet_app_function.page.push_route("/new-route")
    await flet_app_function.tester.pump_and_settle()
    new_text = await flet_app_function.tester.find_by_text("New route: /new-route")
    assert new_text.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": home_store.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_home_store(flet_app_function: ftt.FletTestApp):
    # Verify initial view
    button = await flet_app_function.tester.find_by_text_containing("Visit Store")
    assert button.count == 1
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()

    # Verify store view
    store_button = await flet_app_function.tester.find_by_text_containing("Go Home")
    assert store_button.count == 1
    await flet_app_function.tester.tap(store_button)
    await flet_app_function.tester.pump_and_settle()

    # Verify back to initial view
    button = await flet_app_function.tester.find_by_text_containing("Visit Store")
    assert button.count == 1

    # Go to store again with push_route
    await flet_app_function.page.push_route("/store")
    await flet_app_function.tester.pump_and_settle()
    store_button = await flet_app_function.tester.find_by_text_containing("Go Home")
    assert store_button.count == 1

    # Go home again with push_route
    await flet_app_function.page.push_route("/")
    await flet_app_function.tester.pump_and_settle()
    button = await flet_app_function.tester.find_by_text_containing("Visit Store")
    assert button.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": pop_view_confirm.main}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_pop_view_confirm(flet_app_function: ftt.FletTestApp):
    # Verify initial view
    button = await flet_app_function.tester.find_by_text_containing("Go to store")
    assert button.count == 1
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()

    # Verify permission view
    permission_view_text = await flet_app_function.tester.find_by_text("/store View")
    assert permission_view_text.count == 1

    # Click Back button
    back_button = await flet_app_function.tester.find_by_tooltip("Back")
    assert back_button.count == 1
    await flet_app_function.tester.tap(back_button)
    await flet_app_function.tester.pump_and_settle()

    # Verify that confirmation dialog is shown
    dlg_text = await flet_app_function.tester.find_by_text("Please confirm")
    assert dlg_text.count == 1

    # Click No button
    no_button = await flet_app_function.tester.find_by_text("No")
    assert no_button.count == 1
    await flet_app_function.tester.tap(no_button)
    await flet_app_function.tester.pump_and_settle()

    # Verify still in permission view
    permission_view_text = await flet_app_function.tester.find_by_text("/store View")
    assert permission_view_text.count == 1

    # Click Back button again
    back_button = await flet_app_function.tester.find_by_tooltip("Back")
    assert back_button.count == 1
    await flet_app_function.tester.tap(back_button)
    await flet_app_function.tester.pump_and_settle()

    # Verify that confirmation dialog is shown again
    dlg_text = await flet_app_function.tester.find_by_text("Please confirm")
    assert dlg_text.count == 1

    # Click Yes button
    yes_button = await flet_app_function.tester.find_by_text("Yes")
    assert yes_button.count == 1
    await flet_app_function.tester.tap(yes_button)
    await flet_app_function.tester.pump_and_settle()

    # Verify back to initial view
    button = await flet_app_function.tester.find_by_text_containing("Go to store")
    assert button.count == 1
