"""Modal routes — fullscreen-dialog overlays that don't unmount the
underlying stack.

A route marked ``modal=True`` is rendered on top of the previous
location's view stack. Closing the modal pops it without rebuilding
the views underneath — they stay mounted.

Two flavours, distinguished by placement in the route tree:

* **Global modal** — declared at the top level. Reachable from
  anywhere with a single URL; the base stack comes from the last
  non-modal location the Router saw. Demonstrated by ``/settings`` here.

* **Local modal** — declared as a child of a non-modal parent. The URL
  embeds the parent's path, so deep-link works without any state.
  Demonstrated by ``/items/<id>/edit`` here.
"""

import flet as ft

# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------


@ft.component
def Home():
    page = ft.context.page
    return ft.View(
        route="/",
        appbar=ft.AppBar(title=ft.Text("Home")),
        controls=[
            ft.Text("Welcome!", size=22, weight=ft.FontWeight.BOLD),
            ft.Button(
                "Open Items",
                on_click=lambda: page.navigate("/items"),
            ),
            ft.Button(
                "Open Settings (global modal)",
                on_click=lambda: page.navigate("/settings"),
            ),
        ],
    )


ITEMS = {"1": "Apples", "2": "Bananas", "3": "Cherries"}


@ft.component
def ItemList():
    page = ft.context.page
    return ft.View(
        route="/items",
        appbar=ft.AppBar(title=ft.Text("Items")),
        controls=[
            ft.Text("Pick an item:"),
            *[
                ft.Button(
                    name,
                    on_click=lambda _e, i=iid: page.navigate(f"/items/{i}"),
                )
                for iid, name in ITEMS.items()
            ],
            ft.Button(
                "Open Settings (global modal)",
                on_click=lambda: page.navigate("/settings"),
            ),
        ],
    )


@ft.component
def ItemDetails():
    page = ft.context.page
    params = ft.use_route_params()
    iid = params["id"]
    name = ITEMS.get(iid, "Unknown")
    return ft.View(
        route=ft.use_view_path(),
        appbar=ft.AppBar(title=ft.Text(f"Item: {name}")),
        controls=[
            ft.Text(f"Details for item {iid}: {name}"),
            ft.Button(
                "Edit (local modal)",
                on_click=lambda: page.navigate(f"/items/{iid}/edit"),
            ),
            ft.Button(
                "Open Settings (global modal)",
                on_click=lambda: page.navigate("/settings"),
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Modals
# ---------------------------------------------------------------------------


@ft.component
def SettingsModal():
    """Global modal — `/settings` works from any base location."""
    return ft.View(
        route="/settings",
        fullscreen_dialog=True,
        appbar=ft.AppBar(title=ft.Text("Settings")),
        controls=[
            ft.Text("Account / System / About would live here."),
            ft.Text(
                "Close the modal — the underlying view (Home, Items, or "
                "Item details) is still mounted underneath, no rebuild.",
                size=12,
                color=ft.Colors.ON_SURFACE_VARIANT,
            ),
        ],
    )


@ft.component
def EditItemModal():
    """Local modal — `/items/<id>/edit` is pinned to a specific item.

    Deep-link to it directly and the stack rebuilds from URL alone:
    `[ItemList, ItemDetails(id), EditItemModal]`.
    """
    params = ft.use_route_params()
    iid = params["id"]
    name = ITEMS.get(iid, "Unknown")
    return ft.View(
        route=ft.use_view_path(),
        fullscreen_dialog=True,
        appbar=ft.AppBar(title=ft.Text(f"Edit {name}")),
        controls=[
            ft.Text(f"Editing item {iid}"),
            ft.TextField(label="Name", value=name),
            ft.Text(
                "URL: " + ft.context.page.route,
                size=12,
                color=ft.Colors.ON_SURFACE_VARIANT,
            ),
        ],
    )


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------


@ft.component
def App():
    return ft.Router(
        [
            # Pathless parent so /items/<id> stacks on top of Home.
            ft.Route(
                component=Home,
                children=[
                    ft.Route(
                        path="items",
                        component=ItemList,
                        children=[
                            ft.Route(
                                path=":id",
                                component=ItemDetails,
                                children=[
                                    # Local modal — child of /items/:id.
                                    ft.Route(
                                        path="edit",
                                        component=EditItemModal,
                                        modal=True,
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # Global modal — top-level route, reachable from anywhere.
            ft.Route(path="settings", component=SettingsModal, modal=True),
        ],
        manage_views=True,
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render_views(App))
