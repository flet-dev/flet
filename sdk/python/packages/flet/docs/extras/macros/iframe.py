import os
from typing import Optional
from urllib.parse import urlparse

# Default iframe base can be overridden for local dev via FLET_IFRAME_BASE.
# Points to the published examples gallery bundled with the docs.
DEFAULT_IFRAME_BASE = os.environ.get(
    "FLET_IFRAME_BASE", "/apps/examples-gallery/dist/index.html#/"
)


def _prettify_token(token: str) -> str:
    return " ".join(
        word.title() for word in token.replace("-", " ").replace("_", " ").split()
    )


def _pretty_from_route(route: str) -> str:
    parts = [p for p in route.split("/") if p]
    if not parts:
        return "iframe"
    if len(parts) == 1:
        return _prettify_token(parts[0])
    # Use the last two segments for nested routes, e.g. charts/line_chart/example_1 -> Line Chart / Example 1
    tail = parts[-2:]
    return " / ".join(_prettify_token(p) for p in tail)


def render_iframe(
    src=None,
    *,
    route=None,
    base: Optional[str] = None,
    width: str = "100%",
    height: str = "480",
    title: Optional[str] = None,
    allow: Optional[str] = None,
    loading: str = "lazy",
) -> str:
    """
    Build an iframe HTML snippet.

    When route is provided, the iframe source is constructed from the base URL.
    The base defaults to the published examples gallery served by MkDocs:
    /apps/examples-gallery/dist/index.html#/ (override with FLET_IFRAME_BASE).
    """
    base = base or DEFAULT_IFRAME_BASE

    if route:
        parsed_base = urlparse(base)
        if parsed_base.fragment:
            fragment = parsed_base.fragment.rstrip("/")
            new_fragment = fragment + "/" + route.lstrip("/")
            parsed_base = parsed_base._replace(fragment=new_fragment)
            src = parsed_base.geturl()
        else:
            src = base.rstrip("/") + "/" + route.lstrip("/")
    if not src:
        raise ValueError("Either src or route must be provided")

    if title is None:
        # Prefer a human-friendly title from the route when available, even if
        # the underlying src includes an index.html with a fragment.
        if route:
            title = _pretty_from_route(route)
        else:
            parsed = urlparse(src)
            candidate = parsed.path or src
            title = _pretty_from_route(candidate) if "." not in candidate else "iframe"

    attrs = [
        f'src="{src}"',
        f'width="{width}"',
        f'height="{height}"',
        'style="border:0;"',
        f'title="{title}"',
        f'loading="{loading}"',
    ]
    if allow:
        attrs.append(f'allow="{allow}"')
    iframe_html = f"<iframe {' '.join(attrs)}></iframe>"

    return f'<div style="display:flex; justify-content:center;">{iframe_html}</div>'
