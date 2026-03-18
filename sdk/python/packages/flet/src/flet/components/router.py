"""
Router — React Router-like declarative routing for Flet components.

Provides nested route matching, layout routes with outlets, dynamic segments,
optional segments, splats, data loaders, and navigation hooks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Callable
from urllib.parse import urlparse

import repath

from flet.components.component_decorator import component
from flet.components.hooks.use_context import create_context, use_context
from flet.components.hooks.use_effect import use_effect
from flet.components.hooks.use_ref import use_ref
from flet.components.hooks.use_state import use_state
from flet.controls.context import context

__all__ = [
    "LocationInfo",
    "Route",
    "Router",
    "is_route_active",
    "use_route_loader_data",
    "use_route_location",
    "use_route_outlet",
    "use_route_params",
]

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class Route:
    """
    Defines a single route in the route tree.

    Routes can be nested via `children` to create layout hierarchies.
    A route with `component` and `children` acts as a layout route — its
    component should call [`use_route_outlet()`][flet.use_route_outlet] to render the
    matched child.

    Args:
        path: Relative path segment. Supports dynamic segments (`:name`),
            optional segments (`:name?`), splats (`:name*`), and custom
            regex constraints (`:name(\\\\d+)`). ``None`` for pathless
            layout routes.
        index: When ``True``, this route matches when the parent path
            matches exactly (no further segments). Index routes must not
            have ``path`` or ``children``.
        component: A ``@component`` function to render when this route
            matches.
        children: Nested child routes.
        loader: Optional data loader function. Called with the matched
            params dict when the route matches. Result is available via
            [`use_route_loader_data()`][flet.use_route_loader_data].
    """

    path: str | None = None
    index: bool = False
    component: Callable | None = None
    children: list[Route] | None = field(default=None)
    loader: Callable[..., Any] | None = None


@dataclass
class LocationInfo:
    """
    Describes the current location parsed from the page route.

    Args:
        pathname: URL path portion (e.g. ``/products/42``).
        search: Query string portion without leading ``?``.
        hash: Fragment portion without leading ``#``.
    """

    pathname: str
    search: str = ""
    hash: str = ""


# ---------------------------------------------------------------------------
# Internal: route matching
# ---------------------------------------------------------------------------


@dataclass
class _RouteMatch:
    """One matched level in the route chain."""

    route: Route
    params: dict[str, str]
    full_path: str


def _join_paths(parent: str, child: str) -> str:
    """Join parent and child path segments, normalizing slashes."""
    if not child:
        return parent
    parent = parent.rstrip("/")
    if not child.startswith("/"):
        child = "/" + child
    return parent + child


def _normalize_path(path: str) -> str:
    """Ensure path starts with / and has no trailing /."""
    if not path:
        return "/"
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path


def _match_routes(
    routes: list[Route],
    pathname: str,
    parent_path: str = "",
) -> list[_RouteMatch] | None:
    """
    Match pathname against route tree.

    Returns a chain of matched routes from outermost to innermost,
    or ``None`` if no route matches.
    """
    for route in routes:
        result = _try_match(route, pathname, parent_path)
        if result is not None:
            return result
    return None


def _try_match(
    route: Route,
    pathname: str,
    parent_path: str,
) -> list[_RouteMatch] | None:
    """Try to match a single route (and its children) against pathname."""

    if route.index:
        # Index routes match the parent path exactly
        full_path = _normalize_path(parent_path) if parent_path else "/"
        pattern = repath.pattern(full_path)
        m = re.match(pattern, pathname)
        if m:
            return [_RouteMatch(route=route, params=m.groupdict(), full_path=full_path)]
        # Also try with trailing slash stripped from pathname
        if pathname.endswith("/") and pathname != "/":
            m = re.match(pattern, pathname.rstrip("/"))
            if m:
                return [
                    _RouteMatch(route=route, params=m.groupdict(), full_path=full_path)
                ]
        return None

    # Build full path for this route
    route_path = route.path or ""
    full_path = _join_paths(parent_path, route_path)
    if not full_path:
        full_path = "/"

    if route.children:
        # Parent route — try prefix match to extract params, then match children
        parent_params: dict[str, str] = {}
        if route_path:
            # Only do prefix match if route has a path segment
            prefix_pattern = repath.pattern(full_path, end=False)
            prefix_m = re.match(prefix_pattern, pathname)
            if not prefix_m:
                return None
            parent_params = prefix_m.groupdict()

        # Try matching children
        for child in route.children:
            child_result = _try_match(child, pathname, full_path)
            if child_result is not None:
                return [
                    _RouteMatch(route=route, params=parent_params, full_path=full_path)
                ] + child_result

        # No children matched — if this route has a component, try exact match
        if route.component and route_path:
            exact_pattern = repath.pattern(full_path)
            exact_m = re.match(exact_pattern, pathname)
            if exact_m:
                return [
                    _RouteMatch(
                        route=route,
                        params=exact_m.groupdict(),
                        full_path=full_path,
                    )
                ]

        return None

    # Leaf route — exact match
    leaf_pattern = repath.pattern(full_path)
    m = re.match(leaf_pattern, pathname)
    if m:
        return [_RouteMatch(route=route, params=m.groupdict(), full_path=full_path)]

    return None


# ---------------------------------------------------------------------------
# Contexts
# ---------------------------------------------------------------------------

_MISSING = object()  # sentinel to detect calls outside Router

_location_context = create_context(_MISSING)
_params_context = create_context(_MISSING)
_outlet_context = create_context(_MISSING)
_loader_data_context = create_context(_MISSING)


def _is_inside_router(value: Any) -> bool:
    """Check if a router hook is called inside a Router component tree."""
    return value is not _MISSING


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------


def use_route_params() -> dict[str, str]:
    """
    Returns all dynamic segment parameters from the current matched route chain.

    Must be called inside a component rendered by a [`Router`][flet.Router].
    Returns an empty dict if called outside a Router tree (e.g. during a
    stale observable re-render).

    Returns:
        Dictionary mapping parameter names to their matched string values.
    """
    value = use_context(_params_context)
    if not _is_inside_router(value):
        return {}
    return value


def use_route_location() -> str:
    """
    Returns the current location pathname.

    Must be called inside a component rendered by a [`Router`][flet.Router].
    Returns an empty string if called outside a Router tree.

    Returns:
        The current URL pathname (e.g. ``"/products/42"``).
    """
    loc = use_context(_location_context)
    if not _is_inside_router(loc):
        return ""
    return loc.pathname


def use_route_outlet():
    """
    Returns the matched child route's rendered component.

    Used inside layout route components to render the active child route.
    Must be called inside a component rendered by a [`Router`][flet.Router].
    Returns ``None`` if called outside a Router tree.

    Returns:
        The rendered child component, or ``None`` if no child matches.
    """
    value = use_context(_outlet_context)
    if not _is_inside_router(value):
        return None
    return value


def use_route_loader_data():
    """
    Returns the data from the current route's loader function.

    Must be called inside a component whose route has a ``loader`` defined.

    Returns:
        The return value of the route's loader function, or ``None``.
    """
    value = use_context(_loader_data_context)
    if not _is_inside_router(value):
        return None
    return value


def is_route_active(path: str, exact: bool = False) -> bool:
    """
    Check whether the given path matches the current location.

    Useful for highlighting active navigation links or tabs.

    Args:
        path: Path to check against the current location.
        exact: If ``True``, requires an exact match. If ``False`` (default),
            a prefix match is used (e.g. ``"/products"`` matches
            ``"/products/42"``).

    Returns:
        ``True`` if the path matches the current location.
    """
    loc = use_context(_location_context)
    if not _is_inside_router(loc):
        return False
    pathname = loc.pathname
    path = _normalize_path(path)

    if exact or path == "/":
        return pathname == path

    return pathname == path or pathname.startswith(path + "/")


# ---------------------------------------------------------------------------
# Outlet chain builder
# ---------------------------------------------------------------------------


def _build_outlet_chain(
    chain: list[_RouteMatch],
    loader_results: dict[int, Any],
    index: int = 0,
):
    """
    Build nested outlet context providers from the match chain.

    Recursively processes the chain from outermost (index=0) to innermost.
    Each level wraps the next level as its outlet context.
    """
    # Skip routes without components (path-only grouping)
    while index < len(chain) and chain[index].route.component is None:
        index += 1

    if index >= len(chain):
        return None

    matched = chain[index]
    route = matched.route
    loader_data = loader_results.get(index)

    # Recursively build the child outlet
    child = _build_outlet_chain(chain, loader_results, index + 1)

    def render_level():
        """Render this route level's component, optionally wrapped with loader data."""
        if loader_data is not None:
            return _loader_data_context(loader_data, route.component)
        return route.component()

    if child is not None:
        # Layout route: provide child as outlet, then render this level
        return _outlet_context(child, render_level)
    else:
        # Leaf route: just render
        return render_level()


