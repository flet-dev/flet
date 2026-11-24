"""Unit tests for ApiStore: docstring compaction, member drill-down,
query filtering, and the text rendering used by the default `get_api`
response. Uses a small synthetic api.json payload — no built data files."""

import pytest

from flet_mcp.api_store import (
    ApiStore,
    first_sentence,
    render_text,
)

LONG_DOC = (
    "Pushes a new navigation route to the browser history stack.\n"
    "Changing route will fire the on_route_change event.\n\n"
    "Example:\n    ```python\n    page.push_route('/settings')\n    ```"
)

RAW = {
    "controls": [
        {
            "name": "Page",
            "module": "flet.page",
            "package": "flet",
            "kind": "control",
            "summary": "High-level root control.",
            "bases": ["AdaptiveControl"],
            "properties": [
                {
                    "name": "bgcolor",
                    "type": "Optional[ColorValue]",
                    "default": "None",
                    "docstring": "Background color of the page. Uses theme otherwise.",
                },
                {
                    "name": "views",
                    "type": "list[View]",
                    "default": "field(default_factory=list)",
                    "docstring": "The list of views.",
                },
            ],
            "events": [
                {
                    "name": "on_route_change",
                    "type": "Optional[EventHandler[RouteChangeEvent[Page]]]",
                    "default": "None",
                    "docstring": "Called when page route changes.",
                },
                {
                    "name": "on_login",
                    "type": "SomethingExotic[Weird]",
                    "default": "None",
                    "docstring": "Called on login.",
                },
            ],
            "methods": [
                {
                    "name": "push_route",
                    "params": [{"name": "route"}, {"name": "kwargs"}],
                    "return_type": "None",
                    "async": True,
                    "docstring": LONG_DOC,
                },
            ],
        },
        {
            "name": "AdaptiveControl",
            "module": "flet.adaptive",
            "package": "flet",
            "kind": "control",
            "summary": "Base for adaptive controls.",
            "bases": [],
            "properties": [
                {
                    "name": "adaptive_border",
                    "type": "Optional[Border]",
                    "default": "None",
                    "docstring": "Platform-adaptive border.",
                }
            ],
        },
        {
            "name": "Text",
            "module": "flet.controls.core.text",
            "package": "flet",
            "kind": "control",
            "summary": "Display text with a single style.",
            "properties": [
                {
                    "name": "value",
                    "type": "str",
                    "default": "''",
                    "docstring": "The text displayed.",
                }
            ],
        },
        {
            "name": "Text",
            "module": "flet.controls.core.canvas.text",
            "package": "flet",
            "kind": "control",
            "summary": "Draws :attr:`value` with :attr:`style` at the given point.",
            "bases": ["Shape"],
            "properties": [
                {
                    "name": "style",
                    "type": "Optional[TextStyle]",
                    "default": "None",
                    "docstring": "The style to draw with. See :class:`TextStyle`.",
                }
            ],
        },
        {
            "name": "Audio",
            "module": "flet_audio",
            "package": "flet-audio",
            "kind": "service",
            "summary": "Plays audio.",
            "deprecated": {"reason": "Use AudioPlayer instead."},
            "properties": [
                {
                    "name": "volume",
                    "type": "float",
                    "default": "1.0",
                    "docstring": "Playback volume.",
                }
            ],
        },
    ],
    "events": [],
    "types": [
        {
            "name": "TextStyle",
            "module": "flet.types",
            "package": "flet",
            "docstring": "A style describing how to format text.",
            "fields": [
                {
                    "name": "size",
                    "type": "Optional[Number]",
                    "default": "None",
                    "docstring": "The size of glyphs. In logical pixels.",
                },
                {
                    "name": "weight",
                    "type": "Optional[FontWeight]",
                    "default": "None",
                    "docstring": "The typeface thickness.",
                },
                {
                    "name": "kind",
                    "type": "Optional[PointerDeviceType]",
                    "default": "field(default=None, metadata={'data_field': 'k'})",
                    "docstring": "Device kind.",
                },
            ],
        }
    ],
    "enums": [
        {
            "name": "TextAlign",
            "module": "flet.types",
            "package": "flet",
            "docstring": "Text alignment.",
            "members": [
                {
                    "name": "LEFT",
                    "value": "'left'",
                    "docstring": "Align left. More words here about it.",
                }
            ],
        },
        {
            "name": "Icons",
            "module": "flet.icons",
            "package": "flet",
            "kind": "large_enum",
            "members": [
                {"name": "BOOKMARK_REMOVE"},
                {"name": "BOOKMARK_REMOVE_OUTLINED"},
                {"name": "GROUP_REMOVE"},
                {"name": "REMOVE"},
                {"name": "REMOVE_CIRCLE"},
                {"name": "REMOVE_OUTLINED"},
                {"name": "REMOVE_ROUNDED"},
                {"name": "REMOVE_SHARP"},
            ],
        },
    ],
    "functions": [
        {
            "name": "run",
            "module": "flet",
            "package": "flet",
            "kind": "function",
            "summary": "Run the app.",
            "docstring": "Run the app.",
            "args": [{"name": "target", "type": "Callable", "default": ""}],
            "return_type": "None",
        },
        {
            "name": "use_state",
            "module": "flet.core.reactive",
            "package": "flet",
            "kind": "function",
            "summary": "Reactive state hook.",
            "docstring": "Reactive state hook.",
            "args": [{"name": "initial", "type": "T", "default": ""}],
            "return_type": "tuple[T, Callable]",
        },
    ],
}


