from typing import Any, List, Dict, Optional, Union

from flet_core.control import Control
from flet_core.ref import Ref
from flet_core.types import (
    MaterialState
)

class ImageViewer(Control):
    """
    A ImageViewer displays a full screen Image that allows Zoom, Pan, and paging through multipe images.
    
    The image src can be a single image path String or a List of image strings to page through.
    Example:
    ```
    import flet as ft
    def main(page):
        def show_image_viewer_click(e):
            img = e.control.data
            page.dialog = ft.ImageViewer(src=img, swipe_dismissable=False)
            page.dialog.open = True
            page.update()
        images = ft.GridView(expand=1, runs_count=5)
        for i in range(0, 60):
            images.controls.append(
                ft.GestureDetector(
                    content=ft.Image(
                        src=f"https://picsum.photos/150/150?{i}",
                        fit=ft.ImageFit.NONE,
                    ),
                    data=f"https://picsum.photos/150/150?{i}",
                    on_tap=show_image_viewer_click,
                )
            )
        
        page.add(images)
    ft.app(target=main)
    ```
    -----
    Online docs: https://flet.dev/docs/controls/ImageViewer
    """

    def __init__(
        self,
        ref: Optional[Ref] = None,
        disabled: Optional[bool] = None,
        visible: Optional[bool] = None,
        data: Any = None,
        #
        # Specific
        #
        open: bool = False,
        src: Union[str, List[str]] = None,
        swipe_dismissible: Optional[bool] = True,
        double_tap_zoomable: Optional[bool] = True,
        background_color: Optional[str] = None,
        close_button_color: Optional[str] = None,
        close_button_tooltip: Optional[str] = "Close",
        immersive: Optional[bool] = True,
        initial_index: Optional[int] = 0,
    ):
        Control.__init__(
            self,
            ref=ref,
            disabled=disabled,
            visible=visible,
            data=data,
        )

        self.open = open
        self.src = src
        self.swipe_dismissible = swipe_dismissible
        self.double_tap_zoomable = double_tap_zoomable
        self.background_color = background_color
        self.close_button_color = close_button_color
        self.close_button_tooltip = close_button_tooltip
        self.immersive = immersive
        self.initial_index = initial_index

    def _get_control_name(self):
        return "imageviewer"

    def _before_build_command(self):
        super()._before_build_command()

    # open
    @property
    def open(self) -> Optional[bool]:
        return self._get_attr("open", data_type="bool", def_value=False)

    @open.setter
    def open(self, value: Optional[bool]):
        self._set_attr("open", value)

    # src
    @property
    def src(self) -> Union[str, List[str]]:
        img = self._get_attr("src")
        if "|" in img:
            img = img.split("|")
        return img

    @src.setter
    def src(self, value: Union[str, List[str]]):
        self.src = value
        img = value
        if isinstance(value, List):
            img = "|".join(value)
        self._set_attr("src", img)

    # swipe_dismissible
    @property
    def swipe_dismissible(self) -> Optional[bool]:
        return self._get_attr("swipeDismissible", data_type="bool", def_value=True)

    @swipe_dismissible.setter
    def swipe_dismissible(self, value: Optional[bool]):
        self._set_attr("swipeDismissible", value)

    # double_tap_zoomable
    @property
    def double_tap_zoomable(self) -> Optional[bool]:
        return self._get_attr("doubleTapZoomable", data_type="bool", def_value=True)

    @double_tap_zoomable.setter
    def double_tap_zoomable(self, value: Optional[bool]):
        self._set_attr("doubleTapZoomable", value)

    # close_button_color
    @property
    def background_color(self):
        return self._get_attr("backgroundColor")

    @background_color.setter
    def background_color(self, value):
        self._set_attr("backgroundColor", value)

    # close_button_color
    @property
    def close_button_color(self):
        return self._get_attr("closeButtonColor")

    @close_button_color.setter
    def close_button_color(self, value):
        self._set_attr("closeButtonColor", value)

    # close_button_tooltip
    @property
    def close_button_tooltip(self):
        return self._get_attr("closeButtonTooltip", def_value="Close")

    @close_button_tooltip.setter
    def close_button_tooltip(self, value):
        self._set_attr("closeButtonTooltip", value)

    # immersive
    @property
    def immersive(self) -> Optional[bool]:
        return self._get_attr("immersive", data_type="bool", def_value=True)

    @immersive.setter
    def immersive(self, value: Optional[bool]):
        self._set_attr("immersive", value)

    # initial_index
    @property
    def initial_index(self) -> Optional[int]:
        return self._get_attr("initialIndex", def_value=0)

    @initial_index.setter
    def divisions(self, value: Optional[int]):
        self._set_attr("initialIndex", value)