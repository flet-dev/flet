import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


def test_instance_no_attrs_set():
    r = ft.Markdown()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["markdown"],
            attrs={},
            commands=[],
        )
    ], "Test failed"


def test_extension_set_enum():
    r = ft.Markdown()
    assert r.extension_set is None
    assert r._get_attr("extensionSet") is None

    r = ft.Markdown(extension_set=ft.MarkdownExtensionSet.COMMON_MARK)
    assert isinstance(r.extension_set, ft.MarkdownExtensionSet)
    assert r.extension_set == ft.MarkdownExtensionSet.COMMON_MARK
    assert r._get_attr("extensionSet") == "commonMark"

    r = ft.Markdown(extension_set="none")
    assert isinstance(r.extension_set, str)
    assert r._get_attr("extensionSet") == "none"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Markdown(extension_set="something")

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.Markdown(extension_set=1)
