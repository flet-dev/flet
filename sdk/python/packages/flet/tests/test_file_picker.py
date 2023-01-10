import beartype.roar
import pytest

import flet as ft
from flet.protocol import Command


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
    assert r.file_type == ft.FilePickerFileType.VIDEO
    assert r._get_attr("fileType") == "video"

    r = ft.FilePicker()
    r.file_type = "any"
    assert isinstance(r.file_type, str)
    assert r._get_attr("fileType") == "any"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.FilePicker()
        r.file_type = "something"

    with pytest.raises(beartype.roar.BeartypeCallHintParamViolation):
        r = ft.FilePicker()
        r.file_type = 1
