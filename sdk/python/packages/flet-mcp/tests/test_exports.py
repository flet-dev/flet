"""The `exports` section of api.json: built by introspecting the installed
packages (build/exports.py) and read through ApiStore."""

import pytest

import flet as ft
from flet_mcp.api_store import ApiStore, shared_api_store
from flet_mcp.build.exports import build_exports, module_exports


@pytest.fixture(scope="module")
def flet_exports() -> dict:
    return module_exports(ft)


def test_names_include_what_griffe_misses(flet_exports):
    """Refs, keys, `context`, hooks and submodules are all usable as `ft.X`."""
    names = set(flet_exports["names"])
    assert {"Ref", "ValueKey", "Observable", "context", "use_state", "canvas"} <= names
    assert "PieChart" not in names
    assert not any(n.startswith("_") for n in names)


def test_class_params_are_the_full_signature(flet_exports):
    """Inherited parameters included; `helper`, not `helper_text`."""
    params = set(flet_exports["classes"]["TextField"]["params"])
    assert {"label", "helper", "error", "expand", "width", "on_change"} <= params
    assert "helper_text" not in params
    assert "attrs" in flet_exports["classes"]["TextField"]


def test_enums(flet_exports):
    assert "BLACK_45" in flet_exports["enums"]["Colors"]
    assert "BLACK45" not in flet_exports["enums"]["Colors"]
    # Icons members are listed once, in api.json's `enums`.
    assert "Icons" not in flet_exports["enums"]


def test_build_exports_adds_namespaces_and_skips_what_fails(caplog):
    out = build_exports(["flet", "flet_no_such_package"])
    assert set(out) == {"flet", "flet.canvas"}
    assert "Line" in out["flet.canvas"]["names"]
    assert "flet_no_such_package" in caplog.text


RAW = {
    "enums": [
        {
            "name": "Icons",
            "package": "flet",
            "kind": "large_enum",
            "members": [{"name": "HOME", "value": "1"}, {"name": "ADD", "value": "2"}],
        }
    ],
    "exports": {
        "flet": {
            "names": ["Colors", "Icons", "Ref", "TextField", "Tooltip", "canvas"],
            "classes": {
                "TextField": {
                    "params": ["error", "helper", "label"],
                    "attrs": ["page_id"],
                },
                "Tooltip": {"params": None},
                "Ref": {"params": []},
            },
            "enums": {"Colors": ["BLACK_45", "PRIMARY"]},
        },
        "flet_charts": {"names": ["PieChart"], "classes": {}, "enums": {}},
    },
}


def _store(raw: dict) -> ApiStore:
    s = ApiStore()
    s._raw = raw
    s._enums = {e["name"]: e for e in raw.get("enums", [])}
    return s


def test_store_reads_exports():
    s = _store(RAW)
    assert s.export_modules() == ["flet", "flet_charts"]
    assert "Ref" in s.module_exports("flet")
    assert s.modules_exporting("PieChart") == ["flet_charts"]
    assert s.init_params("flet", "TextField") == {"error", "helper", "label"}
    assert s.init_params("flet", "Tooltip") is None  # takes **kwargs
    assert s.settable_attrs("flet", "TextField") == {
        "error",
        "helper",
        "label",
        "page_id",
    }
    assert s.settable_attrs("flet", "Ref") is None  # not a dataclass
    assert s.module_enum_members("flet", "Colors") == {"BLACK_45", "PRIMARY"}
    assert s.module_enum_members("flet", "Icons") == {"HOME", "ADD"}
    assert s.module_enum_members("flet", "TextField") is None


def test_store_without_exports_says_nothing():
    """api.json from before exports were recorded: every answer is None, so a
    checker stays quiet instead of flagging valid code."""
    s = _store({"enums": RAW["enums"]})
    assert s.export_modules() == []
    assert s.module_exports("flet") is None
    assert s.modules_exporting("PieChart") == []
    assert s.init_params("flet", "TextField") is None
    assert s.settable_attrs("flet", "TextField") is None
    assert s.module_enum_members("flet", "Colors") is None


def test_shared_store_is_the_servers():
    """Code in the MCP server's process reads the store the server loaded."""
    from flet_mcp.server import _get_api_store

    assert shared_api_store() is shared_api_store() is _get_api_store()


def test_lucide_icons_are_a_module_enum():
    """Injected icon sets belong to the module their entry names: LucideIcons to
    flet_shadcn_ui, though its package is spelled flet-shadcn-ui."""
    raw = {
        "enums": [
            *RAW["enums"],
            {
                "name": "LucideIcons",
                "module": "flet_shadcn_ui.lucide_icons",
                "package": "flet-shadcn-ui",
                "kind": "large_enum",
                "members": [{"name": "HOUSE", "value": "1"}],
            },
        ],
        "exports": {
            **RAW["exports"],
            "flet_shadcn_ui": {"names": ["LucideIcons"], "classes": {}, "enums": {}},
        },
    }
    s = _store(raw)
    assert s.module_enum_members("flet_shadcn_ui", "LucideIcons") == {"HOUSE"}
    assert s.module_enum_members("flet", "LucideIcons") is None
    assert 'find_icon(family="lucide")' in s.get_enum("LucideIcons")["note"]
