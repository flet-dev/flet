import flet as ft
import flet_audio as fta

# https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3
# https://luan.xyz/files/audio/ambient_c_motion.mp3
# https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true


@ft.component
def App():
    duration, set_duration = ft.use_state(0.0)
    position, set_position = ft.use_state(0.0)

    audio, _ = ft.use_state(
        lambda: fta.Audio(
            src="https://luan.xyz/files/audio/ambient_c_motion.mp3",
            autoplay=False,
            on_duration_change=lambda e: set_duration(e.duration.in_milliseconds),
            on_position_change=lambda e: set_position(e.position),
        )
    )

    print("duration:", duration)
    print("position:", position)

    async def play():
        await audio.play()

    async def pause():
        await audio.pause()

    async def resume():
        await audio.resume()

    return [
        ft.ProgressBar(position / duration if duration > 0 else 0),
        ft.Button("Play", disabled=duration == 0, on_click=play),
        ft.Button("Pause", disabled=duration == 0, on_click=pause),
        ft.Button("Resume", disabled=duration == 0, on_click=resume),
    ]


ft.run(lambda page: page.render(App))
