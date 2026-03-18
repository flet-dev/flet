Router is a declarative routing system for Flet apps, inspired by React Router.
It handles nested route matching, layout routes with outlets, dynamic segments,
data loading, and provides hooks for accessing route state.

## Why Router?

Without Router, multi-page Flet apps require manual route matching, conditional
rendering, and parameter extraction. Router automates all of this:

- **Nested routes** — define parent/child hierarchies
- **Layout routes** — share layouts across pages using [`use_route_outlet()`][flet.use_route_outlet]
- **Dynamic segments** — `:paramName` in paths, accessed via [`use_route_params()`][flet.use_route_params]
- **Data loading** — fetch data before rendering with `loader`
- **Active link detection** — highlight nav items with [`is_route_active()`][flet.is_route_active]

## Quick start

```python
--8<-- "../../examples/apps/router/basic.py"
```

## Defining routes

Routes are defined as a tree of [`Route`][flet.Route] objects.

### Flat routes

The simplest setup — all routes at the top level:

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
--8<-- "../../examples/apps/router/nested_routes.py"
```

### Index routes

An index route (`index=True`) matches when the parent path matches exactly,
with no further segments. It's the "default" child for a parent route:

```python
--8<-- "../../examples/apps/router/index_routes.py"
```

### Prefix routes

**Pathless layout routes** — group children under a shared layout without
adding a path segment:

```python
ft.Route(component=AdminLayout, children=[
    ft.Route(path="users", component=Users),     # matches /users
    ft.Route(path="settings", component=Settings), # matches /settings
])
```

**Path-only routes** — add a path prefix without rendering a component:

```python
ft.Route(path="api", children=[
    ft.Route(path="users", component=ApiUsers),      # matches /api/users
    ft.Route(path="products", component=ApiProducts), # matches /api/products
])
```

```python
--8<-- "../../examples/apps/router/prefix_routes.py"
```

## Layout routes and `use_route_outlet()`

A layout route has both a `component` and `children`. Its component renders
shared UI (header, sidebar, footer) and calls [`use_route_outlet()`][flet.use_route_outlet]
to place the matched child:

```python
--8<-- "../../examples/apps/router/layout_outlet.py"
```

Layout routes can be nested to any depth. Each level calls `use_route_outlet()` to
get its immediate child.

## Dynamic segments, optional segments, and splats

Route paths support Express-style patterns via the `repath` library:

### Dynamic segments

`:paramName` matches a single path segment:

```python
ft.Route(path="users/:userId", component=UserProfile)
# /users/42 → use_route_params() returns {"userId": "42"}
```

### Optional segments

`:paramName?` — the segment may be absent:

```python
ft.Route(path="users/:userId?", component=UserProfile)
# /users → {"userId": None}
# /users/42 → {"userId": "42"}
```

### Splats (catch-all)

`:paramName*` — matches zero or more segments:

```python
ft.Route(path="files/:path*", component=FileBrowser)
# /files/a/b/c → {"path": "a/b/c"}
```

```python
--8<-- "../../examples/apps/router/splats.py"
```

### Custom regex

`:paramName(\\d+)` — constrain a segment with a regex pattern:

```python
ft.Route(path="item/:id(\\d+)", component=ItemDetails)
# /item/42 → matches
# /item/abc → does NOT match
```

```python
--8<-- "../../examples/apps/router/dynamic_segments.py"
```

## Navigation

Use [`page.navigate()`][flet.Page.navigate] to navigate from synchronous callbacks:

```python
ft.Button("Go to About", on_click=lambda: ft.context.page.navigate("/about"))
```

For async contexts, use [`page.push_route()`][flet.Page.push_route] directly with `await`.

The Router automatically re-renders when the route changes.

## Active links with `is_route_active()`

[`is_route_active(path)`][flet.is_route_active] returns `True` if the given path matches
the current location. Use it to highlight navigation elements:

```python
--8<-- "../../examples/apps/router/active_links.py"
```

By default, `is_active` uses prefix matching — `is_route_active("/products")` returns
`True` for `/products/42`. Pass `exact=True` for exact matching.

## Data loading

Routes can define a `loader` function that runs when the route matches.
The loader receives the merged params dict and its return value is available
via [`use_route_loader_data()`][flet.use_route_loader_data]:

```python
--8<-- "../../examples/apps/router/loaders.py"
```

## Authentication

Auth is implemented using layout routes as guards — no special Router API needed.

### Page redirect

```python
--8<-- "../../examples/apps/router/auth_page.py"
```

### Dialog overlay

```python
--8<-- "../../examples/apps/router/auth_dialog.py"
```

### Role-based access

Nest guard routes for layered access control:

```python
@ft.component
def AdminOnly():
    auth = ft.use_context(AuthContext)
    outlet = ft.use_route_outlet()
    if not auth.is_admin:
        return ft.Text("403 Forbidden")
    return outlet

ft.Router([
    ft.Route(component=ProtectedRoute, children=[
        ft.Route(index=True, component=Home),
        ft.Route(component=AdminOnly, children=[
            ft.Route(path="admin", component=AdminPanel),
        ]),
    ]),
])
```

## Runtime route modification

Routes are mutable — add, remove, or modify them at any time using
[`use_state`][flet.use_state]:

```python
--8<-- "../../examples/apps/router/runtime_routes.py"
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

## Featured example

A complete app demonstrating layout, navigation, nested routes, dynamic
segments, loaders, and authentication:

```python
--8<-- "../../examples/apps/router/featured.py"
```

## Hooks reference

| Hook | Returns | Description |
|------|---------|-------------|
| [`use_route_params()`][flet.use_route_params] | `dict[str, str]` | All dynamic segment values from the matched route chain |
| [`use_location()`][flet.use_route_location] | `str` | Current URL pathname |
| [`use_route_outlet()`][flet.use_route_outlet] | component | Matched child route component (for layout routes) |
| [`use_route_loader_data()`][flet.use_route_loader_data] | `Any` | Return value of the current route's `loader` |
| [`is_route_active(path)`][flet.is_route_active] | `bool` | Whether `path` matches the current location |