@pytest.fixture
def store() -> ApiStore:
    s = ApiStore()
    s._raw = RAW
    s._controls = {c["name"]: c for c in RAW["controls"]}
    s._events = {e["name"]: e for e in RAW["events"]}
    s._types = {t["name"]: t for t in RAW["types"]}
    s._enums = {e["name"]: e for e in RAW["enums"]}
    s._functions = {f["name"]: f for f in RAW.get("functions", [])}
    s._by_name = {}
    for bucket in ("controls", "types", "events", "functions", "enums"):
        for e in RAW[bucket]:
            s._by_name.setdefault(e["name"], []).append((bucket, e))
    return s


# ---------- first_sentence ----------


def test_first_sentence_short_text_unchanged():
    assert first_sentence("Short doc.") == "Short doc."


def test_first_sentence_cuts_paragraphs_and_lines():
    assert first_sentence(LONG_DOC) == (
        "Pushes a new navigation route to the browser history stack."
    )


def test_first_sentence_caps_length():
    out = first_sentence("x" * 500)
    assert len(out) <= 160 and out.endswith("…")


# ---------- compaction + note ----------


def test_note_present_and_leading_when_trimmed(store):
    hit = store.get("Page")
    assert list(hit.keys())[0] == "note"
    assert "member=<name>" in hit["note"] and "query=<substring>" in hit["note"]
    method = hit["methods"][0]
    assert method["docstring"] == (
        "Pushes a new navigation route to the browser history stack."
    )


def test_no_note_when_nothing_trimmed(store):
    hit = store.get("Audio")
    assert "note" not in hit


# ---------- text rendering ----------


def test_render_text_grammar(store):
    text = render_text(store.get("Page"))
    assert text.startswith("Page (control) — High-level root control.")
    assert "bases: AdaptiveControl" in text
    assert "  bgcolor: ColorValue? — Background color of the page." in text
    assert "  views: list[View] = [] — The list of views." in text
    # Recognized handler unwrapped; unrecognized falls back to raw type.
    assert "  on_route_change(RouteChangeEvent) — " in text
    assert "  on_login: SomethingExotic[Weird] — Called on login." in text
    assert "  async push_route(route, kwargs) -> None — " in text
    # No package line for core flet.
    assert "package:" not in text


def test_render_text_deprecated_and_package(store):
    text = render_text(store.get("Audio"))
    assert "DEPRECATED: Use AudioPlayer instead." in text
    assert "package: flet-audio" in text


def test_render_text_type_fields(store):
    # Dataclass types keep members under "fields" — they must render,
    # compact, and drill down like control properties.
    text = render_text(store.get("TextStyle"))
    assert text.startswith("TextStyle (type)")
    assert "fields:" in text
    assert "  size: Number? — The size of glyphs." in text
    # field(default=None, metadata=...) is plumbing — no default shown.
    assert "  kind: PointerDeviceType? — Device kind." in text

    hit = store.get("TextStyle", member="weight")
    assert hit["member_kind"] == "field"
    assert hit["member"]["docstring"] == "The typeface thickness."

    hit = store.get("TextStyle", query="wei")
    assert [e["name"] for e in hit["fields"]] == ["weight"]


def test_render_text_enum(store):
    text = render_text(store.get("TextAlign"))
    assert text.startswith("TextAlign (enum)")
    assert "  LEFT = 'left' — Align left." in text


# ---------- member drill-down ----------


def test_member_full_docstring(store):
    hit = store.get("Page", member="push_route")
    assert hit["member_kind"] == "method"
    assert hit["member"]["docstring"] == LONG_DOC
    text = render_text(hit)
    assert text.startswith("Page.push_route (method)")
    assert "```python" in text  # full doc, untrimmed


def test_member_unknown_lists_available(store):
    hit = store.get("Page", member="nope")
    assert "error" in hit
    assert "bgcolor" in hit["available_members"]


