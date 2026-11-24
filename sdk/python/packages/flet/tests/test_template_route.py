"""Tests for `TemplateRoute`, which matches route templates against a route path."""

import pytest

import flet as ft


@pytest.mark.parametrize(
    "route, template, params",
    [
        ("/store?ref=ad", "/store", {}),
        ("/books/42?tab=reviews", "/books/:id", {"id": "42"}),
        ("/books/42/?tab=reviews", "/books/:id", {"id": "42"}),
        ("/books/42?next=/books/43", "/books/:id", {"id": "42"}),
        ("/books/42#details?tab=reviews", "/books/:id", {"id": "42"}),
        ("/books?tab=reviews", "/books/:id?", {"id": None}),
        ("//books/42?x=1", "//books/:id", {"id": "42"}),
    ],
)
def test_template_route_matches_the_path_only(route, template, params):
    """A route matches the template of its path whatever its query and fragment."""
    troute = ft.TemplateRoute(route)

    assert troute.match(template)
    assert {k: getattr(troute, k) for k in params} == params
    assert troute.route == route


def test_template_route_clears_parameters_on_a_failed_match():
    """A failed match returns `False` and resets the previous match's parameters."""
    troute = ft.TemplateRoute("/books/42?next=/store")
    assert troute.match("/books/:id")

    assert not troute.match("/store")
    assert troute.id is None
