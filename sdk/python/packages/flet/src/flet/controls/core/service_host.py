from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.services.service import Service

__all__ = ["ServiceHost"]


@control("ServiceHost")
class ServiceHost(Control):
    """
    Hosts services and makes them available to children.

    Example:

    ```python
    async def main(page: ft.Page):
        async def pick_files():
            await file_picker.pick_files()

        page.add(
            ft.ServiceHost(
                services=[file_picker := ft.FilePicker()],
                content=ft.Column([ft.Button("Pick files", on_click=pick_files)]),
            )
        )


    ft.run(main)
    ```
    """

    services: list[Service] = field(default_factory=list)
    """
    List of services hosted by this ServiceHost.
    """

    content: Optional[Control] = None
    """
    Child content.
    """
