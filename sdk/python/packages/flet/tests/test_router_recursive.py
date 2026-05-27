"""Unit tests for `Route(recursive=True)` matching.

A recursive route matches itself as its own descendant — one
`_RouteMatch` per consumed URL segment. The matcher tries
non-recursive children before self-recursion at every depth so a
specific sibling (e.g. `example/:gp*`) wins over the recursive
`:slug`.

These tests exercise `_match_routes` directly. View emission with
one stack entry per recursion level is exercised by the
`recursive_routes` integration test that drives the example app.
"""

from flet.components.router import Route, _match_routes


def _dummy():
    pass


def _paths(chain):
    """Helper — pull (route_path, params, resolved_path) from a chain."""
    return [(m.route.path, m.params, m.resolved_path) for m in chain]


# ---------------------------------------------------------------------------
# Basic recursion — one match per segment
# ---------------------------------------------------------------------------


def test_recursive_route_matches_single_segment():
    """A recursive route at the depth-1 URL produces exactly one
    recursive match (the leaf)."""
    folder = Route(
        path="folder",
        component=_dummy,
        children=[
            Route(path=":name", component=_dummy, recursive=True),
        ],
    )
    chain = _match_routes([folder], "/folder/docs")

    assert chain is not None
    assert [m.route.path for m in chain] == ["folder", ":name"]
    assert chain[1].params == {"name": "docs"}
    assert chain[1].resolved_path == "/folder/docs"


def test_recursive_route_matches_three_levels():
    """`/folder/a/b/c` produces three `:name` matches. Each level's
    `resolved_path` accumulates the consumed prefix."""
    folder = Route(
        path="folder",
        component=_dummy,
        children=[
            Route(path=":name", component=_dummy, recursive=True),
        ],
    )
    chain = _match_routes([folder], "/folder/a/b/c")

    assert chain is not None
    # 1 base ("folder") + 3 recursive levels.
    assert len(chain) == 4
    assert chain[0].route.path == "folder"
    for m, expected in zip(
        chain[1:], [("a", "/folder/a"), ("b", "/folder/a/b"), ("c", "/folder/a/b/c")]
    ):
        slug, resolved = expected
        assert m.route.path == ":name"
        assert m.route.recursive is True
        assert m.params == {"name": slug}
        assert m.resolved_path == resolved


def test_recursive_route_unbounded_depth():
    """No fixed upper bound on recursion depth."""
    folder = Route(
        path="folder",
        component=_dummy,
        children=[
            Route(path=":name", component=_dummy, recursive=True),
        ],
    )
    deep_url = "/folder/" + "/".join(f"d{i}" for i in range(12))
    chain = _match_routes([folder], deep_url)

    assert chain is not None
    assert len(chain) == 13  # 1 base + 12 recursive
    assert chain[-1].resolved_path == deep_url


# ---------------------------------------------------------------------------
# Sibling specificity — non-recursive child wins over self-recursion
# ---------------------------------------------------------------------------


def test_non_recursive_sibling_wins_at_root_depth():
    """A non-recursive child declared as a sibling of the recursive
    route matches before self-recursion at every depth — here the root
    depth. `/folder/search` lands on Search, not on Folder(search)."""
    folder = Route(
        path="folder",
        component=_dummy,
        children=[
            Route(path="search", component=_dummy),
            Route(path=":name", component=_dummy, recursive=True),
        ],
    )
    chain = _match_routes([folder], "/folder/search")

    assert chain is not None
    assert [m.route.path for m in chain] == ["folder", "search"]


def test_non_recursive_sibling_wins_at_recursive_child_depth():
    """The same rule applies inside the recursive route itself — a
    `search` child of the recursive `:name` wins over self-recursion
    at every depth."""
    search = Route(path="search", component=_dummy)
    folder = Route(
        path="folder",
        component=_dummy,
        children=[
            Route(
                path=":name",
                component=_dummy,
                recursive=True,
                children=[search],
            ),
        ],
    )

    chain = _match_routes([folder], "/folder/a/b/search")
    assert chain is not None
    # base + 2 recursive (a, b) + search leaf
    assert [m.route.path for m in chain] == ["folder", ":name", ":name", "search"]
    assert chain[-1].route is search
    assert chain[-1].resolved_path == "/folder/a/b/search"

    # Same rule one level deeper.
    chain = _match_routes([folder], "/folder/a/b/c/search")
    assert chain is not None
    assert [m.route.path for m in chain] == [
        "folder",
        ":name",
        ":name",
        ":name",
        "search",
    ]


def test_recursive_route_consumes_only_when_no_sibling_matches():
    """If the next segment doesn't match any non-recursive child, the
    recursive route self-recurses and consumes the segment."""
    folder = Route(
        path="folder",
        component=_dummy,
        children=[
            Route(path="search", component=_dummy),
            Route(path=":name", component=_dummy, recursive=True),
        ],
    )
    chain = _match_routes([folder], "/folder/a")
    assert chain is not None
    assert [m.route.path for m in chain] == ["folder", ":name"]
    assert chain[1].params == {"name": "a"}


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


def test_recursive_route_alone_at_root_matches_each_segment():
    """A recursive route declared at the top level (no path parent)
    still emits one match per consumed segment."""
    routes = [
        Route(path=":name", component=_dummy, recursive=True),
    ]
    chain = _match_routes(routes, "/a/b/c")
    assert chain is not None
    assert len(chain) == 3
    assert [m.params["name"] for m in chain] == ["a", "b", "c"]
    assert chain[-1].resolved_path == "/a/b/c"


def test_recursive_route_trailing_slash_treated_as_terminator():
    """Both `/folder/a` and `/folder/a/` terminate at the same
    leaf match — the trailing slash isn't consumed as another empty
    recursion."""
    folder = Route(
        path="folder",
        component=_dummy,
        children=[
            Route(path=":name", component=_dummy, recursive=True),
        ],
    )
    a = _match_routes([folder], "/folder/a")
    a_slash = _match_routes([folder], "/folder/a/")
    assert a is not None and a_slash is not None
    assert len(a) == len(a_slash) == 2
    assert a[-1].params == a_slash[-1].params == {"name": "a"}


def test_recursive_route_with_splat_child_at_every_depth():
    """The canonical `gallery` pattern from the studio app: a recursive
    `:slug` with an `example/:gp*` child. The splat child wins over
    self-recursion at any depth."""
    example = Route(path="example/:gp*", component=_dummy)
    gallery = Route(
        path="gallery",
        component=_dummy,
        children=[
            Route(path="example/:gp*", component=_dummy),  # /gallery/example/<gp>
            Route(
                path=":slug",
                component=_dummy,
                recursive=True,
                children=[example],
            ),
        ],
    )

    # Flat deep-link.
    chain = _match_routes([gallery], "/gallery/example/foo/bar")
    assert chain is not None
    assert [m.route.path for m in chain] == ["gallery", "example/:gp*"]
    assert chain[-1].params == {"gp": "foo/bar"}

    # Nested under one slug.
    chain = _match_routes([gallery], "/gallery/a/example/foo")
    assert chain is not None
    assert [m.route.path for m in chain] == [
        "gallery",
        ":slug",
        "example/:gp*",
    ]
    assert chain[1].params == {"slug": "a"}
    assert chain[-1].params == {"gp": "foo"}

    # Nested under multiple slugs.
    chain = _match_routes([gallery], "/gallery/a/b/c/example/foo")
    assert chain is not None
    assert [m.route.path for m in chain] == [
        "gallery",
        ":slug",
        ":slug",
        ":slug",
        "example/:gp*",
    ]
    assert chain[-1].params == {"gp": "foo"}
