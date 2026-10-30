"""Tests for `page.query`, which parses the query string of `page.route` on read."""

import gc

import pytest

from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub


class _Connection(Connection):
    def __init__(self, page_url: str):
        super().__init__()
        self.pubsubhub = PubSubHub()
        self.page_url = page_url

    def send_message(self, message):
        pass


def _open(route: str, page_url: str = "ws://127.0.0.1:8550") -> Session:
    """Return a session whose page was opened at `route`, as on client connect."""
    session = Session(_Connection(page_url))
    session.apply_page_patch({"route": route})
    return session


async def _change_route(session: Session, route: str):
    """Change the route the way the client does: patch it, then fire the event."""
    session.apply_page_patch({"route": route})
    await session.page._trigger_event("route_change", {"route": route})


@pytest.mark.parametrize(
    "page_url",
    ["ws://127.0.0.1:8550", "/tmp/flet.sock", "http://127.0.0.1:8550/?name=Joe"],
    ids=["web", "desktop", "pyodide"],
)
@pytest.mark.asyncio
async def test_query_follows_the_current_route(page_url):
    """`page.query` follows `page.route` in `main()`, `on_route_change` and later."""
    session = _open("/products?name=Joe&id=1", page_url)
    page = session.page

    assert page.query.get("name") == "Joe"
    assert page.query.to_dict == {"name": "Joe", "id": "1"}
    assert page.query.path == "/products"

    seen = []
    page.on_route_change = lambda e: seen.append((page.query.path, page.query.to_dict))
    await _change_route(session, "/store?name=Ann")
    assert seen == [("/store", {"name": "Ann"})]

    page.route = "/"
    assert page.query.path == "/"
    assert page.query.to_dict == {}
    with pytest.raises(KeyError):
        page.query.get("name")


@pytest.mark.parametrize(
    "route, path, params",
    [
        ("/a?next=/b?c=1", "/a", {"next": "/b?c=1"}),
        ("/a?tag=x&tag=y&tag=&debug", "/a", {"tag": "y"}),
        ("/books/42?tab=reviews#details", "/books/42", {"tab": "reviews"}),
        ("/books/42#details?tab=reviews", "/books/42", {}),
        ("//books/42?x=1", "//books/42", {"x": "1"}),
    ],
)
@pytest.mark.asyncio
async def test_query_splits_path_query_and_fragment(route, path, params):
    """The route splits at the first `?`, without the fragment or blank values."""
    session = _open("/")
    await _change_route(session, route)

    assert session.page.query.path == path
    assert session.page.query.to_dict == params


@pytest.mark.asyncio
async def test_push_route_parameters_read_back_decoded_once(monkeypatch):
    """Parameters passed to `push_route` read back from `page.query` as strings."""
    session = _open("/")
    page = session.page
    pushed = []

    async def invoke_method(method_name, arguments=None, timeout=None):
        pushed.append(arguments["route"])

    monkeypatch.setattr(page, "_invoke_method", invoke_method)
    await page.push_route(
        "/search", q="salt & pepper", tag="c++", next="/cart#pay", limit=20
    )
    await _change_route(session, pushed[0])

    assert page.query.path == "/search"
    assert page.query.to_dict == {
        "q": "salt & pepper",
        "tag": "c++",
        "next": "/cart#pay",
        "limit": "20",
    }


def test_query_is_empty_once_the_page_is_gone():
    """A `QueryString` that outlives its page has an empty path and no parameters."""
    session = _open("/products?name=Joe")
    query = session.page.query
    del session
    gc.collect()

    assert query.path == ""
    assert query.to_dict == {}
