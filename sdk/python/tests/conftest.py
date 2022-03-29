import flet
import pytest
from flet import Control
from flet import Text


@pytest.fixture
def page():
    return flet.page("test_update", no_window=True)


@pytest.fixture
def control_type_tree():
    def func(control: Control):
        if getattr(control, "controls", None):
            return {type(control): [func(child) for child in control.controls]}
        elif type(control) is Text:
            return control.value
        else:
            return type(control)

    return func