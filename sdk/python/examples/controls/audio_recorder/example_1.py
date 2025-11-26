import logging

import flet as ft
import flet_audio_recorder as far

logging.basicConfig(level=logging.DEBUG)


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(title=ft.Text("Audio Recorder"), center_title=True)

    path = "test-audio-file.wav"

    def show_snackbar(message):
        page.show_dialog(ft.SnackBar(ft.Text(message)))

    async def handle_recording_start(e: ft.Event[ft.Button]):
        show_snackbar("Starting recording...")
        await recorder.start_recording(output_path=path)

    async def handle_recording_stop(e: ft.Event[ft.Button]):
        output_path = await recorder.stop_recording()
        show_snackbar(f"Stopped recording. Output Path: {output_path}")
        if page.web and output_path is not None:
            await page.launch_url(output_path)

    async def handle_list_devices(e: ft.Event[ft.Button]):
        o = await recorder.get_input_devices()
        show_snackbar(f"Input Devices: {', '.join([f'{d.id}:{d.label}' for d in o])}")

    async def handle_has_permission(e: ft.Event[ft.Button]):
        try:
            status = await recorder.has_permission()
            show_snackbar(f"Audio Recording Permission status: {status}")
        except Exception as e:
            show_snackbar(f"Error checking permission: {e}")

    async def handle_pause(e: ft.Event[ft.Button]):
        print(f"isRecording: {await recorder.is_recording()}")
        if await recorder.is_recording():
            await recorder.pause_recording()

    async def handle_resume(e: ft.Event[ft.Button]):
        print(f"isPaused: {await recorder.is_paused()}")
        if await recorder.is_paused():
            await recorder.resume_recording()

    async def handle_audio_encoder_test(e: ft.Event[ft.Button]):
        print(await recorder.is_supported_encoder(far.AudioEncoder.WAV))

    recorder = far.AudioRecorder(
        configuration=far.AudioRecorderConfiguration(encoder=far.AudioEncoder.WAV),
        on_state_change=lambda e: print(f"State Changed: {e.data}"),
    )

    page.add(
        ft.Button(content="Start Audio Recorder", on_click=handle_recording_start),
        ft.Button(content="Stop Audio Recorder", on_click=handle_recording_stop),
        ft.Button(content="List Devices", on_click=handle_list_devices),
        ft.Button(content="Pause Recording", on_click=handle_pause),
        ft.Button(content="Resume Recording", on_click=handle_resume),
        ft.Button(content="WAV Encoder Support", on_click=handle_audio_encoder_test),
        ft.Button(
            content="Get Audio Recording Permission Status",
            on_click=handle_has_permission,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
