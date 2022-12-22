import pytest

import flet
from flet import Control, Text


@pytest.fixture
def page():
    return flet.page("test_update", no_window=True)


@pytest.fixture
def control_type_tree():
    def func(control: Control):
        if getattr(control, "controls", None):
            return {type(control): [func(child) for child in control.controls]}
        if type(control) is Text:
            return control.value
        return type(control)

    return func
