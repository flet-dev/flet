import pytest

import flet as ft
import flet.testing as ftt
from examples.apps.routing_navigation.drawer_navigation import main as drawer_navigation
from examples.apps.routing_navigation.home_store import main as home_store
from examples.apps.routing_navigation.initial_route import main as initial_route
from examples.apps.routing_navigation.pop_view_confirm import main as pop_view_confirm
from examples.apps.routing_navigation.pop_views_until import main as pop_views_until
from examples.apps.routing_navigation.route_change_event import (
    main as route_change_event,
)


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": initial_route}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_initial_route(flet_app_function: ftt.FletTestApp):
    text = await flet_app_function.tester.find_by_text("Initial route: /")
    assert text.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": route_change_event}],
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
    [{"flet_app_main": home_store}],
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
    [{"flet_app_main": pop_view_confirm}],
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


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": drawer_navigation}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_drawer_navigation(flet_app_function: ftt.FletTestApp):
    # Verify initial view
    hamburger_button = await flet_app_function.tester.find_by_icon(ft.Icons.MENU)
    assert hamburger_button.count == 1
    await flet_app_function.tester.tap(hamburger_button)
    await flet_app_function.tester.pump_and_settle()

    # Select Store from drawer
    store_item = await flet_app_function.tester.find_by_icon(ft.Icons.STORE_OUTLINED)
    assert store_item.count == 1
    await flet_app_function.tester.tap(store_item)
    await flet_app_function.tester.pump_and_settle()

    # Verify store view
    store_text = await flet_app_function.tester.find_by_text("Welcome to Store Page")
    assert store_text.count == 1

    # Open drawer again
    hamburger_button = await flet_app_function.tester.find_by_icon(ft.Icons.MENU)
    assert hamburger_button.count == 1
    await flet_app_function.tester.tap(hamburger_button)
    await flet_app_function.tester.pump_and_settle()

    # Select About from drawer
    about_item = await flet_app_function.tester.find_by_icon(ft.Icons.PHONE_OUTLINED)
    assert about_item.count == 1
    await flet_app_function.tester.tap(about_item)
    await flet_app_function.tester.pump_and_settle()

    # Verify about view
    about_text = await flet_app_function.tester.find_by_text("Welcome to About Page")
    assert about_text.count == 1

    # Open drawer again
    hamburger_button = await flet_app_function.tester.find_by_icon(ft.Icons.MENU)
    assert hamburger_button.count == 1
    await flet_app_function.tester.tap(hamburger_button)
    await flet_app_function.tester.pump_and_settle()

    # Select Home from drawer
    home_item = await flet_app_function.tester.find_by_icon(ft.Icons.HOME_OUTLINED)
    assert home_item.count == 1
    await flet_app_function.tester.tap(home_item)
    await flet_app_function.tester.pump_and_settle()

    # Verify home view
    home_text = await flet_app_function.tester.find_by_text("Welcome to Home Page")
    assert home_text.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": pop_views_until}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_pop_views_until(flet_app_function: ftt.FletTestApp):
    # Verify initial view
    button = await flet_app_function.tester.find_by_text_containing("Start flow")
    assert button.count == 1
    result_text = await flet_app_function.tester.find_by_text("No result yet")
    assert result_text.count == 1

    # Navigate to Step 1
    await flet_app_function.tester.tap(button)
    await flet_app_function.tester.pump_and_settle()
    step1_text = await flet_app_function.tester.find_by_text("Step 1 of the flow")
    assert step1_text.count == 1

    # Navigate to Step 2
    step2_button = await flet_app_function.tester.find_by_text_containing(
        "Go to Step 2"
    )
    assert step2_button.count == 1
    await flet_app_function.tester.tap(step2_button)
    await flet_app_function.tester.pump_and_settle()
    step2_text = await flet_app_function.tester.find_by_text("Step 2 of the flow")
    assert step2_text.count == 1

    # Navigate to Step 3
    step3_button = await flet_app_function.tester.find_by_text_containing(
        "Go to Step 3"
    )
    assert step3_button.count == 1
    await flet_app_function.tester.tap(step3_button)
    await flet_app_function.tester.pump_and_settle()
    final_text = await flet_app_function.tester.find_by_text("Flow complete!")
    assert final_text.count == 1

    # Click "Finish and go Home" — triggers pop_views_until
    finish_button = await flet_app_function.tester.find_by_text_containing(
        "Finish and go Home"
    )
    assert finish_button.count == 1
    await flet_app_function.tester.tap(finish_button)
    await flet_app_function.tester.pump_and_settle()

    # Verify back at Home with result
    result_text = await flet_app_function.tester.find_by_text("Result: Flow completed!")
    assert result_text.count == 1

    # Verify we can start the flow again
    button = await flet_app_function.tester.find_by_text_containing("Start flow")
    assert button.count == 1
