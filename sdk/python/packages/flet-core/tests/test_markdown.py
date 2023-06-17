import flet_core as ft
import pytest
from flet_core.protocol import Command


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
    assert isinstance(r.extension_set, ft.MarkdownExtensionSet)
    assert r.extension_set == ft.MarkdownExtensionSet.NONE
    assert r._get_attr("extensionSet") is None

    r = ft.Markdown(extension_set=ft.MarkdownExtensionSet.COMMON_MARK)
    assert isinstance(r.extension_set, ft.MarkdownExtensionSet)
    assert isinstance(r._get_attr('extensionSet'), str)
    assert r.extension_set == ft.MarkdownExtensionSet.COMMON_MARK
    assert r._get_attr("extensionSet") == ft.MarkdownExtensionSet.COMMON_MARK.value
    assert r._get_attr("extensionSet") == "commonMark"

    r = ft.Markdown(extension_set="gitHubWeb")
    assert isinstance(r.extension_set, ft.MarkdownExtensionSet)
    assert isinstance(r._get_attr('extensionSet'), str)
    assert r._get_attr("extensionSet") == ft.MarkdownExtensionSet.GITHUB_WEB.value
    assert r._get_attr("extensionSet") == "gitHubWeb"
