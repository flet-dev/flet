import pytest

import flet as ft
import flet.testing as ftt
from examples.apps.router.active_links import main as active_links
from examples.apps.router.app_drawer import main as app_drawer
from examples.apps.router.auth_dialog import main as auth_dialog
from examples.apps.router.auth_page import main as auth_page
from examples.apps.router.basic import main as basic
from examples.apps.router.dynamic_segments import main as dynamic_segments
from examples.apps.router.featured import main as featured
from examples.apps.router.featured_views import main as featured_views
from examples.apps.router.index_routes import main as index_routes
from examples.apps.router.layout_outlet import main as layout_outlet
from examples.apps.router.loaders import main as loaders
from examples.apps.router.nested_outlet_views import main as nested_outlet_views
from examples.apps.router.nested_routes import main as nested_routes
from examples.apps.router.prefix_routes import main as prefix_routes
from examples.apps.router.runtime_routes import main as runtime_routes
from examples.apps.router.splats import main as splats

# Helpers to run Router examples. Examples don't define a `main(page)` function —
# they use `page.render(App)` or `page.render_views(App)` inline in a lambda.
# The test fixture expects a callable taking a page, so we wrap the `App`
# component in a small main function here.


def _make_render_main(app_component):
    def main(page: ft.Page):
        page.render(app_component)

    return main


def _make_render_views_main(app_component):
    def main(page: ft.Page):
        page.render_views(app_component)

    return main


