from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber, OptionalString


@control("Image")
class Image(Shape):
    """
    Draws an image.
    """

    src: OptionalString = None
    """
    Draws an image from a source.

    This could be an external URL or a local
    [asset file](https://flet.dev/docs/cookbook/assets).
    """

    src_bytes: Optional[bytes] = None
    """
    Draws an image from a bytes array.
    """

    x: OptionalNumber = None
    """
    The x-axis coordinate of the image's top-left corner.
    """

    y: OptionalNumber = None
    """
    The y-axis coordinate of the image's top-left corner.
    """

    width: OptionalNumber = None
    """
    The width of the rectangle to draw the image into. Use image width if None.
    """

    height: OptionalNumber = None
    """
    The height of the rectangle to draw the image into. Use image height if None.
    """

    paint: Optional[Paint] = None
    """
    A paint to composite the image into canvas. The value of this property
    is the instance of [`Paint`](https://flet.dev/docs/reference/types/paint) class.
    """
