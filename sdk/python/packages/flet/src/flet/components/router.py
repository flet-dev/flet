"""
Router — React Router-like declarative routing for Flet components.

Provides nested route matching, layout routes with outlets, dynamic segments,
optional segments, splats, data loaders, navigation hooks, and view-stack
navigation with swipe-back gesture support.
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
    "use_view_path",
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
    component should call :func:`~flet.use_route_outlet` to render the
    matched child.

    Args:
        path: Relative path segment. Supports dynamic segments (`:name`),
            optional segments (`:name?`), splats (`:name*`), and custom
            regex constraints (`:name(\\\\d+)`). `None` for pathless
            layout routes.
        index: When `True`, this route matches when the parent path
            matches exactly (no further segments). Index routes must not
            have `path` or `children`.
        component: A `@component` function to render when this route
            matches.
        children: Nested child routes.
        loader: Optional data loader function. Called with the matched
            params dict when the route matches. Result is available via
            :func:`~flet.use_route_loader_data`.
        outlet: When `True` and `manage_views=True`, this route acts
            as a layout that wraps its matched child via
            :func:`~flet.use_route_outlet` within a single
            :class:`~flet.View`, instead of each child becoming a separate
            :class:`~flet.View`.
        modal: When `True` and `manage_views=True`, the route's View
            is rendered as a modal overlay on top of the existing stack
            instead of replacing it. The route's component should set
            `fullscreen_dialog=True` on its returned :class:`~flet.View`
            so Flutter renders the slide-up presentation and a close (X)
            icon. Placement controls the base stack:

            * Declared at the **top level**: a *global* modal. The base
              stack is rebuilt from the last non-modal location the
              Router saw (defaults to `"/"` on first render).
            * Declared as a **child** of a non-modal route: a *local*
              modal. The base stack is the chain above the modal in the
              route tree, so deep-link works from the URL alone.

            On pop, the Router navigates to the resolved URL of the
            non-modal parent — never to `views[-2].route` — so a
            modal close is always a real navigation back to the
            base location.
        recursive: When `True`, the route can match itself as its own
            descendant — one matched `_RouteMatch` per consumed segment.
            Useful for tree-shaped URLs with unbounded depth
            (e.g. `/folder/a/b/c`) where each segment should become its
            own stack entry. Non-recursive children are tried before
            self-recursion at every depth so a more specific sibling
            (e.g. `example/:gp*`) wins over the recursive `:slug`.
    """

    path: str | None = None
    index: bool = False
    component: Callable | None = None
    children: list[Route] | None = field(default=None)
    loader: Callable[..., Any] | None = None
    outlet: bool = False
    modal: bool = False
    recursive: bool = False


