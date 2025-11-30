import flet as ft
import flet_audio as fta


def main(page: ft.Page):
    url = "https://luan.xyz/files/audio/ambient_c_motion.mp3"

    def log(message: str):
        page.show_dialog(ft.SnackBar(content=message))
        print(message)

    async def play():
        await audio.play()

    async def pause():
        await audio.pause()

    async def resume():
        await audio.resume()

    async def release():
        await audio.release()

    def set_volume(value: float):
        audio.volume += value
        log(f"Volume: {audio.volume}")

    def set_balance(value: float):
        audio.balance += value

    async def seek_2s():
        await audio.seek(ft.Duration(seconds=2))

    async def get_duration():
        duration = await audio.get_duration()
        log(f"Duration: {duration}")

    async def on_get_current_position():
        position = await audio.get_current_position()
        log(f"Current position: {position}")

    audio = fta.Audio(
        src=url,
        autoplay=False,
        volume=1,
        balance=0,
        on_loaded=lambda _: log("Loaded"),
        on_duration_change=lambda e: print(f"Duration changed: {e.duration}"),
        on_position_change=lambda e: print(f"Position changed: {e.position}"),
        on_state_change=lambda e: log(f"State changed: {e.state}"),
        on_seek_complete=lambda _: log("Seek complete"),
    )

    page.add(
        ft.Button("Play", on_click=play),
        ft.Button("Pause", on_click=pause),
        ft.Button("Resume", on_click=resume),
        ft.Button("Release", on_click=release),
        ft.Button("Seek 2s", on_click=seek_2s),
        ft.Row(
            controls=[
                ft.Button("Volume down", on_click=lambda _: set_volume(-0.1)),
                ft.Button("Volume up", on_click=lambda _: set_volume(0.1)),
            ]
        ),
        ft.Row(
            controls=[
                ft.Button("Balance left", on_click=lambda _: set_balance(-0.1)),
                ft.Button("Balance right", on_click=lambda _: set_balance(0.1)),
            ]
        ),
        ft.Button("Get duration", on_click=get_duration),
        ft.Button("Get current position", on_click=on_get_current_position),
    )


if __name__ == "__main__":
    ft.run(main)
