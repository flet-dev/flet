import flet_core as ft
import pytest
from flet_core.protocol import Command


def test_instance_no_attrs_set():
    r = ft.FilePicker()
    assert isinstance(r, ft.Control)
    assert r._build_add_commands() == [
        Command(
            indent=0,
            name=None,
            values=["filepicker"],
            attrs={"upload": "[]"},
            commands=[],
        )
    ], "Test failed"


def test_file_type_enum():
    r = ft.FilePicker()
    r.file_type = ft.FilePickerFileType.VIDEO
    assert isinstance(r.file_type, ft.FilePickerFileType)
    assert isinstance(r._get_attr('fileType'), str)
    assert r.file_type == ft.FilePickerFileType.VIDEO
    assert r._get_attr('fileType') == ft.FilePickerFileType.VIDEO.value
    assert r._get_attr("fileType") == "video"

    r = ft.FilePicker()
    assert isinstance(r.file_type, ft.FilePickerFileType)
    assert isinstance(r._get_attr('fileType'), str)
    assert r.file_type == ft.FilePickerFileType.ANY
    assert r._get_attr('fileType') == ft.FilePickerFileType.ANY.value
    assert r._get_attr("fileType") == "any"
