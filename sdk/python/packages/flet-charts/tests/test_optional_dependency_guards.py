"""``import flet_charts`` survives an optional dependency that is present but broken.

matplotlib and plotly are optional: absent, they degrade to a ``ModuleNotFoundError``
raised only when the corresponding control is used. The guards used to catch
``ImportError`` alone, so a dependency that was *installed but unimportable* took the
whole package down instead.

That is not hypothetical. On Flet's Android runtime site-packages ship inside a zip,
and matplotlib reads ``mpl-data/matplotlibrc`` through a real ``__file__`` path — so
``import matplotlib`` raises ``NotADirectoryError``, and every app importing
``flet_charts`` crashed at startup, whether or not it ever drew a matplotlib chart.

Each case runs in a subprocess: the fault has to be injected before the first import
of the module under test, and ``@ft.control`` registration makes re-importing
``flet_charts`` in-process unsafe.
"""

import subprocess
import sys
import textwrap

# Meta-path finder that makes one top-level package raise a NON-ImportError at import
# time — the shape of the Android failure, reproduced without an Android device.
_FAULT = """
import sys
from importlib.abc import Loader, MetaPathFinder


class BrokenLoader(Loader):
    def create_module(self, spec):
        raise NotADirectoryError(
            20, "Not a directory", "/…/sitepackages.zip/{pkg}/some/bundled/data"
        )

    def exec_module(self, module):  # pragma: no cover - create_module raises first
        raise AssertionError("unreachable")


class BrokenFinder(MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname == "{pkg}" or fullname.startswith("{pkg}."):
            from importlib.machinery import ModuleSpec

            return ModuleSpec(fullname, BrokenLoader())
        return None


for _name in [n for n in sys.modules if n == "{pkg}" or n.startswith("{pkg}.")]:
    del sys.modules[_name]
sys.meta_path.insert(0, BrokenFinder())
"""


def _run(pkg: str, body: str) -> None:
    """Run ``body`` where importing ``pkg`` raises NotADirectoryError."""
    script = _FAULT.format(pkg=pkg) + textwrap.dedent(body)
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr


def test_import_survives_broken_matplotlib():
    """`import flet_charts` works when matplotlib is installed but fails to import."""
    _run(
        "matplotlib",
        """
        import flet_charts

        assert flet_charts.MatplotlibChart is not None
        assert flet_charts.LineChart is not None  # unrelated charts stay usable
        """,
    )


def test_matplotlib_chart_reports_the_underlying_failure():
    """Using MatplotlibChart raises ModuleNotFoundError chained to the real cause."""
    _run(
        "matplotlib",
        """
        import pytest
        from flet_charts.matplotlib_chart import _require_matplotlib

        with pytest.raises(ModuleNotFoundError) as excinfo:
            _require_matplotlib()

        assert isinstance(excinfo.value.__cause__, NotADirectoryError)
        assert "matplotlib" in str(excinfo.value)
        """,
    )


def test_matplotlib_chart_with_toolbar_reports_the_underlying_failure():
    """The toolbar variant guards the same way as the plain chart."""
    _run(
        "matplotlib",
        """
        import pytest
        from flet_charts.matplotlib_chart_with_toolbar import _require_matplotlib

        with pytest.raises(ModuleNotFoundError) as excinfo:
            _require_matplotlib()

        assert isinstance(excinfo.value.__cause__, NotADirectoryError)
        """,
    )


def test_import_survives_broken_plotly():
    """`import flet_charts` works when plotly is installed but fails to import."""
    _run(
        "plotly",
        """
        import pytest
        import flet_charts
        from flet_charts.plotly_chart import _PLOTLY_IMPORT_ERROR, _require_plotly

        assert flet_charts.PlotlyChart is not None
        # Only assert the guard fired if plotly is actually installed here;
        # when it is absent the import fails before the fault finder is reached.
        if _PLOTLY_IMPORT_ERROR is not None:
            with pytest.raises(ModuleNotFoundError):
                _require_plotly()
        """,
    )
