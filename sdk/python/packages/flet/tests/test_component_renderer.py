import pytest

from flet.components.component import Renderer
from flet.components.utils import current_renderer


def test_renderer_with_context_binds_and_resets_current_renderer():
    renderer = Renderer()

    with pytest.raises(RuntimeError):
        current_renderer()

    with renderer.with_context():
        assert current_renderer() is renderer

    with pytest.raises(RuntimeError):
        current_renderer()


def test_renderer_with_context_reuses_context_manager_type():
    renderer = Renderer()

    ctx1 = renderer.with_context()
    ctx2 = renderer.with_context()

    assert type(ctx1) is type(ctx2)
