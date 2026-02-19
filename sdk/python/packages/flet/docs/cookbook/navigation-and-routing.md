Navigation and routing is the core of building multi-screen Flet apps.
It lets you organize your UI into virtual pages ([`View`][flet.View] objects),
keep URL/history in sync, and support deep links to specific app states.

This page focuses on the current routing model and maintained examples.

## Routing model in Flet

A [`Page`][flet.Page] is a container of views ([`page.views`][flet.Page.views]), where each view represents one route-level screen.

- [`page.route`][flet.Page.route] is the current route string (for example `/`, `/store`, `/settings/mail`).
- [`page.views`][flet.Page.views] is the active navigation stack.
- [`page.on_route_change`][flet.Page.on_route_change] rebuilds the stack when route changes.
- [`page.on_view_pop`][flet.Page.on_view_pop] handles Back navigation (system Back, AppBar Back, browser Back).

A reliable setup uses a single source of truth: derive [`page.views`][flet.Page.views] from [`page.route`][flet.Page.route].

## Route basics

The default route is `/` when no route is provided.

```python
--8<-- "../../examples/apps/routing_navigation/initial_route.py"
```

All routes should start with `/`, for example `/store`, `/products/42`, `/settings/mail`.

## Handling route changes

Whenever route changes (URL edit, browser Back/Forward, or app navigation),
[`page.on_route_change`][flet.Page.on_route_change] event is triggered.
Use this event as the place where you decide which views must exist for the current route.

```python
--8<-- "../../examples/apps/routing_navigation/route_change_event.py"
```

## Building views from route

The pattern below is the baseline for most apps:

1. Clear [`page.views`][flet.Page.views].
2. Add root view (`/`).
3. Add extra views conditionally based on [`page.route`][flet.Page.route].
4. Handle Back in [`page.on_view_pop`][flet.Page.on_view_pop] and navigate to the new top view.

/// admonition | Why is this pattern important?
    type: tip
- Keeps URL, history stack, and visible UI synchronized.
- Supports deep links and reloads naturally.
- Makes navigation deterministic and easier to debug.
///

```python
--8<-- "../../examples/apps/routing_navigation/building_views_on_route_change.py"
```

## Programmatic navigation

Use [`page.push_route()`][flet.Page.push_route] to navigate.

You can also pass query parameters as keyword arguments:

```python
await page.push_route("/search", q="flet", page=2)
```

## Back navigation and pop confirmation

When users go back, Flet triggers [`page.on_view_pop`][flet.Page.on_view_pop].
For flows requiring confirmation (for example, unsaved changes), disable automatic pop
and confirm manually with [`View.can_pop`][flet.View.can_pop] + [`View.on_confirm_pop`][flet.View.on_confirm_pop].

```python
--8<-- "../../examples/apps/routing_navigation/pop_view_confirm.py"
```

## Navigation UI patterns

Routing composes well with navigation controls such as drawer, rail, and tabs.
This example shows route-driven drawer navigation with multiple top-level destinations:

```python
--8<-- "../../examples/apps/routing_navigation/drawer_navigation.py"
```

## Route templates (parameterized routes)

Use [`TemplateRoute`][flet.TemplateRoute] to match and parse route parameters, for example `/books/:id`.
Template syntax is provided by [repath](https://github.com/nickcoutsos/python-repath#parameters).

```python
import flet as ft

troute = ft.TemplateRoute(page.route)

if troute.match("/books/:id"):
    print("Book ID:", troute.id)
elif troute.match("/account/:account_id/orders/:order_id"):
    print("Account:", troute.account_id, "Order:", troute.order_id)
else:
    print("Unknown route")
```

## Web URL strategy

Flet web apps support two URL strategies :

- `"path"` (default): in the form `https://myapp.dev/store`
- `"hash"`: `https://myapp.dev/#/store`

It can be set via `route_url_strategy` in `ft.run()`
```python
import flet as ft
ft.run(main, route_url_strategy="hash")
```

For Flet server deployments, you can also set the [`FLET_ROUTE_URL_STRATEGY`](../reference/environment-variables.md#flet_web_route_url_strategy)
environment variable.

## Practical recommendations

- Always keep a root `/` view in [`page.views`][flet.Page.views].
- Keep route handling centralized in [`page.on_route_change`][flet.Page.on_route_change]; avoid mutating [`page.views`][flet.Page.views] from many places.
- When adding new routes, test these cases: direct deep link, browser Back/Forward, app Back button, and reload.
- Use route templates for dynamic segments instead of manual string splitting.
