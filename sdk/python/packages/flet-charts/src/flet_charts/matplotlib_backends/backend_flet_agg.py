from matplotlib import _api
from matplotlib.backends import backend_webagg_core


class FigureCanvasFletAgg(backend_webagg_core.FigureCanvasWebAggCore):
    manager_class = _api.classproperty(lambda cls: FigureManagerFletAgg)
    supports_blit = False


class FigureManagerFletAgg(backend_webagg_core.FigureManagerWebAgg):
    _toolbar2_class = backend_webagg_core.NavigationToolbar2WebAgg


FigureCanvas = FigureCanvasFletAgg
FigureManager = FigureManagerFletAgg
interactive = True
