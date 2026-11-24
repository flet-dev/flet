"""Unit tests for `Route(modal=True)` matching.

The modal flag itself is not exercised by `_match_routes` — it's
consumed by the `Router` component when emitting views. These tests
cover the matching layer: the `modal_idx` location in the chain
behaves as documented for both global and local modals, and the
fields the Router reads from each match are populated correctly.

End-to-end behaviour (chain combination with the previous non-modal
location, `modal_pop_to` stamping, no-flash close) is exercised by
the `modal_routes` integration test that drives the example app
through the Flet testing harness.
"""

from flet.components.router import Route, _match_routes


def _dummy():  # placeholder component — Route requires a callable
    pass


def _find_modal_idx(chain):
    """Replicates the Router's modal-index lookup."""
    for i, m in enumerate(chain):
        if m.route.modal:
            return i
    return -1


# ---------------------------------------------------------------------------
# Global modal — declared at the top level
# ---------------------------------------------------------------------------


def test_global_modal_matches_as_first_chain_entry():
    """A top-level modal with no parents in the tree matches at index 0
    of the chain. The Router uses this signal to compose the visible
    stack from the previous non-modal location + the modal chain.
    """
    settings = Route(
        path="settings",
        component=_dummy,
        modal=True,
        outlet=True,
        children=[Route(index=True, component=_dummy)],
    )
    routes = [Route(component=_dummy), settings]

    chain = _match_routes(routes, "/settings")

    assert chain is not None
    assert _find_modal_idx(chain) == 0
    assert chain[0].route is settings


def test_global_modal_with_subpath_keeps_modal_at_index_0():
    """`/settings/system` still has the modal route at index 0; the
    deeper match (the System tab) is at index 1 with its own params."""
    settings = Route(
        path="settings",
        component=_dummy,
        modal=True,
        outlet=True,
        children=[
            Route(path="system", component=_dummy),
        ],
    )
    chain = _match_routes([settings], "/settings/system")

    assert chain is not None
    assert _find_modal_idx(chain) == 0
    assert chain[0].route.modal is True
    assert chain[1].route.path == "system"


# ---------------------------------------------------------------------------
# Local modal — child of a non-modal parent
# ---------------------------------------------------------------------------


def test_local_modal_index_reflects_nesting_depth():
    """A modal nested under non-modal parents reports its index as the
    number of non-modal ancestors. `modal_pop_to` is derived from
    `chain[modal_idx-1].resolved_path`, which here resolves to the
    parent `/items/<id>` URL."""
    edit = Route(path="edit", component=_dummy, modal=True)
    routes = [
        Route(
            component=_dummy,
            children=[
                Route(
                    path="items",
                    component=_dummy,
                    children=[
                        Route(path=":id", component=_dummy, children=[edit]),
                    ],
                ),
            ],
        ),
    ]

    chain = _match_routes(routes, "/items/42/edit")

    assert chain is not None
    modal_idx = _find_modal_idx(chain)
    # parent (pathless) → "items" → ":id" → modal "edit" — modal at index 3
    assert modal_idx == 3
    assert chain[modal_idx].route is edit
    # chain[modal_idx-1] is the modal's direct non-modal parent.
    parent = chain[modal_idx - 1]
    assert parent.params == {"id": "42"}
    assert parent.resolved_path == "/items/42"


def test_local_modal_preserves_parents_params_in_chain():
    """Each match in the chain exposes every dynamic segment captured up
    to and including that match's own path (parents' captures included
    via the joined regex). So the modal route at `/items/:id/edit`
    sees `{"id": "abc"}` on its own match — the Router's
    `use_route_params()` consumer would see the same dict whether it
    reads from the modal's match alone or the accumulated chain.
    """
    edit = Route(path="edit", component=_dummy, modal=True)
    items = Route(
        path="items",
        component=_dummy,
        children=[
            Route(path=":id", component=_dummy, children=[edit]),
        ],
    )
    chain = _match_routes([items], "/items/abc/edit")

    assert chain is not None
    id_match = next(m for m in chain if m.route.path == ":id")
    assert id_match.params == {"id": "abc"}
    edit_match = next(m for m in chain if m.route is edit)
    # The matcher carries parent captures into the leaf's regex too —
    # `id` is still bound for the modal so it can fetch the right
    # item record via `use_route_params()`.
    assert edit_match.params == {"id": "abc"}


# ---------------------------------------------------------------------------
# Non-modal navigation — sanity / regression
# ---------------------------------------------------------------------------


def test_non_modal_chain_has_modal_idx_minus_one():
    """When no route in the matched chain is modal, the helper returns
    `-1` — the Router uses this to update
    `prev_non_modal_location_ref`."""
    routes = [
        Route(
            component=_dummy,
            children=[
                Route(path="items", component=_dummy),
            ],
        ),
    ]
    chain = _match_routes(routes, "/items")

    assert chain is not None
    assert _find_modal_idx(chain) == -1
    assert all(not m.route.modal for m in chain)


def test_modal_flag_does_not_change_match_outcome_for_non_modal_url():
    """A modal route declared in the tree must not affect matching of
    unrelated URLs."""
    routes = [
        Route(path="home", component=_dummy),
        Route(path="settings", component=_dummy, modal=True),
    ]
    home_chain = _match_routes(routes, "/home")
    settings_chain = _match_routes(routes, "/settings")

    assert home_chain is not None
    assert _find_modal_idx(home_chain) == -1
    assert settings_chain is not None
    assert _find_modal_idx(settings_chain) == 0
