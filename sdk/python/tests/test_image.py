import flet
from flet import Image
from flet.protocol import Command


def test_image_add():
    i = Image(
        src="https://www.w3schools.com/css/img_5terre.jpg",
        alt="This is image",
        title="This is title",
        maximize_frame=False,
    )
    assert isinstance(i, flet.Control)
    assert isinstance(i, flet.Image)
    assert i.get_cmd_str() == [
        Command(
            indent=0,
            name=None,
            values=["image"],
            attrs={
                "alt": "This is image",
                "maximizeframe": "false",
                "src": "https://www.w3schools.com/css/img_5terre.jpg",
                "title": "This is title",
            },
            lines=[],
            commands=[],
        )
    ], "Test failed"
