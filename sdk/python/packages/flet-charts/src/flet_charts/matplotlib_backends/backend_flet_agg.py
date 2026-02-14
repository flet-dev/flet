from matplotlib import _api
from matplotlib.backends import backend_webagg_core


class FigureCanvasFletAgg(backend_webagg_core.FigureCanvasWebAggCore):
    """Canvas implementation used to render Matplotlib figures in Flet."""

    manager_class = _api.classproperty(lambda cls: FigureManagerFletAgg)
    supports_blit = False


class FigureManagerFletAgg(backend_webagg_core.FigureManagerWebAgg):
    """Figure manager binding Matplotlib WebAgg tooling to Flet transport."""

    _toolbar2_class = backend_webagg_core.NavigationToolbar2WebAgg


FigureCanvas = FigureCanvasFletAgg
FigureManager = FigureManagerFletAgg
interactive = True
