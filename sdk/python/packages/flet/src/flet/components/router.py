"""
Router — React Router-like declarative routing for Flet components.

Provides nested route matching, layout routes with outlets, dynamic segments,
optional segments, splats, data loaders, and navigation hooks.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Callable
from urllib.parse import urlparse

import repath

from flet.components.component_decorator import component

if TYPE_CHECKING:
    from flet.controls.control import Control
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
        outlet: When ``True`` and ``manage_views=True``, this route acts
            as a layout that wraps its matched child via
            [`use_route_outlet()`][flet.use_route_outlet] within a single
            View, instead of each child becoming a separate View.
    """

    path: str | None = None
    index: bool = False
    component: Callable | None = None
    children: list[Route] | None = field(default=None)
    loader: Callable[..., Any] | None = None
    outlet: bool = False


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
        if route.component:
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


def use_route_outlet() -> Control:
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
# View-stack builder (manage_views=True)
# ---------------------------------------------------------------------------


def _split_chain_into_view_levels(
    chain: list[_RouteMatch],
) -> tuple[list[_RouteMatch], list[tuple[_RouteMatch, str]]]:
    """
    Split matched chain into layout wrappers and view entries.

    Only **pathless** routes (no ``path``, not ``index``) with a component
    are treated as layouts that wrap every View.  All other routes with
    a component become their own View in the stack.

    Returns:
        A tuple of (layouts, view_entries) where:
        - layouts: pathless routes with components that wrap every View
        - view_entries: path-bearing routes, each becoming its own View.
          Each entry is ``(match, accumulated_path)``.
    """
    layouts: list[_RouteMatch] = []
    view_entries: list[tuple[_RouteMatch, str]] = []

    for i, match in enumerate(chain):
        route = match.route
        if route.component is None:
            continue

        is_last = i == len(chain) - 1

        if not is_last and route.outlet:
            # Explicit outlet layout — wraps child views
            layouts.append(match)
        else:
            view_entries.append((match, match.full_path))

    return layouts, view_entries


def _build_view_level(
    layouts: list[_RouteMatch],
    leaf_match: _RouteMatch,
    loader_results: dict[int, Any],
    chain: list[_RouteMatch],
):
    """
    Build the component tree for a single View level.

    Wraps the leaf component in layout outlets and optional loader data.
    """
    leaf_route = leaf_match.route
    leaf_index = chain.index(leaf_match)
    leaf_loader_data = loader_results.get(leaf_index)

    def render_leaf():
        if leaf_loader_data is not None:
            return _loader_data_context(leaf_loader_data, leaf_route.component)
        return leaf_route.component()

    if not layouts:
        return render_leaf()

    # Wrap the leaf in layout outlets from innermost to outermost.
    # The innermost layout gets the leaf as its outlet; each outer layout
    # gets the next inner layout as its outlet.
    current_render = render_leaf
    for layout_match in reversed(layouts):
        layout_route = layout_match.route
        layout_index = chain.index(layout_match)
        layout_loader_data = loader_results.get(layout_index)
        # Capture loop variables
        _lr = layout_route
        _lld = layout_loader_data
        _cr = current_render

        def make_render(_lr=_lr, _lld=_lld, _cr=_cr):
            def render_layout():
                if _lld is not None:
                    return _loader_data_context(_lld, _lr.component)
                return _lr.component()

            return lambda: _outlet_context(_cr(), render_layout)

        current_render = make_render()

    return current_render()


# ---------------------------------------------------------------------------
# Router component
# ---------------------------------------------------------------------------


@component
def Router(
    routes: list[Route],
    not_found: Callable | None = None,
    manage_views: bool = False,
) -> Control:
    """
    Top-level router component that matches the current page route against
    a tree of [`Route`][flet.Route] definitions and renders the matched
    component chain.

    The Router subscribes to [`page.on_route_change`][flet.Page.on_route_change]
    and re-renders automatically when the route changes.

    Navigation is done via the existing [`page.push_route()`][flet.Page.push_route].

    When ``manage_views`` is ``True``, the Router manages
    [`page.views`][flet.Page.views] directly — each path level in the matched
    chain becomes a separate [`View`][flet.View].  This enables swipe-back
    gestures, system back button, and AppBar implicit back button on mobile.
    Must be used with [`page.render_views()`][flet.Page.render_views].

    Args:
        routes: List of top-level route definitions.
        not_found: Optional component to render when no route matches (404).
        manage_views: When ``True``, produce a list of Views (one per path
            level) instead of a single component tree.

    Example:
        ```python
        @ft.component
        def App():
            return ft.Router(
                [
                    ft.Route(index=True, component=Home),
                    ft.Route(path="about", component=About),
                    ft.Route(path="products/:pid", component=ProductDetails),
                ],
                manage_views=True,
            )
        ```
    """
    page = context.page
    location, set_location = use_state(page.route or "/")
    prev_route_handler_ref = use_ref(None)
    prev_pop_handler_ref = use_ref(None)

    # Subscribe to route changes on mount
    def setup_listeners():
        prev_route_handler_ref.current = page.on_route_change

        def on_route_change(e):
            set_location(e.route)

        page.on_route_change = on_route_change

        if manage_views:
            prev_pop_handler_ref.current = page.on_view_pop

            def on_view_pop(e):
                from flet.components.public_utils import unwrap_component

                views_list = unwrap_component(page.views)
                if isinstance(views_list, list) and len(views_list) > 1:
                    prev_view = unwrap_component(views_list[-2])
                    if prev_view is not None:
                        page.navigate(prev_view.route)

            page.on_view_pop = on_view_pop

    def teardown_listeners():
        page.on_route_change = prev_route_handler_ref.current
        if manage_views:
            page.on_view_pop = prev_pop_handler_ref.current

    use_effect(setup_listeners, dependencies=[], cleanup=teardown_listeners)

    # Parse location
    parsed = urlparse(location)
    pathname = _normalize_path(parsed.path or "/")
    search = parsed.query or ""
    hash_val = parsed.fragment or ""

    # Match routes
    chain = _match_routes(routes, pathname)

    if chain is None:
        if not_found is not None:
            if manage_views:
                from flet.controls.core.view import View

                return [View(route=pathname, controls=[not_found()])]
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

    if not manage_views:
        # Single-view mode (existing behavior)
        return _location_context(
            loc,
            lambda: _params_context(
                all_params, lambda: _build_outlet_chain(chain, loader_results)
            ),
        )

    # Multi-view mode: return a list of route component results.
    # Each route component should return a View (with appbar, controls,
    # route, etc.).  The Router sets route and can_pop on each View
    # after the component body executes (via the patch walk).
    # Used with page.render_views(App).
    layouts, view_entries = _split_chain_into_view_levels(chain)

    results = []
    for match, view_path in view_entries:
        # Params accumulated up to this view level
        level_params: dict[str, str] = {}
        for m in chain:
            level_params.update(m.params)
            if m is match:
                break

        level_loc = LocationInfo(pathname=view_path, search=search, hash=hash_val)
        _match = match
        # Only apply layouts that appear before this view entry in the chain
        match_idx = chain.index(match)
        _layouts = [lm for lm in layouts if chain.index(lm) < match_idx]

        def build_view_content(
            _match=_match,
            _layouts=_layouts,
            _level_params=level_params,
            _level_loc=level_loc,
        ):
            return _location_context(
                _level_loc,
                lambda: _params_context(
                    _level_params,
                    lambda: _build_view_level(_layouts, _match, loader_results, chain),
                ),
            )

        results.append(build_view_content())

    return results