# ---------------------------------------------------------------------------
# Simple examples — flat routing, outlets, index/prefix/dynamic/splat patterns
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(basic.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_basic(flet_app_function: ftt.FletTestApp):
    home = await flet_app_function.tester.find_by_text("Home page")
    assert home.count == 1

    about_btn = await flet_app_function.tester.find_by_text("About")
    assert about_btn.count == 1
    await flet_app_function.tester.tap(about_btn)
    await flet_app_function.tester.pump_and_settle()

    about = await flet_app_function.tester.find_by_text("About page")
    assert about.count == 1

    home_btn = await flet_app_function.tester.find_by_text("Home")
    assert home_btn.count == 1
    await flet_app_function.tester.tap(home_btn)
    await flet_app_function.tester.pump_and_settle()

    home = await flet_app_function.tester.find_by_text("Home page")
    assert home.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(active_links.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_active_links(flet_app_function: ftt.FletTestApp):
    home = await flet_app_function.tester.find_by_text("Home page")
    assert home.count == 1

    products_link = await flet_app_function.tester.find_by_text("Products")
    assert products_link.count == 1
    await flet_app_function.tester.tap(products_link)
    await flet_app_function.tester.pump_and_settle()

    products = await flet_app_function.tester.find_by_text("Products page")
    assert products.count == 1

    settings_link = await flet_app_function.tester.find_by_text("Settings")
    assert settings_link.count == 1
    await flet_app_function.tester.tap(settings_link)
    await flet_app_function.tester.pump_and_settle()

    settings = await flet_app_function.tester.find_by_text("Settings page")
    assert settings.count == 1

    await flet_app_function.page.push_route("/")
    await flet_app_function.tester.pump_and_settle()
    home = await flet_app_function.tester.find_by_text("Home page")
    assert home.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(index_routes.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_index_routes(flet_app_function: ftt.FletTestApp):
    dashboard = await flet_app_function.tester.find_by_text(
        "Dashboard (index route for /)"
    )
    assert dashboard.count == 1

    settings_btn = await flet_app_function.tester.find_by_text("Settings")
    assert settings_btn.count == 1
    await flet_app_function.tester.tap(settings_btn)
    await flet_app_function.tester.pump_and_settle()

    settings_home = await flet_app_function.tester.find_by_text(
        "Settings Home (index route for /settings)"
    )
    assert settings_home.count == 1

    profile_btn = await flet_app_function.tester.find_by_text("Profile")
    assert profile_btn.count == 1
    await flet_app_function.tester.tap(profile_btn)
    await flet_app_function.tester.pump_and_settle()

    profile = await flet_app_function.tester.find_by_text("Profile Settings")
    assert profile.count == 1

    security_btn = await flet_app_function.tester.find_by_text("Security")
    assert security_btn.count == 1
    await flet_app_function.tester.tap(security_btn)
    await flet_app_function.tester.pump_and_settle()

    security = await flet_app_function.tester.find_by_text("Security Settings")
    assert security.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(layout_outlet.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_layout_outlet(flet_app_function: ftt.FletTestApp):
    # AppBar is shared across all routes — verify it's there on initial render.
    appbar_title = await flet_app_function.tester.find_by_text("My App")
    assert appbar_title.count == 1

    home = await flet_app_function.tester.find_by_text("Welcome home!")
    assert home.count == 1

    about_btn = await flet_app_function.tester.find_by_text("About")
    assert about_btn.count == 1
    await flet_app_function.tester.tap(about_btn)
    await flet_app_function.tester.pump_and_settle()

    about = await flet_app_function.tester.find_by_text("About us")
    assert about.count == 1
    # AppBar still present after navigation
    appbar_title = await flet_app_function.tester.find_by_text("My App")
    assert appbar_title.count == 1

    contact_btn = await flet_app_function.tester.find_by_text("Contact")
    assert contact_btn.count == 1
    await flet_app_function.tester.tap(contact_btn)
    await flet_app_function.tester.pump_and_settle()

    contact = await flet_app_function.tester.find_by_text("Contact page")
    assert contact.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(prefix_routes.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_prefix_routes(flet_app_function: ftt.FletTestApp):
    home_text = await flet_app_function.tester.find_by_text("Select a section above")
    assert home_text.count == 1

    # Pathless layout wraps Users with ADMIN PANEL header
    users_btn = await flet_app_function.tester.find_by_text("Users")
    assert users_btn.count == 1
    await flet_app_function.tester.tap(users_btn)
    await flet_app_function.tester.pump_and_settle()

    users = await flet_app_function.tester.find_by_text("Users page")
    assert users.count == 1
    admin_header = await flet_app_function.tester.find_by_text("ADMIN PANEL")
    assert admin_header.count == 1

    # Path-only grouping — /api/users has no admin layout
    api_users_btn = await flet_app_function.tester.find_by_text("API Users")
    assert api_users_btn.count == 1
    await flet_app_function.tester.tap(api_users_btn)
    await flet_app_function.tester.pump_and_settle()

    api_users = await flet_app_function.tester.find_by_text("API: Users endpoint")
    assert api_users.count == 1
    admin_header = await flet_app_function.tester.find_by_text("ADMIN PANEL")
    assert admin_header.count == 0


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(dynamic_segments.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_dynamic_segments(flet_app_function: ftt.FletTestApp):
    users_heading = await flet_app_function.tester.find_by_text("Users")
    assert users_heading.count == 1

    alice_btn = await flet_app_function.tester.find_by_text("User alice")
    assert alice_btn.count == 1
    await flet_app_function.tester.tap(alice_btn)
    await flet_app_function.tester.pump_and_settle()

    alice = await flet_app_function.tester.find_by_text("User: alice")
    assert alice.count == 1

    post_btn = await flet_app_function.tester.find_by_text("View post #10")
    assert post_btn.count == 1
    await flet_app_function.tester.tap(post_btn)
    await flet_app_function.tester.pump_and_settle()

    post = await flet_app_function.tester.find_by_text("User: alice, Post: 10")
    assert post.count == 1

    back_btn = await flet_app_function.tester.find_by_text("Back to user")
    assert back_btn.count == 1
    await flet_app_function.tester.tap(back_btn)
    await flet_app_function.tester.pump_and_settle()

    alice = await flet_app_function.tester.find_by_text("User: alice")
    assert alice.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(splats.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_splats(flet_app_function: ftt.FletTestApp):
    title = await flet_app_function.tester.find_by_text("File Browser Demo")
    assert title.count == 1

    browse_btn = await flet_app_function.tester.find_by_text(
        "Browse /files/docs/readme.md"
    )
    assert browse_btn.count == 1
    await flet_app_function.tester.tap(browse_btn)
    await flet_app_function.tester.pump_and_settle()

    path_text = await flet_app_function.tester.find_by_text(
        "Current path: docs/readme.md"
    )
    assert path_text.count == 1


# ---------------------------------------------------------------------------
# Data / state examples
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(loaders.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_loaders(flet_app_function: ftt.FletTestApp):
    home_title = await flet_app_function.tester.find_by_text("Home")
    assert home_title.count >= 1  # "Home" appears in button + heading
    message = await flet_app_function.tester.find_by_text("Welcome to the app!")
    assert message.count == 1

    products_btn = await flet_app_function.tester.find_by_text("Products")
    assert products_btn.count == 1
    await flet_app_function.tester.tap(products_btn)
    await flet_app_function.tester.pump_and_settle()

    widget = await flet_app_function.tester.find_by_text("Widget A")
    assert widget.count == 1

    await flet_app_function.tester.tap(widget)
    await flet_app_function.tester.pump_and_settle()

    stock = await flet_app_function.tester.find_by_text("In stock: 42")
    assert stock.count == 1

    back_btn = await flet_app_function.tester.find_by_text("Back to products")
    assert back_btn.count == 1
    await flet_app_function.tester.tap(back_btn)
    await flet_app_function.tester.pump_and_settle()

    gadget = await flet_app_function.tester.find_by_text("Gadget B")
    assert gadget.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(runtime_routes.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_runtime_routes(flet_app_function: ftt.FletTestApp):
    home = await flet_app_function.tester.find_by_text("Home page")
    assert home.count == 1

    # Admin button not yet present
    admin_btn_before = await flet_app_function.tester.find_by_text("Admin")
    assert admin_btn_before.count == 0

    add_btn = await flet_app_function.tester.find_by_text("Add Admin Route")
    assert add_btn.count == 1
    await flet_app_function.tester.tap(add_btn)
    await flet_app_function.tester.pump_and_settle()

    admin_btn = await flet_app_function.tester.find_by_text("Admin")
    assert admin_btn.count == 1
    await flet_app_function.tester.tap(admin_btn)
    await flet_app_function.tester.pump_and_settle()

    admin_panel = await flet_app_function.tester.find_by_text(
        "Admin panel (dynamically added!)"
    )
    assert admin_panel.count == 1

    remove_btn = await flet_app_function.tester.find_by_text("Remove Admin Route")
    assert remove_btn.count == 1
    await flet_app_function.tester.tap(remove_btn)
    await flet_app_function.tester.pump_and_settle()

    home = await flet_app_function.tester.find_by_text("Home page")
    assert home.count == 1
    admin_btn_after = await flet_app_function.tester.find_by_text("Admin")
    assert admin_btn_after.count == 0


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(auth_page.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_auth_page(flet_app_function: ftt.FletTestApp):
    login_title = await flet_app_function.tester.find_by_text("Login")
    assert login_title.count == 1

    sign_in_btn = await flet_app_function.tester.find_by_text("Sign In")
    assert sign_in_btn.count == 1
    await flet_app_function.tester.tap(sign_in_btn)
    await flet_app_function.tester.pump_and_settle()

    dashboard = await flet_app_function.tester.find_by_text(
        "Dashboard — Welcome, admin!"
    )
    assert dashboard.count == 1

    logout_btn = await flet_app_function.tester.find_by_text("Logout")
    assert logout_btn.count == 1
    await flet_app_function.tester.tap(logout_btn)
    await flet_app_function.tester.pump_and_settle()

    login_title = await flet_app_function.tester.find_by_text("Login")
    assert login_title.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(auth_dialog.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_auth_dialog(flet_app_function: ftt.FletTestApp):
    dialog_title = await flet_app_function.tester.find_by_text("Please log in")
    assert dialog_title.count == 1

    login_btn = await flet_app_function.tester.find_by_text("Login")
    assert login_btn.count == 1
    await flet_app_function.tester.tap(login_btn)
    await flet_app_function.tester.pump_and_settle()

    greeting = await flet_app_function.tester.find_by_text("Home — Hello, admin!")
    assert greeting.count == 1

    logout_btn = await flet_app_function.tester.find_by_text("Logout")
    assert logout_btn.count == 1
    await flet_app_function.tester.tap(logout_btn)
    await flet_app_function.tester.pump_and_settle()

    dialog_title = await flet_app_function.tester.find_by_text("Please log in")
    assert dialog_title.count == 1


# ---------------------------------------------------------------------------
# Featured example
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_main(featured.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_featured(flet_app_function: ftt.FletTestApp):
    sign_in = await flet_app_function.tester.find_by_text("Sign In")
    assert sign_in.count == 1

    login_btn = await flet_app_function.tester.find_by_text("Login")
    assert login_btn.count == 1
    await flet_app_function.tester.tap(login_btn)
    await flet_app_function.tester.pump_and_settle()

    greeting = await flet_app_function.tester.find_by_text(
        "Welcome to the Router Demo!"
    )
    assert greeting.count == 1
    featured_count = await flet_app_function.tester.find_by_text(
        "3 featured projects available"
    )
    assert featured_count.count == 1

    browse_btn = await flet_app_function.tester.find_by_text("Browse projects")
    assert browse_btn.count == 1
    await flet_app_function.tester.tap(browse_btn)
    await flet_app_function.tester.pump_and_settle()

    flet_project = await flet_app_function.tester.find_by_text("Flet")
    assert flet_project.count == 1
    await flet_app_function.tester.tap(flet_project)
    await flet_app_function.tester.pump_and_settle()

    description = await flet_app_function.tester.find_by_text("Build apps in Python")
    assert description.count == 1

    back_btn = await flet_app_function.tester.find_by_text("Back to projects")
    assert back_btn.count == 1
    await flet_app_function.tester.tap(back_btn)
    await flet_app_function.tester.pump_and_settle()

    flutter_project = await flet_app_function.tester.find_by_text("Flutter")
    assert flutter_project.count == 1

    # Navigate to settings via nav link
    settings_link = await flet_app_function.tester.find_by_text("Settings")
    assert settings_link.count >= 1
    await flet_app_function.page.push_route("/settings")
    await flet_app_function.tester.pump_and_settle()

    sections_text = await flet_app_function.tester.find_by_text("Available sections:")
    assert sections_text.count == 1
    profile_item = await flet_app_function.tester.find_by_text("Profile")
    assert profile_item.count == 1
    await flet_app_function.tester.tap(profile_item)
    await flet_app_function.tester.pump_and_settle()

    profile_title = await flet_app_function.tester.find_by_text("Profile Settings")
    assert profile_title.count == 1


# ---------------------------------------------------------------------------
# manage_views examples
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_views_main(nested_routes.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_nested_routes(flet_app_function: ftt.FletTestApp):
    home_title = await flet_app_function.tester.find_by_text("Home")
    assert home_title.count >= 1  # appears in AppBar and body

    go_products_btn = await flet_app_function.tester.find_by_text("Go to Products")
    assert go_products_btn.count == 1
    await flet_app_function.tester.tap(go_products_btn)
    await flet_app_function.tester.pump_and_settle()

    products_title = await flet_app_function.tester.find_by_text("All Products")
    assert products_title.count == 1

    product1_btn = await flet_app_function.tester.find_by_text("View Product #1")
    assert product1_btn.count == 1
    await flet_app_function.tester.tap(product1_btn)
    await flet_app_function.tester.pump_and_settle()

    details = await flet_app_function.tester.find_by_text("Details for product #1")
    assert details.count == 1

    # AppBar back → go to products
    back_btn = await flet_app_function.tester.find_by_tooltip("Back")
    assert back_btn.count == 1
    await flet_app_function.tester.tap(back_btn)
    await flet_app_function.tester.pump_and_settle()

    products_title = await flet_app_function.tester.find_by_text("All Products")
    assert products_title.count == 1

    # AppBar back → go to home
    back_btn = await flet_app_function.tester.find_by_tooltip("Back")
    assert back_btn.count == 1
    await flet_app_function.tester.tap(back_btn)
    await flet_app_function.tester.pump_and_settle()

    go_products_btn = await flet_app_function.tester.find_by_text("Go to Products")
    assert go_products_btn.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_views_main(nested_outlet_views.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_nested_outlet_views(flet_app_function: ftt.FletTestApp):
    welcome = await flet_app_function.tester.find_by_text("Welcome!")
    assert welcome.count == 1

    browse_btn = await flet_app_function.tester.find_by_text("Browse Products")
    assert browse_btn.count == 1
    await flet_app_function.tester.tap(browse_btn)
    await flet_app_function.tester.pump_and_settle()

    products_title = await flet_app_function.tester.find_by_text("All Products")
    assert products_title.count == 1
    # Shared layout footer visible on products list
    footer = await flet_app_function.tester.find_by_text("Products Footer")
    assert footer.count == 1

    product1_btn = await flet_app_function.tester.find_by_text("View Product #1")
    assert product1_btn.count == 1
    await flet_app_function.tester.tap(product1_btn)
    await flet_app_function.tester.pump_and_settle()

    product_title = await flet_app_function.tester.find_by_text("Product #1")
    assert product_title.count == 1
    # Footer still present — shared layout wraps the detail view too
    footer = await flet_app_function.tester.find_by_text("Products Footer")
    assert footer.count == 1

    # AppBar back → products list
    back_btn = await flet_app_function.tester.find_by_tooltip("Back")
    assert back_btn.count == 1
    await flet_app_function.tester.tap(back_btn)
    await flet_app_function.tester.pump_and_settle()

    products_title = await flet_app_function.tester.find_by_text("All Products")
    assert products_title.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_views_main(featured_views.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_featured_views(flet_app_function: ftt.FletTestApp):
    welcome = await flet_app_function.tester.find_by_text("Welcome to the app!")
    assert welcome.count == 1

    # Navigate to Projects via URL (NavigationRail tap is flaky in tests).
    await flet_app_function.page.push_route("/projects")
    await flet_app_function.tester.pump_and_settle()

    projects_title = await flet_app_function.tester.find_by_text("All Projects")
    assert projects_title.count == 1
    project_btn = await flet_app_function.tester.find_by_text("Landing Page Redesign")
    assert project_btn.count == 1

    # Note: the example deliberately pins RootLayout's View.route="/" to
    # avoid slide transitions between top-level destinations. A side-effect
    # is that pushing /projects/:pid can't produce a stacked detail view
    # (all views share the same Navigator key), so we only assert on the
    # top-level destinations here.

    # Settings with tabs — General by default
    await flet_app_function.page.push_route("/settings/general")
    await flet_app_function.tester.pump_and_settle()

    general_title = await flet_app_function.tester.find_by_text("General Settings")
    assert general_title.count == 1

    # Switch to Account tab
    await flet_app_function.page.push_route("/settings/account")
    await flet_app_function.tester.pump_and_settle()

    account_title = await flet_app_function.tester.find_by_text("Account Settings")
    assert account_title.count == 1


@pytest.mark.parametrize(
    "flet_app_function",
    [{"flet_app_main": _make_render_views_main(app_drawer.App)}],
    indirect=True,
)
@pytest.mark.asyncio(loop_scope="function")
async def test_app_drawer(flet_app_function: ftt.FletTestApp):
    welcome = await flet_app_function.tester.find_by_text("Welcome")
    assert welcome.count == 1

    browse_btn = await flet_app_function.tester.find_by_text("Browse Apps")
    assert browse_btn.count == 1
    await flet_app_function.tester.tap(browse_btn)
    await flet_app_function.tester.pump_and_settle()

    your_apps = await flet_app_function.tester.find_by_text("Your apps")
    assert your_apps.count == 1

    app_btn = await flet_app_function.tester.find_by_text("Acme Web")
    assert app_btn.count == 1
    await flet_app_function.tester.tap(app_btn)
    await flet_app_function.tester.pump_and_settle()

    app_id_text = await flet_app_function.tester.find_by_text("App ID: 1")
    assert app_id_text.count == 1

    # Open Settings drawer via in-content button (simpler than the AppBar icon)
    open_settings = await flet_app_function.tester.find_by_text("Open Settings")
    assert open_settings.count == 1
    await flet_app_function.tester.tap(open_settings)
    await flet_app_function.tester.pump_and_settle()

    general_title = await flet_app_function.tester.find_by_text("General Settings")
    assert general_title.count == 1

    # Deep-link directly to Permissions tab
    await flet_app_function.page.push_route("/apps/1/settings/permissions")
    await flet_app_function.tester.pump_and_settle()

    permissions_title = await flet_app_function.tester.find_by_text("Permissions")
    assert permissions_title.count >= 1
    permission_switch = await flet_app_function.tester.find_by_text(
        "Require 2FA for admins"
    )
    assert permission_switch.count == 1
