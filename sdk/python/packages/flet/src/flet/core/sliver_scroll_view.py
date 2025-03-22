from typing import Any, List, Optional

from flet.core.adaptive_control import AdaptiveControl
from flet.core.control import Control
from flet.core.ref import Ref
from flet.core.sliver import Sliver
from flet.core.types import ClipBehavior, OptionalNumber


class SliverScrollView(AdaptiveControl, Sliver):
    """
    A scroll view that creates custom scroll effects using slivers.

    -----

    Online docs: https://flet.dev/docs/controls/sliverscrollview
    """

    def __init__(
        self,
        slivers: List[Sliver],
        clip_behavior: Optional[ClipBehavior] = None,
        reverse: Optional[bool] = None,
        horizontal: Optional[bool] = None,
        shrink_wrap: Optional[bool] = None,
        semantic_child_count: Optional[int] = None,
        anchor: OptionalNumber = None,
        primary: Optional[bool] = None,
        cache_extent: OptionalNumber = None,
        #
        # AdaptiveControl
        #
        ref: Optional[Ref] = None,
        visible: Optional[bool] = None,
        disabled: Optional[bool] = None,
        data: Any = None,
        rtl: Optional[bool] = None,
        adaptive: Optional[bool] = None,
        expand: Optional[bool] = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            visible=visible,
            disabled=disabled,
            data=data,
            rtl=rtl,
            expand=expand,
        )

        AdaptiveControl.__init__(self, adaptive=adaptive)

        self.slivers = slivers
        self.clip_behavior = clip_behavior
        self.reverse = reverse
        self.horizontal = horizontal
        self.shrink_wrap = shrink_wrap
        self.semantic_child_count = semantic_child_count
        self.anchor = anchor
        self.primary = primary
        self.cache_extent = cache_extent

    def _get_control_name(self):
        return "sliverscrollview"

    def _get_children(self):
        return self.__slivers

    # slivers
    @property
    def slivers(self) -> List[Control]:
        return self.__slivers

    @slivers.setter
    def slivers(self, value: List[Control]):
        self.__slivers = value

    # clip_behavior
    @property
    def clip_behavior(self) -> Optional[ClipBehavior]:
        return self.__clip_behavior

    @clip_behavior.setter
    def clip_behavior(self, value: Optional[ClipBehavior]):
        self.__clip_behavior = value
        self._set_enum_attr("clipBehavior", value, ClipBehavior)

    # reverse
    @property
    def reverse(self) -> Optional[bool]:
        return self._get_attr("reverse", data_type="bool", def_value=False)

    @reverse.setter
    def reverse(self, value: Optional[bool]):
        self._set_attr("reverse", value)

    # horizontal
    @property
    def horizontal(self) -> Optional[bool]:
        return self._get_attr("horizontal", data_type="bool", def_value=False)

    @horizontal.setter
    def horizontal(self, value: Optional[bool]):
        self._set_attr("horizontal", value)

    # shrink_wrap
    @property
    def shrink_wrap(self) -> Optional[bool]:
        return self._get_attr("shrinkWrap", data_type="bool", def_value=False)

    @shrink_wrap.setter
    def shrink_wrap(self, value: Optional[bool]):
        self._set_attr("shrinkWrap", value)

    # semantic_child_count
    @property
    def semantic_child_count(self) -> Optional[int]:
        return self._get_attr("semanticChildCount", data_type="int")

    @semantic_child_count.setter
    def semantic_child_count(self, value: Optional[int]):
        self._set_attr("semanticChildCount", value)

    # anchor
    @property
    def anchor(self) -> OptionalNumber:
        return self._get_attr("anchor", data_type="float", def_value=0.0)

    @anchor.setter
    def anchor(self, value: OptionalNumber):
        self._set_attr("anchor", value)

    # primary
    @property
    def primary(self) -> Optional[bool]:
        return self._get_attr("primary", data_type="bool", def_value=False)

    @primary.setter
    def primary(self, value: Optional[bool]):
        self._set_attr("primary", value)

    # cache_extent
    @property
    def cache_extent(self) -> OptionalNumber:
        return self._get_attr("cacheExtent", data_type="float")

    @cache_extent.setter
    def cache_extent(self, value: OptionalNumber):
        self._set_attr("cacheExtent", value)
