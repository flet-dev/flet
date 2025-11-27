from typing import Optional
from urllib.parse import urlparse


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
    base: str = "http://127.0.0.1:60222/",
    width: str = "100%",
    height: str = "480",
    title: Optional[str] = None,
    allow: Optional[str] = None,
    loading: str = "lazy",
) -> str:
    """
    Build an iframe HTML snippet.
    """
    if route:
        src = base.rstrip("/") + "/" + route.lstrip("/")
    if not src:
        raise ValueError("Either src or route must be provided")

    if title is None:
        parsed = urlparse(src)
        candidate = parsed.path or src
        if "." not in candidate:
            title = _pretty_from_route(route or candidate)
        else:
            title = "iframe"

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
    return f"<iframe {' '.join(attrs)}></iframe>"