# ---------------------------------------------------------------------------
# Router component
# ---------------------------------------------------------------------------


@component
def Router(routes: list[Route], not_found: Callable | None = None):
    """
    Top-level router component that matches the current page route against
    a tree of [`Route`][flet.Route] definitions and renders the matched
    component chain.

    The Router subscribes to [`page.on_route_change`][flet.Page.on_route_change]
    and re-renders automatically when the route changes.

    Navigation is done via the existing [`page.push_route()`][flet.Page.push_route].

    Args:
        routes: List of top-level route definitions.
        not_found: Optional component to render when no route matches (404).

    Example:
        ```python
        @ft.component
        def App():
            return ft.Router(
                [
                    ft.Route(index=True, component=Home),
                    ft.Route(path="about", component=About),
                    ft.Route(path="products/:pid", component=ProductDetails),
                ]
            )
        ```
    """
    page = context.page
    location, set_location = use_state(page.route or "/")
    prev_handler_ref = use_ref(None)

    # Subscribe to route changes on mount
    def setup_route_listener():
        prev_handler_ref.current = page.on_route_change

        def on_route_change(e):
            set_location(e.route)

        page.on_route_change = on_route_change

    def teardown_route_listener():
        page.on_route_change = prev_handler_ref.current

    use_effect(setup_route_listener, dependencies=[], cleanup=teardown_route_listener)

    # Parse location
    parsed = urlparse(location)
    pathname = _normalize_path(parsed.path or "/")
    search = parsed.query or ""
    hash_val = parsed.fragment or ""

    # Match routes
    chain = _match_routes(routes, pathname)

    if chain is None:
        if not_found is not None:
            return not_found()
        return None

    # Merge all params from the chain
    all_params: dict[str, str] = {}
    for m in chain:
        all_params.update(m.params)

    # Run loaders
    loader_results: dict[int, Any] = {}
    for i, m in enumerate(chain):
        if m.route.loader is not None:
            loader_results[i] = m.route.loader(all_params)

    # Build location info
    loc = LocationInfo(pathname=pathname, search=search, hash=hash_val)

    # Wrap outlet chain in location + params contexts
    return _location_context(
        loc,
        lambda: _params_context(
            all_params, lambda: _build_outlet_chain(chain, loader_results)
        ),
    )
