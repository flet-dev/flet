from typing import Optional

from flet.controls.base_control import control
from flet.controls.duration import DurationValue
from flet.controls.keys import KeyValue
from flet.controls.services.service import Service
from flet.controls.types import IconData
from flet.testing.finder import Finder
from flet.controls.transform import Offset


__all__ = ["Tester"]


@control("Tester")
class Tester(Service):
    """
    Class that programmatically interacts with page controls and the test environment.
    """

    async def pump(self, duration: Optional[DurationValue] = None):
        """
        Triggers a frame after duration amount of time.

        Args:
            duration: A duration after which to trigger a frame.
        """
        return await self._invoke_method("pump", {"duration": duration})

    async def pump_and_settle(self, duration: Optional[DurationValue] = None):
        """
        Repeatedly calls pump until there are no longer any frames scheduled.
        This will call `pump` at least once, even if no frames are scheduled when
        the function is called, to flush any pending microtasks which may
        themselves schedule a frame.

        This essentially waits for all animations to have completed.

        Args:
            duration: A duration after which to trigger a frame.
        """
        return await self._invoke_method("pump_and_settle", {"duration": duration})

    async def find_by_text(self, text: str) -> Finder:
        """
        Finds controls containing string equal to the `text` argument.

        Args:
            text: The exact text value to search control by.
        """
        finder = await self._invoke_method("find_by_text", {"text": text})
        return Finder(**finder)

    async def find_by_text_containing(self, pattern: str) -> Finder:
        """
        Finds controls containing specified text pattern.

        Args:
            pattern: Regular expression pattern.
        """
        finder = await self._invoke_method(
            "find_by_text_containing", {"pattern": pattern}
        )
        return Finder(**finder)

    async def find_by_key(self, key: KeyValue) -> Finder:
        """
        Finds controls by a [Key][flet.Key] instance or key name.

        Args:
            key: A key instance or its name.
        """
        finder = await self._invoke_method("find_by_key", {"key": key})
        return Finder(**finder)

    async def find_by_tooltip(self, value: str) -> Finder:
        """
        Finds controls by a tooltip.

        Args:
            value: Tooltip value.
        """
        finder = await self._invoke_method("find_by_tooltip", {"value": value})
        return Finder(**finder)

    async def find_by_icon(self, icon: IconData) -> Finder:
        """
        Finds controls by an icon.

        Args:
            icon: The Icon to search by.
        """
        finder = await self._invoke_method("find_by_icon", {"icon": icon})
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
        return await self._invoke_method("take_screenshot", {"name": name})

    async def tap(self, finder: Finder):
        """
        Dispatch a pointer down / pointer up sequence at the center
        of the given control, assuming it is exposed.

        Args:
            finder: Finder to search for a control.
        """
        await self._invoke_method(
            "tap", {"finder_id": finder.id, "finder_index": finder.index}
        )

    async def tap_at(self, offset: Offset):
        """
        Dispatch a pointer down / pointer up sequence at the given offset.

        Args:
            offset: Offset value at which tap will occur.
        """
        await self._invoke_method("tap_at", {"offset": offset})

    async def long_press(self, finder: Finder):
        """
        Dispatch a pointer down / pointer up sequence (with a delay of
        600 ms between the two events) at the center of the given control,
        assuming it is exposed.

        Args:
            finder: Finder to search for a control.
        """
        await self._invoke_method(
            "long_press", {"finder_id": finder.id, "finder_index": finder.index}
        )

    async def enter_text(self, finder: Finder, text: str):
        """
        Give the text input control specified by `finder` the focus and
        replace its content with `text`, as if it had been provided by
        the onscreen keyboard.

        Args:
            finder: Finder to search for a control.
            text: The text to enter.
        """
        await self._invoke_method(
            "enter_text",
            {"finder_id": finder.id, "finder_index": finder.index, "text": text},
        )

    async def mouse_hover(self, finder: Finder):
        """
        Dispatch a pointer hover event at the center of the given control.

        Args:
            finder: Finder to search for a control.
        """
        await self._invoke_method(
            "mouse_hover", {"finder_id": finder.id, "finder_index": finder.index}
        )

    async def teardown(self):
        """
        Teardown Flutter integration test and exit Flutter process.
        """
        await self._invoke_method("teardown")
