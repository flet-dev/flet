from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number


@control("Image")
class Image(Shape):
    """
    Draws an image.
    """

    src: Optional[Union[str, bytes]] = None
    """
    Draws an image from a source.

    Accepts URLs/paths, base64 strings, or raw bytes.
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
