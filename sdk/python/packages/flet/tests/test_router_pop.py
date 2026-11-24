"""Unit tests for the non-modal view-pop target computation.

The `Router`'s default `on_view_pop` handler navigates to the previous
*view entry*'s resolved URL when the top view is popped. It must derive
that target from the chain's view entries (`_split_chain_into_view_levels`)
rather than `chain[-2]`: an intermediate `outlet=True` layout sits in the
chain between two views but is NOT a view of its own, and its resolved URL
can equal the current view's URL. Using `chain[-2]` there would navigate to
the URL we're already at — a no-op that leaves the page route stranded so
the next navigation to the same URL does nothing.

This replicates the handler's target computation (the handler itself is a
closure inside `Router`) the same way `test_router_modal` replicates the
modal-index lookup.
"""

from flet.components.router import (
    Route,
    _match_routes,
    _split_chain_into_view_levels,
)


def _dummy():  # placeholder component — Route requires a callable
    pass


def _pop_target(chain):
    """Replicates the Router's non-modal pop-target computation."""
    if not chain:
        return None
    _, view_entries = _split_chain_into_view_levels(chain)
    if len(view_entries) > 1:
        parent_match = view_entries[-2][0]
        return parent_match.resolved_path or parent_match.full_path or "/"
    return None


# Mirrors examples/apps/router/nested_outlet_views: a Home route whose
# child is an `outlet=True` products layout wrapping its own children.
_routes = [
    Route(
        component=_dummy,
        children=[
            Route(
                path="products",
                component=_dummy,
                outlet=True,
                children=[
                    Route(
                        component=_dummy,
                        children=[
                            Route(path=":pid", component=_dummy),
                        ],
                    ),
                ],
            ),
        ],
    ),
]


def test_pop_from_outlet_layout_view_skips_layout():
    """`/products` builds views [Home(/), Products(/products)] but the
    chain is [Home, products-layout, ProductsList]. Popping the Products
    view must land on Home (`/`) — not the layout's own `/products`,
    which `chain[-2]` would wrongly yield."""
    chain = _match_routes(_routes, "/products")

    assert chain is not None
    # The layout really is `chain[-2]` and shares the leaf's resolved URL,
    # which is exactly the trap the view-entry computation avoids.
    assert chain[-2].route.outlet is True
    assert chain[-2].resolved_path == "/products"

    assert _pop_target(chain) == "/"


def test_pop_from_nested_product_lands_on_products_list():
    """`/products/1` builds views [Home(/), ProductsList(/products),
    ProductDetails(/products/1)]. Popping the details view lands on the
    products list (`/products`)."""
    chain = _match_routes(_routes, "/products/1")

    assert chain is not None
    assert _pop_target(chain) == "/products"


def test_single_view_has_no_pop_target():
    """At `/` the stack is one view — nothing to pop to."""
    chain = _match_routes(_routes, "/")

    assert chain is not None
    assert _pop_target(chain) is None
