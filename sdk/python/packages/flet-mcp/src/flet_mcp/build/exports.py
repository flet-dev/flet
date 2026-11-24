"""What each Flet module exports, introspected from the installed packages.

The Griffe reference (api.py) documents the API; this records exactly what code
can use, for tools that check app code against it: `ft.PieChart` (Flet has none:
it's `flet_charts.PieChart`), `ft.TextField(helper_text=...)` (the parameter is
`helper`) and `field.error_text = ...` (Flet keeps the attribute and shows
nothing) all fail only when that code runs.

Per module (`flet`, `flet.canvas`, `flet_charts`, ...), written to api.json under
`exports`:

- `names`: every public name, submodules included (`from flet import canvas`);
- `classes`: for each class, `params`, the keyword arguments it takes (`null`
  when it also takes `**kwargs`), and for dataclasses (every control) `attrs`,
  the public names that can be set beyond them: fields with `init=False` and
  settable properties;
- `enums`: the member names of each enum. `Icons` and `CupertinoIcons` are left
  out: api.json already lists their members under `enums`.
"""

from __future__ import annotations

import dataclasses
import enum
import importlib
import inspect
import logging
import pkgutil
from typing import Any

logger = logging.getLogger(__name__)

# Submodules apps use as namespaces of their own (`import flet.canvas as cv`).
NAMESPACE_MODULES = ["flet.canvas"]
_LARGE_ENUMS = {"Icons", "CupertinoIcons"}


def _params(cls: type) -> list[str] | None:
    try:
        sig = inspect.signature(cls)
    except (TypeError, ValueError):
        return None
    if any(p.kind is p.VAR_KEYWORD for p in sig.parameters.values()):
        return None
    return sorted(
        n
        for n, p in sig.parameters.items()
        if p.kind in (p.POSITIONAL_OR_KEYWORD, p.KEYWORD_ONLY)
    )


def _attrs(cls: type, params: list[str]) -> list[str]:
    fields = {f.name for f in dataclasses.fields(cls)}
    props = {
        n for n, v in inspect.getmembers(cls) if isinstance(v, property) and v.fset
    }
    return sorted(n for n in (fields | props) - set(params) if not n.startswith("_"))


def module_exports(module: Any) -> dict[str, Any]:
    """The `exports` entry of one imported module."""
    names = {n for n in dir(module) if not n.startswith("_")}
    if hasattr(module, "__path__"):
        names |= {
            m.name
            for m in pkgutil.iter_modules(module.__path__)
            if not m.name.startswith("_")
        }
    classes: dict[str, dict[str, Any]] = {}
    enums: dict[str, list[str]] = {}
    for name in sorted(names):
        obj = getattr(module, name, None)
        if not isinstance(obj, type):
            continue
        if issubclass(obj, enum.Enum):
            if name not in _LARGE_ENUMS:
                enums[name] = sorted(obj.__members__)
            continue
        params = _params(obj)
        entry: dict[str, Any] = {"params": params}
        if params is not None and dataclasses.is_dataclass(obj):
            entry["attrs"] = _attrs(obj, params)
        classes[name] = entry
    return {"names": sorted(names), "classes": classes, "enums": enums}


def build_exports(packages: list[str]) -> dict[str, dict[str, Any]]:
    """`exports` for `packages` and NAMESPACE_MODULES; a package that doesn't
    import is skipped with a warning, as Griffe's pass skips one."""
    out: dict[str, dict[str, Any]] = {}
    for name in [*packages, *NAMESPACE_MODULES]:
        try:
            module = importlib.import_module(name)
        except Exception as exc:
            logger.warning("Could not import %s for exports: %s", name, exc)
            continue
        out[name] = module_exports(module)
    return out
