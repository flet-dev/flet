from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number


@control("Image")
class Image(Shape):
    """
    Draws an image.
    """

    src: Optional[str] = None
    """
    Draws an image from a source.

    This could be an external URL or a local
    [asset file](https://flet.dev/docs/cookbook/assets).
    """

    src_bytes: Optional[bytes] = None
    """
    Draws an image from a bytes array.
    """

    x: Optional[Number] = None
    """
    The x-axis coordinate of the image's top-left corner.
    """

    y: Optional[Number] = None
    """
    The y-axis coordinate of the image's top-left corner.
    """

    width: Optional[Number] = None
    """
    The width of the rectangle to draw the image into. Use image width if None.
    """

    height: Optional[Number] = None
    """
    The height of the rectangle to draw the image into. Use image height if None.
    """

    paint: Optional[Paint] = None
    """
    A paint to composite the image into canvas.
    """
