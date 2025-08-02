from typing import Optional

from flet.controls.base_control import control
from flet.controls.duration import Duration
from flet.controls.keys import KeyValue
from flet.controls.services.service import Service
from flet.controls.types import IconValue
from flet.testing.finder import Finder

__all__ = ["Tester"]


@control("Tester")
class Tester(Service):
    """
    Class that programmatically interacts with page controls and the test environment.
    """

    async def pump(self, duration: Optional[Duration] = None):
        """
        Triggers a frame after duration amount of time.

        Args:
            duration: A duration after which to trigger a frame.
        """
        return await self._invoke_method_async("pump", {"duration": duration})

    async def pump_and_settle(self):
        """
        Repeatedly calls pump until there are no longer any frames scheduled.
        This will call `pump` at least once, even if no frames are scheduled when
        the function is called, to flush any pending microtasks which may
        themselves schedule a frame.

        This essentially waits for all animations to have completed.
        """
        return await self._invoke_method_async("pump_and_settle")

    async def find_by_text(self, text: str) -> Finder:
        """
        Finds controls containing string equal to the `text` argument.

        Args:
            text: The exact text value to search control by.
        """
        finder = await self._invoke_method_async("find_by_text", {"text": text})
        return Finder(**finder)

    async def find_by_text_containing(self, pattern: str) -> Finder:
        """
        Finds controls containing specified text pattern.

        Args:
            pattern: Regular expression pattern.
        """
        finder = await self._invoke_method_async(
            "find_by_text_containing", {"pattern": pattern}
        )
        return Finder(**finder)

    async def find_by_key(self, key: KeyValue) -> Finder:
        """
        Finds controls by a [Key][flet.Key] instance or key name.

        Args:
            key: A key instance or its name.
        """
        finder = await self._invoke_method_async("find_by_key", {"key": key})
        return Finder(**finder)

    async def find_by_tooltip(self, value: str) -> Finder:
        """
        Finds controls by a tooltip.

        Args:
            value: Tooltip value.
        """
        finder = await self._invoke_method_async("find_by_tooltip", {"value": value})
        return Finder(**finder)

    async def find_by_icon(self, icon: IconValue) -> Finder:
        """
        Finds controls by an icon.

        Args:
            icon: The Icon to search by.
        """
        finder = await self._invoke_method_async("find_by_icon", {"icon": icon})
        return Finder(**finder)

    async def take_screenshot(self, name: str) -> bytes:
        """
        Takes a screenshot of the entire application window.
        This method works when testing on iOS and Android only.

        Args:
            name: The name of the screenshot.

        Returns:
            Screenshot in PNG format.
        """
        return await self._invoke_method_async("take_screenshot", {"name": name})

    async def tap(self, finder: Finder):
        """
        Dispatch a pointer down / pointer up sequence at the center
        of the given control, assuming it is exposed.

        Args:
            finder: Finder to search for a control.
        """
        await self._invoke_method_async("tap", {"id": finder.id})

    async def enter_text(self, finder: Finder, text: str):
        """
        Give the text input control specified by `finder` the focus and
        replace its content with `text`, as if it had been provided by
        the onscreen keyboard.

        Args:
            finder: Finder to search for a control.
            text: The text to enter.
        """
        await self._invoke_method_async("enter_text", {"id": finder.id, "text": text})

    async def mouse_hover(self, finder: Finder):
        """
        Dispatch a pointer hover event at the center of the given control.

        Args:
            finder: Finder to search for a control.
        """
        await self._invoke_method_async("mouse_hover", {"id": finder.id})

    def teardown(self):
        """
        Teardown Flutter integration test and exit Flutter process.
        """
        return self._invoke_method_async("teardown")
