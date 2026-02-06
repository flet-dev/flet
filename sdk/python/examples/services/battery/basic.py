import flet as ft


async def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    async def refresh_info(e: ft.Event[ft.Button] = None):
        level = await battery.get_battery_level()
        state = await battery.get_battery_state()
        save_mode = await battery.is_in_battery_save_mode()
        info.value = (
            f"Battery level: {level}% \n"
            f"Battery state: {state.name} \n"
            f"Battery saver: {'ON' if save_mode else 'OFF'}"
        )

    async def on_state_change(e: ft.BatteryStateChangeEvent):
        print(f"State changed: {e.state}")
        await refresh_info()

    battery = ft.Battery(on_state_change=on_state_change)
    page.services.append(battery)  # need to keep a reference to the service

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    info := ft.Text(),
                    ft.Button("Refresh battery info", on_click=refresh_info),
                ],
            )
        )
    )
    await refresh_info()


ft.run(main)
