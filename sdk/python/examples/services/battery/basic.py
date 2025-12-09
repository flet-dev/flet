import flet as ft


async def main(page: ft.Page):
    battery = ft.Battery()
    page.services.append(battery)  # need to keep a reference to the service

    info = ft.Text()
    state_text = ft.Text()

    async def refresh_info(_=None):
        level = await battery.get_battery_level()
        state = await battery.get_battery_state()
        save_mode = await battery.is_in_battery_save_mode()
        info.value = (
            f"Level: {level}% | State: {state} | "
            f"Battery saver: {'on' if save_mode else 'off'}"
        )

    async def on_state_change(e: ft.BatteryStateChangeEvent):
        state_text.value = f"State changed: {e.state}"
        await refresh_info()

    battery.on_state_change = on_state_change

    await refresh_info()

    page.add(
        ft.Column(
            [
                info,
                ft.Row(
                    [
                        ft.Button("Refresh battery info", on_click=refresh_info),
                    ]
                ),
                state_text,
            ],
        )
    )


ft.run(main)
