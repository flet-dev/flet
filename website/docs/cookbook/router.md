---
title: "Router"
---

Router is a declarative routing system for Flet apps, inspired by React Router.
It handles nested route matching, layout routes with outlets, dynamic segments,
data loading, view-stack navigation, and provides hooks for accessing route state.

## Why Router?

Without Router, multi-page Flet apps require manual route matching, conditional
rendering, and parameter extraction. Router automates all of this:

- **Nested routes** — define parent/child hierarchies
- **Layout routes** — share layouts across pages using [use_route_outlet()](../types/use_route_outlet.md)
- **Dynamic segments** — `:paramName` in paths, accessed via [use_route_params()](../types/use_route_params.md)
- **Data loading** — fetch data before rendering with `loader`
- **Active link detection** — highlight nav items with [is_route_active()](../types/is_route_active.md)
- **View-stack navigation** — swipe-back and AppBar back button with `manage_views=True`

## Quick start

```python
@ft.component
def Home():
    return ft.Text("Welcome home!")

@ft.component
def About():
    return ft.Text("About us")

@ft.component
def App():
    return ft.Router([
        ft.Route(index=True, component=Home),
        ft.Route(path="about", component=About),
    ])

ft.run(lambda page: page.render(App))
```

See [full example](../controls/router.md#basic).

## Defining routes

Routes are defined as a tree of [Route](../types/route.md) objects.

### Flat routes

All routes at the top level:

```python
ft.Router([
    ft.Route(index=True, component=Home),
    ft.Route(path="about", component=About),
    ft.Route(path="contact", component=Contact),
])
```

### Nested routes

Child routes are nested under parent routes. The parent's path is
automatically prepended:

```python
ft.Route(
    path="products",
    component=ProductsList,
    children=[
        ft.Route(path=":pid", component=ProductDetails),
    ],
)
# /products → ProductsList
# /products/42 → ProductDetails (params: {"pid": "42"})
```

See [full example](../controls/router.md#dynamic-segments).

### Index routes

An index route (`index=True`) matches when the parent path matches exactly,
with no further segments:

```python
ft.Route(path="settings", children=[
    ft.Route(index=True, component=SettingsHome),   # /settings
    ft.Route(path="profile", component=Profile),     # /settings/profile
])
```

### Prefix routes

**Pathless layout routes** — group children under a shared layout without
adding a path segment:

```python
ft.Route(component=AdminLayout, children=[
    ft.Route(path="users", component=Users),       # /users
    ft.Route(path="settings", component=Settings), # /settings
])
```

**Path-only routes** — add a path prefix without rendering a component:

```python
ft.Route(path="api", children=[
    ft.Route(path="users", component=ApiUsers),        # /api/users
    ft.Route(path="products", component=ApiProducts),   # /api/products
])
```

## Layout routes and `use_route_outlet()`

A layout route has both a `component` and `children`. Its component renders
shared UI (header, sidebar, footer) and calls [use_route_outlet()](../types/use_route_outlet.md)
to place the matched child:

```python
@ft.component
def AppLayout():
    outlet = ft.use_route_outlet()
    return ft.Column([
        ft.AppBar(title=ft.Text("My App")),
        ft.Container(content=outlet, expand=True),
        ft.Text("Footer"),
    ])

ft.Router([
    ft.Route(component=AppLayout, children=[
        ft.Route(index=True, component=Home),
        ft.Route(path="about", component=About),
    ]),
])
```

Layout routes can be nested to any depth. Each level calls `use_route_outlet()` to
get its immediate child. See [full example](../controls/router.md#layout-with-outlet).

## Dynamic segments, optional segments, and splats

Route paths support Express-style patterns via the `repath` library.

**Dynamic segments** — `:paramName` matches a single path segment:

```python
ft.Route(path="users/:userId", component=UserProfile)
# /users/42 → use_route_params() returns {"userId": "42"}
```

**Optional segments** — `:paramName?` may be absent:

```python
ft.Route(path="users/:userId?", component=UserProfile)
# /users → {"userId": None}
# /users/42 → {"userId": "42"}
```

**Splats (catch-all)** — `:paramName*` matches zero or more segments:

```python
ft.Route(path="files/:path*", component=FileBrowser)
# /files/a/b/c → {"path": "a/b/c"}
```

**Custom regex** — `:paramName(\\d+)` constrains a segment:

```python
ft.Route(path="item/:id(\\d+)", component=ItemDetails)
# /item/42 → matches
# /item/abc → does NOT match
```

## Navigation

Use [page.navigate()](../controls/page.md#flet.Page.navigate) from synchronous callbacks:

```python
ft.Button("About", on_click=lambda: ft.context.page.navigate("/about"))
```

For async contexts, use [page.push_route()](../controls/page.md#flet.Page.push_route) with `await`.
The Router automatically re-renders when the route changes.

## Active links with `is_route_active()`

[is_route_active(path)](../types/is_route_active.md) returns `True` if the given path matches
the current location:

```python
ft.Button(
    "Products",
    style=ft.ButtonStyle(
        bgcolor=ft.Colors.PRIMARY_CONTAINER
        if ft.is_route_active("/products")
        else None,
    ),
    on_click=lambda: ft.context.page.navigate("/products"),
)
```

By default it uses prefix matching — `is_route_active("/products")` returns
`True` for `/products/42`. Pass `exact=True` for exact matching.
See [full example](../controls/router.md#active-links).

## Data loading

Routes can define a `loader` function. It runs when the route matches and its
return value is available via [use_route_loader_data()](../types/use_route_loader_data.md):

```python
def load_user(params):
    return db.get_user(params["userId"])

ft.Route(path="users/:userId", component=UserProfile, loader=load_user)
```

```python
@ft.component
def UserProfile():
    user = ft.use_route_loader_data()
    return ft.Text(f"Hello, {user.name}")
```

See [full example](../controls/router.md#loaders).

## Authentication

Auth is implemented using layout routes as guards — no special Router API needed.

**Page redirect** — redirect to `/login` if not authenticated:

```python
@ft.component
def ProtectedRoute():
    outlet = ft.use_route_outlet()
    if not auth.is_authenticated:
        ft.context.page.navigate("/login")
        return ft.Text("Redirecting...")
    return outlet
```

**Role-based access** — nest guard routes for layered access control:

```python
ft.Router([
    ft.Route(component=ProtectedRoute, children=[
        ft.Route(index=True, component=Home),
        ft.Route(component=AdminOnly, children=[
            ft.Route(path="admin", component=AdminPanel),
        ]),
    ]),
])
```

## 404 handling

Pass a `not_found` component to render when no route matches:

```python
@ft.component
def NotFound():
    location = ft.use_route_location()
    return ft.Text(f"Page not found: {location}")

ft.Router(routes, not_found=NotFound)
```

## Multi-view navigation

By default, Router renders all route content within a single [View](../controls/view.md).
With `manage_views=True`, the Router returns a list of Views — one per path level.
This enables:

- Swipe-back gesture on mobile
- System back button
- [AppBar](../controls/appbar.md) implicit back button
- Slide transition between route levels

Use [page.render_views()](../controls/page.md#flet.Page.render_views) instead of
`page.render()`.

### Components return Views

Each route component returns a [View](../controls/view.md) with `route`, `appbar`,
and `controls`:

```python
@ft.component
def ProductDetails():
    params = ft.use_route_params()
    return ft.View(
        route=f"/products/{params['pid']}",
        appbar=ft.AppBar(title=ft.Text(f"Product #{params['pid']}")),
        controls=[
            ft.Text(f"Details for product #{params['pid']}"),
        ],
    )
```

### Nested route hierarchy

Structure routes as a nested tree. A pathless root ensures it is always
in the view stack:

```python
ft.Router([
    ft.Route(component=Home, children=[
        ft.Route(path="products", component=ProductsList, children=[
            ft.Route(path=":pid", component=ProductDetails),
        ]),
    ]),
], manage_views=True)
```

:::tip[View stack]
- `/` — 1 view (Home)
- `/products` — 2 views (Home, Products) — back button to Home
- `/products/1` — 3 views (Home, Products, Product Details) — back button to Products
:::

See [full example](../controls/router.md#managed-views--nested-routes).

### Shared layouts with `outlet=True`

Set `outlet=True` on a route to make it a layout that wraps child routes
via [use_route_outlet()](../types/use_route_outlet.md). The layout returns a
[View](../controls/view.md); child components return regular controls:

```python
@ft.component
def ProductsLayout():
    outlet = ft.use_route_outlet()
    location = ft.use_route_location()
    return ft.View(
        route=location,
        appbar=ft.AppBar(title=ft.Text("Products")),
        controls=[
            ft.Container(content=outlet, expand=True),
            ft.Text("Footer"),
        ],
    )

ft.Route(path="products", component=ProductsLayout, outlet=True, children=[
    ft.Route(component=ProductsList, children=[
        ft.Route(path=":pid", component=ProductDetails),
    ]),
])
```

The layout's shared UI appears on every child route's View, and each child
is still a separate View in the stack — back navigation works between them.
See [full example](../controls/router.md#managed-views--shared-layout-with-outlet).

### Avoiding transition animation

When switching between top-level NavigationRail destinations, set a fixed
`route` value on the root layout's View to prevent slide transitions:

```python
@ft.component
def RootLayout():
    outlet = ft.use_route_outlet()
    return ft.View(
        route="/",  # fixed key — no animation between top-level pages
        can_pop=False,
        controls=[
            ft.Row([
                ft.NavigationRail(...),
                ft.Container(content=outlet, expand=True),
            ], expand=True),
        ],
    )
```

See [full example](../controls/router.md#managed-views--full-app-with-navigationrail).

## Hooks reference

| Hook | Returns | Description |
|------|---------|-------------|
| [use_route_params()](../types/use_route_params.md) | `dict[str, str]` | All dynamic segment values from the matched route chain |
| [use_route_location()](../types/use_route_location.md) | `str` | Current URL pathname |
| [use_route_outlet()](../types/use_route_outlet.md) | component | Matched child route component (for layout routes) |
| [use_route_loader_data()](../types/use_route_loader_data.md) | `Any` | Return value of the current route's `loader` |
| [is_route_active(path)](../types/is_route_active.md) | `bool` | Whether `path` matches the current location |
