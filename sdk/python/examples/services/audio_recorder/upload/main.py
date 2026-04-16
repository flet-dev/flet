import time

import flet as ft
import flet_audio_recorder as far


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(title=ft.Text("Audio Recorder Upload"), center_title=True)

    upload_status = ft.Text("Waiting to record...")

    def show_snackbar(message: str):
        page.show_dialog(ft.SnackBar(content=ft.Text(message)))

    def handle_upload(e: far.AudioRecorderUploadEvent):
        if e.error:
            upload_status.value = f"Upload error: {e.error}"
        elif e.progress == 1:
            upload_status.value = f"Upload complete: {e.bytes_uploaded or 0} bytes."
        else:
            upload_status.value = f"Uploading: {e.bytes_uploaded or 0} bytes sent."

    async def handle_recording_start(e: ft.Event[ft.Button]):
        if not await recorder.has_permission():
            show_snackbar("Microphone permission is required.")
            return

        file_name = f"recordings/recording-{int(time.time())}.pcm"
        upload_status.value = "Recording..."
        await recorder.start_recording(
            upload=far.AudioRecorderUploadSettings(
                upload_url=page.get_upload_url(file_name, expires=600),
                file_name=file_name,
            ),
            configuration=far.AudioRecorderConfiguration(
                encoder=far.AudioEncoder.PCM16BITS,
                channels=1,
            ),
        )

    async def handle_recording_stop(e: ft.Event[ft.Button]):
        await recorder.stop_recording()
        show_snackbar("Recording stopped.")

    recorder = far.AudioRecorder(
        configuration=far.AudioRecorderConfiguration(
            encoder=far.AudioEncoder.PCM16BITS,
            channels=1,
        ),
        on_upload=handle_upload,
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text("Record PCM16 audio and upload it as it streams."),
                    ft.Button("Start upload", on_click=handle_recording_start),
                    ft.Button("Stop recording", on_click=handle_recording_stop),
                    upload_status,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main, upload_dir="uploads")
