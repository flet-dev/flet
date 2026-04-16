import time

import flet as ft
import flet_audio_recorder as far


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def show_snackbar(message: str):
        page.show_dialog(ft.SnackBar(content=message, duration=ft.Duration(seconds=5)))

    def handle_upload(e: far.AudioRecorderUploadEvent):
        if e.error:
            status.value = f"Upload error: {e.error}"
        elif e.progress == 1:
            status.value = f"Upload complete: {e.bytes_uploaded or 0} bytes."
        else:
            status.value = f"Uploading: {e.bytes_uploaded or 0} bytes sent."

    async def handle_recording_start(e: ft.Event[ft.Button]):
        if not await recorder.has_permission():
            show_snackbar("Microphone permission is required.")
            return

        file_name = f"recordings/rec-{int(time.time())}.pcm"
        try:
            upload_url = page.get_upload_url(file_name=file_name, expires=600)
        except RuntimeError as ex:
            if "FLET_SECRET_KEY" not in str(ex):
                raise
            status.value = (
                "Uploads require a secret key. "
                "Set FLET_SECRET_KEY before running this app."
            )
            show_snackbar(status.value)
            return

        status.value = "Recording..."
        await recorder.start_recording(
            upload=far.AudioRecorderUploadSettings(
                upload_url=upload_url,
                file_name=file_name,
            ),
            configuration=far.AudioRecorderConfiguration(
                encoder=far.AudioEncoder.PCM16BITS,
                channels=1,
            ),
        )

    async def handle_recording_stop(e: ft.Event[ft.Button]):
        await recorder.stop_recording()
        show_snackbar(
            "Recording stopped. See 'uploads/recordings' folder for the recorded file."
        )

    recorder = far.AudioRecorder(on_upload=handle_upload)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Record PCM16 audio and upload it as it streams."),
                    ft.Button("Start upload", on_click=handle_recording_start),
                    ft.Button("Stop recording", on_click=handle_recording_stop),
                    status := ft.Text(),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(
        main,
        upload_dir="uploads",
    )
