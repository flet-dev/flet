import logging
from typing import Union

from flet.control import OptionalNumber
from flet.ref import Ref
from flet.stack import Stack


class UserControl(Stack):
    # def __init__(
    #     self,
    #     ref: Ref = None,
    #     width: OptionalNumber = None,
    #     height: OptionalNumber = None,
    #     expand: Union[bool, int] = None,
    #     opacity: OptionalNumber = None,
    #     visible: bool = None,
    #     disabled: bool = None,
    #     data: any = None,
    # ):
    #     Stack.__init__(
    #         self,
    #         ref=ref,
    #         width=width,
    #         height=height,
    #         expand=expand,
    #         opacity=opacity,
    #         visible=visible,
    #         disabled=disabled,
    #         data=data,
    #     )

    def did_mount(self):
        logging.debug(f"UserControl.did_mount(): {self.uid}")

    def will_unmount(self):
        logging.debug(f"UserControl.will_unmount(): {self.uid}")
