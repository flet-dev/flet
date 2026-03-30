from enum import Enum
from typing import Any, Optional

import flet as ft

@ft.control("{{cookiecutter.control_name}}")
class {{cookiecutter.control_name}}(ft.LayoutControl):
    """
    {{cookiecutter.control_name}} Control description.
    """

    value: str
