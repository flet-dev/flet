import time

import flet as ft


def example(page):
    import flet.canvas as cv

    url = "https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true"

    def convertMillis(millis):
        seconds = int(millis / 1000) % 60
        if seconds < 10:
            seconds_str = f"0{seconds}"
        else:
            seconds_str = f"{seconds}"
        minutes = int(millis / (1000 * 60)) % 60
        return f"{minutes}:{seconds_str}"

    class VolumeSlider(ft.GestureDetector):
        def __init__(self, audio, on_change_volume):
            super().__init__()
            self.visible = False
            self.audio = audio
            self.previous_volume = 1
            self.content = ft.Container(
                width=100,
                height=5,
                content=cv.Canvas(
                    shapes=[
                        cv.Rect(
                            x=0,
                            y=0,
                            height=4,
                            border_radius=3,
                            paint=ft.Paint(color=ft.Colors.GREY_500),
                            width=100,
                        ),
                        cv.Rect(
                            x=0,
                            y=0,
                            height=4,
                            border_radius=3,
                            paint=ft.Paint(color=ft.Colors.GREY_900),
                            width=100,
                        ),
                        cv.Circle(
                            x=100,
                            y=2,
                            radius=6,
                            paint=ft.Paint(color=ft.Colors.GREY_900),
                        ),
                    ]
                ),
            )
            self.on_hover = self.change_cursor
            self.on_pan_start = self.change_volume
            self.on_pan_update = self.change_volume
            self.on_change_volume = on_change_volume

        def change_audio_volume(self, volume):
            self.audio.volume = volume

        def change_cursor(self, e: ft.HoverEvent):
            e.control.mouse_cursor = ft.MouseCursor.CLICK
            e.control.update()

        def change_volume(self, e):
            if e.local_x >= 0 and e.local_x <= self.content.width:
                self.change_audio_volume((e.local_x) / self.content.width)
                self.content.content.shapes[1].width = e.local_x  # New volume
                self.content.content.shapes[2].x = e.local_x  # Thumb
                self.on_change_volume()
                self.page.update()

        def mute(self):
            self.previous_volume = self.audio.volume
            self.content.content.shapes[1].width = 0
            self.content.content.shapes[2].x = 0
            self.audio.volume = 0

        def unmute(self):
            self.audio.volume = self.previous_volume
            self.content.content.shapes[1].width = (
                self.content.width * self.audio.volume
            )
            self.content.content.shapes[2].x = self.content.width * self.audio.volume
            print("Unmute")

    class Track(ft.GestureDetector):
        def __init__(self, audio, on_change_position):
            super().__init__()
            self.visible = False
            self.content = ft.Container(
                content=cv.Canvas(
                    on_resize=self.canvas_resized,
                    shapes=[
                        cv.Rect(
                            x=0,
                            y=0,
                            height=5,
                            border_radius=3,
                            paint=ft.Paint(color=ft.Colors.GREY_500),
                            width=100,
                        ),
                        cv.Rect(
                            x=0,
                            y=0,
                            height=5,
                            border_radius=3,
                            paint=ft.Paint(color=ft.Colors.GREY_900),
                            width=0,
                        ),
                    ],
                ),
                height=10,
                width=float("inf"),
            )
            self.audio = audio
            self.audio_duration = 0
            self.on_pan_start = self.find_position
            self.on_pan_update = self.find_position
            self.on_hover = self.change_cursor
            self.on_change_position = on_change_position

        def canvas_resized(self, e: cv.CanvasResizeEvent):
            print("On resize:", e.width, e.height)
            self.track_width = e.width
            e.control.shapes[0].width = e.width
            e.control.update()

        def find_position(self, e):
            position = int(self.audio_duration * e.local_x / self.track_width)
            self.content.content.shapes[1].width = max(
                0, min(e.local_x, self.track_width)
            )
            self.update()
            self.on_change_position(position)

        def change_cursor(self, e: ft.HoverEvent):
            e.control.mouse_cursor = ft.MouseCursor.CLICK
            e.control.update()

    class AudioPlayer(ft.Column):
        def __init__(self, url):
            super().__init__(tight=True)
            self.audio1 = ft.Audio(
                src=url,
                autoplay=False,
                volume=1,
                balance=0,
                on_loaded=self.audio_loaded,
                on_duration_changed=lambda e: print("Duration changed:", e.data),
                on_position_changed=self.change_position,
                on_state_changed=self.state_changed,
                on_seek_complete=lambda _: print("Seek complete"),
            )
            self.position = 0
            self.track_canvas = Track(
                audio=self.audio1, on_change_position=self.seek_position
            )
            self.play_button = ft.IconButton(
                icon=ft.Icons.PLAY_ARROW,
                visible=False,
                on_click=self.play,
            )
            self.pause_button = ft.IconButton(
                icon=ft.Icons.PAUSE,
                visible=False,
                on_click=self.pause,
            )
            self.position_duration = ft.Text()

            self.volume_slider = VolumeSlider(
                audio=self.audio1, on_change_volume=self.check_mute
            )
            self.volume_icon = ft.IconButton(
                icon=ft.Icons.VOLUME_UP,
                visible=False,
                on_click=self.volume_icon_clicked,
            )
            self.controls = [
                self.track_canvas,
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        self.play_button,
                        self.pause_button,
                        self.position_duration,
                        ft.Row(
                            [
                                self.volume_icon,
                                self.volume_slider,
                            ]
                        ),
                    ],
                ),
            ]

        # happens when example is added to the page (when user chooses the Audio control from the grid)
        def did_mount(self):
            self.page.overlay.append(self.audio1)
            # self.track_canvas.audio_duration = self.audio1.get_duration()
            self.page.update()

        # happens when example is removed from the page (when user chooses different control group on the navigation rail)
        def will_unmount(self):
            self.page.overlay.remove(self.audio1)
            self.page.update()

        def audio_loaded(self, e):
            time.sleep(0.1)
            self.track_canvas.visible = True
            self.position_duration.value = (
                f"{convertMillis(0)} / {convertMillis(self.audio1.get_duration())}"
            )
            self.play_button.visible = True
            self.volume_slider.visible = True
            self.volume_icon.visible = True
            self.track_canvas.audio_duration = self.audio1.get_duration()
            self.page.update()

        def play(self, e):
            if self.position != 0:
                self.audio1.resume()

            else:
                self.audio1.play()
            self.play_button.visible = False
            self.pause_button.visible = True
            self.page.update()

        def pause(self, e):
            self.audio1.pause()
            self.play_button.visible = True
            self.pause_button.visible = False
            self.page.update()

        def state_changed(self, e):
            if e.data == "completed":
                self.play_button.visible = True
                self.pause_button.visible = False

        def seek_position(self, position):
            self.audio1.seek(position)
            self.page.update()

        def change_position(self, e):
            self.position = e.data
            self.position_duration.value = f"{convertMillis(int(e.data))} / {convertMillis(self.track_canvas.audio_duration)}"
            self.track_canvas.content.content.shapes[1].width = (
                int(e.data)
                / self.track_canvas.audio_duration
                * self.track_canvas.track_width
            )
            e.control.page.update()

        def volume_icon_clicked(self, e):
            if e.control.icon == ft.Icons.VOLUME_UP:
                e.control.icon = ft.Icons.VOLUME_OFF
                self.volume_slider.mute()
            else:
                e.control.icon = ft.Icons.VOLUME_UP
                self.volume_slider.unmute()
            e.control.page.update()

        def check_mute(self):
            if (
                int(self.audio1.volume * 100) == 0
                and self.volume_icon.icon == ft.Icons.VOLUME_UP
            ):
                self.volume_icon.icon = ft.Icons.VOLUME_OFF
                self.volume_slider.mute()
                self.volume_icon.update()
            elif (
                int(self.audio1.volume * 100) != 0
                and self.volume_icon.icon == ft.Icons.VOLUME_OFF
            ):
                self.volume_icon.icon = ft.Icons.VOLUME_UP
                self.volume_slider.unmute()
                self.volume_icon.update()

    player = AudioPlayer(url=url)

    return ft.Container(player, alignment=ft.alignment.center, expand=True)


def main(page: ft.Page):
    page.title = "Flet audio player example"
    page.window_width = 390
    page.window_height = 844

    page.add(example(page))


if __name__ == "__main__":
    ft.app(target=main)
