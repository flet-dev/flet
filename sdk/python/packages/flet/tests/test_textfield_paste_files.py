import flet as ft
from flet.controls.base_control import get_event_field_type
from flet.utils.from_dict import from_dict


def test_paste_files_event_decodes_the_client_payload():
    field = ft.TextField(on_paste_files=lambda e: None)
    event_type = get_event_field_type(field, "on_paste_files")
    assert event_type is ft.TextFieldPasteFilesEvent

    png = b"\x89PNG\r\n\x1a\n"
    e = from_dict(
        event_type,
        {
            "control": field,
            "name": "paste_files",
            "files": [
                {"name": "image.png", "mime_type": "image/png", "bytes": png},
                {"name": "notes.txt", "mime_type": "", "bytes": b"hi"},
            ],
        },
    )

    assert e.files == [
        ft.PastedFile(name="image.png", mime_type="image/png", bytes=png),
        ft.PastedFile(name="notes.txt", mime_type="", bytes=b"hi"),
    ]