@dataclass
class LocationInfo:
    """
    Describes the current location parsed from the page route.

    Args:
        pathname: URL path portion (e.g. `/products/42`).
        search: Query string portion without leading `?`.
        hash: Fragment portion without leading `#`.
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
    resolved_path: str = ""


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
    or `None` if no route matches.
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
            return [
                _RouteMatch(
                    route=route,
                    params=m.groupdict(),
                    full_path=full_path,
                    resolved_path=m.group(0),
                )
            ]
        # Also try with trailing slash stripped from pathname
        if pathname.endswith("/") and pathname != "/":
            m = re.match(pattern, pathname.rstrip("/"))
            if m:
                return [
                    _RouteMatch(
                        route=route,
                        params=m.groupdict(),
                        full_path=full_path,
                        resolved_path=m.group(0),
                    )
                ]
        return None

    # Build full path for this route
    route_path = route.path or ""
    full_path = _join_paths(parent_path, route_path)
    if not full_path:
        full_path = "/"

    if route.recursive:
        # Recursive routes consume one matched segment per recursion and
        # try non-recursive children before self-recursing — so a more
        # specific sibling (e.g. `example/:gp*`) wins over the
        # recursive `:slug` at every depth without duplicate
        # declarations.
        prefix_pattern = repath.pattern(full_path, end=False)
        prefix_m = re.match(prefix_pattern, pathname)
        if not prefix_m:
            return None
        consumed = prefix_m.group(0)
        head = _RouteMatch(
            route=route,
            params=prefix_m.groupdict(),
            full_path=full_path,
            resolved_path=consumed,
        )
        # Fully consumed → this is the leaf. Accept either an exact
        # match or a trailing "/" remainder (so /folder/a and
        # /folder/a/ both terminate cleanly).
        remainder = pathname[len(consumed) :]
        if not remainder or remainder == "/":
            return [head]
        # 1) Try non-recursive children first (more specific match).
        for child in route.children or []:
            if child is route:
                continue
            child_result = _try_match(child, pathname, consumed)
            if child_result is not None:
                return [head] + child_result
        # 2) Fall back to self-recursion with the consumed prefix as
        #    the parent path.
        recurse = _try_match(route, pathname, consumed)
        if recurse is None:
            return None
        return [head] + recurse

    if route.children:
        # Parent route — try prefix match to extract params, then match children
        parent_params: dict[str, str] = {}
        parent_resolved = full_path
        if route_path:
            # Only do prefix match if route has a path segment
            prefix_pattern = repath.pattern(full_path, end=False)
            prefix_m = re.match(prefix_pattern, pathname)
            if not prefix_m:
                return None
            parent_params = prefix_m.groupdict()
            parent_resolved = prefix_m.group(0)

        # Try matching children
        for child in route.children:
            child_result = _try_match(child, pathname, full_path)
            if child_result is not None:
                return [
                    _RouteMatch(
                        route=route,
                        params=parent_params,
                        full_path=full_path,
                        resolved_path=parent_resolved,
                    )
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
                        resolved_path=exact_m.group(0),
                    )
                ]

        return None

    # Leaf route — exact match
    leaf_pattern = repath.pattern(full_path)
    m = re.match(leaf_pattern, pathname)
    if m:
        return [
            _RouteMatch(
                route=route,
                params=m.groupdict(),
                full_path=full_path,
                resolved_path=m.group(0),
            )
        ]

    return None


# ---------------------------------------------------------------------------
# Contexts
# ---------------------------------------------------------------------------

_MISSING = object()  # sentinel to detect calls outside Router

_location_context = create_context(_MISSING)
_params_context = create_context(_MISSING)
_outlet_context = create_context(_MISSING)
_loader_data_context = create_context(_MISSING)
_view_path_context = create_context(_MISSING)


def _is_inside_router(value: Any) -> bool:
    """Check if a router hook is called inside a Router component tree."""
    return value is not _MISSING


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------


def use_route_params() -> dict[str, str]:
    """
    Returns all dynamic segment parameters from the current matched route chain.

    Must be called inside a component rendered by a :class:`~flet.Router`.
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

    Must be called inside a component rendered by a :class:`~flet.Router`.
    Returns an empty string if called outside a Router tree.

    Returns:
        The current URL pathname (e.g. `"/products/42"`).
    """
    loc = use_context(_location_context)
    if not _is_inside_router(loc):
        return ""
    return loc.pathname


def use_view_path() -> str:
    """
    Returns the resolved URL for the current view level.

    This differs from :func:`use_route_location` which returns the full
    current URL.  `use_view_path` returns the URL up to the current
    view level (the leaf route of the view in `manage_views=True` mode).

    Useful as the `route` value for :class:`~flet.View` to produce a
    unique Navigator key per view in the stack.

    Must be called inside a component rendered by a :class:`~flet.Router`.
    Returns an empty string if called outside a Router tree.

    Returns:
        The resolved URL for this view level (e.g. `"/products/42"`).
    """
    value = use_context(_view_path_context)
    if not _is_inside_router(value):
        return ""
    return str(value)


def use_route_outlet() -> Control:
    """
    Returns the matched child route's rendered component.

    Used inside layout route components to render the active child route.
    Must be called inside a component rendered by a :class:`~flet.Router`.
    Returns `None` if called outside a Router tree.

    Returns:
        The rendered child component, or `None` if no child matches.
    """
    value = use_context(_outlet_context)
    if not _is_inside_router(value):
        return None
    return value


def use_route_loader_data():
    """
    Returns the data from the current route's loader function.

    Must be called inside a component whose route has a `loader` defined.

    Returns:
        The return value of the route's loader function, or `None`.
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
        exact: If `True`, requires an exact match. If `False` (default),
            a prefix match is used (e.g. `"/products"` matches
            `"/products/42"`).

    Returns:
        `True` if the path matches the current location.
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

    Only **pathless** routes (no `path`, not `index`) with a component
    are treated as layouts that wrap every View.  All other routes with
    a component become their own View in the stack.

    Returns:
        A tuple of (layouts, view_entries) where:
        - layouts: pathless routes with components that wrap every View
        - view_entries: path-bearing routes, each becoming its own View.
          Each entry is `(match, accumulated_path)`.
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
    a tree of :class:`~flet.Route` definitions and renders the matched
    component chain.

    The Router subscribes to :attr:`~flet.Page.on_route_change`
    and re-renders automatically when the route changes.

    Navigation is done via :meth:`~flet.Page.push_route` or
    :meth:`~flet.Page.navigate`.

    When `manage_views` is `True`, the Router returns a list of
    :class:`~flet.View` objects (one per path level) instead of a single
    component tree. This enables swipe-back gestures, system back button,
    and :class:`~flet.AppBar` implicit back button on mobile.
    Must be used with :meth:`~flet.Page.render_views`.

    Args:
        routes: List of top-level :class:`~flet.Route` definitions.
        not_found: Optional component to render when no route matches (404).
        manage_views: When `True`, produce a list of
            :class:`~flet.View` objects (one per path level) instead of a
            single component tree. Route components should return
            :class:`~flet.View` instances with `route` and `appbar`
            set. Use with :meth:`~flet.Page.render_views`.

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
    # Last non-modal location the Router saw. Used as the base for
    # global modal routes (declared at the top level) — when the user
    # navigates from /apps/X to /settings (modal=True), the modal is
    # rendered ON TOP OF the chain matched against /apps/X, so closing
    # it reveals the original stack instead of rebuilding it.
    prev_non_modal_location_ref = use_ref(None)
    # Snapshot of the chain emitted for the current location. Used by
    # the default pop handler to compute the parent URL structurally
    # (`chain[-2].resolved_path`), which survives shared `view.route`
    # keys (e.g. an app that uses the same route key for two sibling
    # tab roots to suppress switch animations).
    current_chain_ref = use_ref(None)
    # URL to navigate to when popping the topmost view, IF the current
    # chain ends in a modal route. `None` otherwise. Set whenever a
    # modal route matches.
    current_modal_pop_to_ref = use_ref(None)

    # Subscribe to route changes on mount
    def setup_listeners():
        prev_route_handler_ref.current = page.on_route_change

        def on_route_change(e):
            set_location(e.route)

        page.on_route_change = on_route_change

        if manage_views:
            prev_pop_handler_ref.current = page.on_view_pop

            def on_view_pop(e):
                # If the app installed its own `page.on_view_pop` before
                # the Router mounted, delegate to it. Apps can still
                # override entirely (e.g. for a stack visualisation or
                # confirmation flow).
                prev = prev_pop_handler_ref.current
                if prev is not None:
                    prev(e)
                    return

                # Modal pop: navigate to the base URL stamped at emit
                # time. Same logic for global and local modals — the
                # base URL was resolved when the modal was matched.
                if current_modal_pop_to_ref.current is not None:
                    page.navigate(current_modal_pop_to_ref.current)
                    return

                # Non-modal pop: navigate to the previous *view entry*'s
                # resolved URL rather than `chain[-2]` or
                # `views[-2].route`. Classifying into view entries skips
                # `outlet=True` layouts and componentless grouping routes
                # — otherwise `chain[-2]` can point at a layout whose URL
                # equals the current view's URL, making the pop navigate
                # to where we already are (a no-op that strands the URL).
                # Staying route-tree-structural also survives shared view
                # keys like a tab-root layout emitting `route="/"` for
                # multiple sibling sections.
                chain_now = current_chain_ref.current
                if chain_now:
                    _, view_entries = _split_chain_into_view_levels(chain_now)
                    if len(view_entries) > 1:
                        parent_match = view_entries[-2][0]
                        target = (
                            parent_match.resolved_path or parent_match.full_path or "/"
                        )
                        page.navigate(target)
                        return

                # Stack of length 1 — nothing to pop to. (Flutter's
                # `Navigator.canPop` is False here anyway.)

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

                # Reset state so a stale modal pop_to doesn't leak into
                # a 404'd location.
                current_chain_ref.current = None
                current_modal_pop_to_ref.current = None
                return [View(route=pathname, controls=[not_found()])]
            return not_found()
        return None

    # Detect modal routes in the chain. `modal_idx` is the index of
    # the first route in the chain with `modal=True`; `-1` means
    # the chain is fully non-modal.
    modal_idx = -1
    for i, m in enumerate(chain):
        if m.route.modal:
            modal_idx = i
            break

    # For a *global* modal (`modal_idx == 0` — the chain starts at a
    # modal with no non-modal parents) we want the visible stack to be
    # the chain of the previously visited non-modal location +
    # the modal's own chain. This way the underlying stack stays mounted
    # underneath the modal — closing the modal reveals it without a
    # rebuild.
    if manage_views and modal_idx == 0:
        base_location = prev_non_modal_location_ref.current or "/"
        base_pathname = _normalize_path(urlparse(base_location).path or "/")
        base_chain = _match_routes(routes, base_pathname) or []
        # If the base path also resolves to a modal (shouldn't happen
        # in practice — non-modal navigations are the only ones that
        # update prev_non_modal_location_ref), fall back to no base.
        if any(b.route.modal for b in base_chain):
            base_chain = []
        # Combine: base lives below, modal sits on top.
        chain = base_chain + chain
        # Re-locate the modal index in the combined chain.
        modal_idx = len(base_chain)

    # Track refs that downstream consumers (default pop handler, etc.)
    # read. `current_chain_ref` always reflects the chain we're
    # actually emitting. `current_modal_pop_to_ref` is set only when
    # the chain ends in a modal — non-modal navigations clear it.
    current_chain_ref.current = chain
    if modal_idx == -1:
        # Non-modal navigation — remember it as the next base.
        prev_non_modal_location_ref.current = location
        current_modal_pop_to_ref.current = None
    else:
        # Modal route — the URL to pop to is the resolved URL of the
        # last non-modal entry in the chain.
        if modal_idx > 0:
            parent = chain[modal_idx - 1]
            current_modal_pop_to_ref.current = (
                parent.resolved_path or parent.full_path or "/"
            )
        else:
            # No non-modal parent in the chain (rare — would require a
            # deep-link to a top-level modal with no remembered base
            # AND an empty default match). Fall back to "/".
            current_modal_pop_to_ref.current = "/"

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
        # Single-view mode (existing behavior). `modal` is ignored
        # here — it only affects stack composition in multi-view mode.
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
    #
    # If the chain contains a modal route, split into two independent
    # sub-chains at the modal boundary. Each sub-chain is classified
    # into layouts vs. view entries SEPARATELY so that an outlet route
    # that would be a leaf view in its own sub-chain doesn't get
    # re-classified as a layout just because there's more chain after
    # the boundary. `modal_idx` already points to the modal route in
    # the (possibly combined) chain.
    # `modal_idx <= 0` covers both the no-modal case (`-1`) and a
    # degenerate modal chain with no base (`0`) — neither is split.
    sub_chains = [chain] if modal_idx <= 0 else [chain[:modal_idx], chain[modal_idx:]]

    # Each sub-chain's views see their own URL via the location
    # context. The base sub-chain (when there's a modal split) sees the
    # remembered non-modal location it was matched against — so
    # `is_route_active("/gallery")` inside a base view stays True
    # while a global `/settings` modal is open over Gallery.
    base_sub_loc = LocationInfo(pathname=pathname, search=search, hash=hash_val)
    if modal_idx > 0:
        base_loc_str = prev_non_modal_location_ref.current or "/"
        base_parsed = urlparse(base_loc_str)
        base_sub_loc = LocationInfo(
            pathname=_normalize_path(base_parsed.path or "/"),
            search=base_parsed.query or "",
            hash=base_parsed.fragment or "",
        )

    results = []
    for sub_chain_idx, sub_chain in enumerate(sub_chains):
        layouts, view_entries = _split_chain_into_view_levels(sub_chain)
        # The base sub-chain (everything before the modal) is rendered
        # "as if" the user is at the previous non-modal URL; the modal
        # sub-chain is rendered at the modal URL.
        sub_loc = base_sub_loc if (modal_idx > 0 and sub_chain_idx == 0) else loc
        for match, _ in view_entries:
            # Params accumulated up to this view level — within the
            # combined chain so a local modal view still sees its
            # parents' captures.
            level_params: dict[str, str] = {}
            for m in chain:
                level_params.update(m.params)
                if m is match:
                    break

            # Per-view resolved URL — unique per view level for
            # Navigator keying.
            level_view_path = match.resolved_path or match.full_path or "/"
            _match = match
            # Only apply layouts that appear before this view entry IN
            # THE SAME SUB-CHAIN. A modal view never inherits the
            # base's layouts (and vice versa).
            match_idx = sub_chain.index(match)
            _layouts = [lm for lm in layouts if sub_chain.index(lm) < match_idx]

            def build_view_content(
                _match=_match,
                _layouts=_layouts,
                _level_params=level_params,
                _level_loc=sub_loc,
                _level_view_path=level_view_path,
                _sub_chain=sub_chain,
            ):
                return _view_path_context(
                    _level_view_path,
                    lambda: _location_context(
                        _level_loc,
                        lambda: _params_context(
                            _level_params,
                            lambda: _build_view_level(
                                _layouts, _match, loader_results, _sub_chain
                            ),
                        ),
                    ),
                )

            results.append(build_view_content())

    return results
