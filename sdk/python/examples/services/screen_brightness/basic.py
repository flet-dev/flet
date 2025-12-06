import flet as ft


async def main(page: ft.Page):
    sb = ft.ScreenBrightness()
    page.services.append(sb)

    info = ft.Text()
    system_change = ft.Text()
    app_change = ft.Text()

    level = ft.Slider(min=0, max=1, divisions=20, value=0.5, label="Brightness")
    animate_switch = ft.Switch(
        label="Animate application changes", value=True, on_change=None
    )
    auto_reset_switch = ft.Switch(
        label="Auto-reset application brightness on lifecycle changes",
        value=True,
        on_change=None,
    )

    async def refresh_info():
        system_brightness = await sb.get_system_screen_brightness()
        app_brightness = await sb.get_application_screen_brightness()
        can_change_system = await sb.can_change_system_screen_brightness()

        animate_switch.value = await sb.is_animate()
        auto_reset_switch.value = await sb.is_auto_reset()

        info.value = (
            f"System: {system_brightness:.2f} | "
            f"Application: {app_brightness:.2f} | "
            f"Can change system: {can_change_system}"
        )

    async def set_application_brightness(_):
        await sb.set_application_screen_brightness(level.value)
        await refresh_info()

    async def set_system_brightness(_):
        await sb.set_system_screen_brightness(level.value)
        await refresh_info()

    async def reset_application_brightness(_):
        await sb.reset_application_screen_brightness()
        await refresh_info()

    async def toggle_animate(e: ft.Event[ft.Switch]):
        await sb.set_animate(e.control.value)
        await refresh_info()

    async def toggle_auto_reset(e: ft.Event[ft.Switch]):
        await sb.set_auto_reset(e.control.value)
        await refresh_info()

    async def on_system_change(e: ft.ScreenBrightnessChangeEvent):
        system_change.value = f"System brightness changed: {e.brightness:.2f}"

    async def on_application_change(e: ft.ScreenBrightnessChangeEvent):
        app_change.value = f"Application brightness changed: {e.brightness:.2f}"

    sb.on_system_screen_brightness_change = on_system_change
    sb.on_application_screen_brightness_change = on_application_change

    await refresh_info()

    animate_switch.on_change = toggle_animate
    auto_reset_switch.on_change = toggle_auto_reset

    page.add(
        ft.Column(
            [
                info,
                level,
                ft.Row(
                    [
                        ft.Button(
                            "Set application", on_click=set_application_brightness
                        ),
                        ft.Button("Set system", on_click=set_system_brightness),
                        ft.TextButton(
                            "Reset application", on_click=reset_application_brightness
                        ),
                    ],
                    wrap=True,
                ),
                animate_switch,
                auto_reset_switch,
                ft.Divider(),
                system_change,
                app_change,
            ],
            spacing=12,
        )
    )


ft.run(main)