# ---------- query filtering ----------


def test_query_filters_members(store):
    hit = store.get("Page", query="route")
    names = [e["name"] for e in hit["events"]] + [e["name"] for e in hit["methods"]]
    assert names == ["on_route_change", "push_route"]
    assert hit["properties"] == []
    assert "matching 'route'" in hit["note"]


def test_query_searches_inherited_members(store):
    # 'adaptive_border' lives on the base AdaptiveControl, not Page itself.
    hit = store.get("Page", query="adaptive_border")
    assert hit["properties"] == [] and hit["events"] == []
    block = hit["inherited"][0]
    assert block["from"] == "AdaptiveControl"
    assert block["properties"][0]["name"] == "adaptive_border"
    text = render_text(hit)
    assert "from AdaptiveControl:" in text
    assert "  adaptive_border: Border? — Platform-adaptive border." in text


def test_query_no_match_error_mentions_bases(store):
    hit = store.get("Page", query="zzz")
    assert "error" in hit and "bgcolor" in hit["available_members"]
    assert "AdaptiveControl" in hit["error"]


def test_member_wins_over_query(store):
    hit = store.get("Page", member="push_route", query="zzz")
    assert hit["member"]["name"] == "push_route"


def test_enum_member_and_query_resolve_inline(store):
    # get_api on an enum with query/member now searches members inline
    # instead of erroring (saves the caller a round-trip).
    hit = store.get("TextAlign", query="left")
    assert "error" not in hit
    assert hit["kind"] == "enum"
    assert [m["name"] for m in hit["members"]] == ["LEFT"]
    # member= is treated as the same member search.
    assert [m["name"] for m in store.get("TextAlign", member="LEFT")["members"]] == [
        "LEFT"
    ]
    # Works for large enums too, rendered as a member list.
    assert "REMOVE" in render_text(store.get("Icons", query="remove"))


def test_enum_query_no_match_notes_search(store):
    hit = store.get("TextAlign", query="zzz")
    assert "error" not in hit
    assert hit["members"] == []
    assert "search_enum_members" in hit["note"]


def test_function_lookup_and_render(store):
    hit = store.get("run")
    assert hit["kind"] == "function"
    text = render_text(hit)
    assert text.startswith("run (function) — Run the app.")
    assert "signature: run(target: Callable) -> None" in text


def test_hook_function_lookup(store):
    assert store.get("use_state")["kind"] == "function"


# ---------- enum member search ranking ----------


def test_enum_search_exact_first_variants_collapsed(store):
    out = store.search_enum_members("Icons", "remove", limit=5)
    # Exact match first, prefix matches next, substring last; the
    # _OUTLINED/_ROUNDED/_SHARP variants of REMOVE are collapsed.
    assert out == [
        "REMOVE",
        "REMOVE_CIRCLE",
        "GROUP_REMOVE",
        "BOOKMARK_REMOVE",
    ]


def test_enum_search_variant_kept_when_base_not_matching(store):
    # BOOKMARK_REMOVE_OUTLINED collapses because BOOKMARK_REMOVE matches;
    # querying the suffix itself still finds variants.
    out = store.search_enum_members("Icons", "outlined", limit=5)
    assert "BOOKMARK_REMOVE_OUTLINED" in out or "REMOVE_OUTLINED" in out


# ---------- name collisions ----------


def test_bare_name_prefers_non_canvas(store):
    hit = store.get("Text")
    assert hit["module"] == "flet.controls.core.text"
    # The response advertises the shadowed alternative + how to fetch it.
    assert "canvas.Text" in hit["note"]
    assert list(hit.keys())[0] == "note"


def test_qualified_name_reaches_canvas_shape(store):
    hit = store.get("canvas.Text")
    assert hit["module"] == "flet.controls.core.canvas.text"
    assert hit["bases"] == ["Shape"]


def test_qualified_name_with_no_match(store):
    assert store.get("nowhere.Text") is None


# ---------- RST role cleanup ----------


def test_rst_roles_stripped_in_render(store):
    text = render_text(store.get("canvas.Text"))
    assert "Draws `value` with `style` at the given point." in text
    assert ":attr:" not in text and ":class:" not in text
    assert "The style to draw with. See `TextStyle`." not in text  # trimmed
    assert "The style to draw with." in text


# ---------- json passthrough / misc ----------


def test_unknown_symbol_none(store):
    assert store.get("Nope") is None


def test_json_shape_keeps_raw_types(store):
    hit = store.get("Page")
    assert hit["events"][0]["type"] == (
        "Optional[EventHandler[RouteChangeEvent[Page]]]"
    )
