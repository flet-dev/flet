"""Loader for chart example apps used by integration tests.

Chart examples live as standalone apps in
`sdk/python/examples/extensions/charts/<chart>/<name>/main.py` (each with
its own pyproject.toml), so they are not importable as regular modules.
This helper loads an app's `main.py` by path and returns the module.
"""

import importlib.util
import sys
from pathlib import Path

_EXAMPLES_ROOT = (
    Path(__file__).resolve().parents[4] / "examples" / "extensions" / "charts"
)


def load_example(app_dir: str):
    """Load the `main.py` module of an example app.

    Args:
        app_dir: App directory relative to `examples/extensions/charts`,
            e.g. `"bar_chart/interactive_bar_chart"`.

    Returns:
        The loaded module; its `main` attribute is the app entry point.
    """
    main_py = _EXAMPLES_ROOT / app_dir / "main.py"
    module_name = "charts_example_" + app_dir.replace("/", "_")
    if module_name in sys.modules:
        return sys.modules[module_name]
    spec = importlib.util.spec_from_file_location(module_name, main_py)
    assert spec is not None and spec.loader is not None, f"Cannot load {main_py}"
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module
