import io
import time
import wave

import flet as ft
import flet_audio_recorder as far

SAMPLE_RATE = 44100
CHANNELS = 1
BYTES_PER_SAMPLE = 2


def pcm_to_wav_bytes(pcm_data: bytes) -> bytes:
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, "wb") as wav:
        wav.setnchannels(CHANNELS)
        wav.setsampwidth(BYTES_PER_SAMPLE)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(pcm_data)
    return wav_buffer.getvalue()


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    buffer = bytearray()

    def show_snackbar(message: str):
        page.show_dialog(ft.SnackBar(content=message, duration=ft.Duration(seconds=5)))

    def handle_stream(e: far.AudioRecorderStreamEvent):
        buffer.extend(e.chunk)
        status.value = (
            f"Streaming chunk {e.sequence}; {e.bytes_streamed} bytes collected."
        )

    async def handle_recording_start(e: ft.Event[ft.Button]):
        if not await recorder.has_permission():
            show_snackbar("Microphone permission is required.")
            return

        buffer.clear()
        status.value = "Recording..."
        await recorder.start_recording(
            configuration=far.AudioRecorderConfiguration(
                encoder=far.AudioEncoder.PCM16BITS,
                sample_rate=SAMPLE_RATE,
                channels=CHANNELS,
            ),
        )

    async def handle_recording_stop(e: ft.Event[ft.Button]):
        await recorder.stop_recording()
        if not buffer:
            show_snackbar("Nothing was recorded.")
            return

        wav_bytes = pcm_to_wav_bytes(bytes(buffer))
        file_name = f"recording-{int(time.time())}.wav"
        file_path = await ft.FilePicker().save_file(
            file_name=file_name,
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["wav"],
            src_bytes=wav_bytes,
        )

        if file_path and not (page.web or page.platform.is_mobile()):
            with open(file_path, "wb") as output:
                output.write(wav_bytes)

        if page.web:
            status.value = f"Downloaded {file_name} ({len(wav_bytes)} bytes)."
        else:
            status.value = f"Saved to: {file_path}" if file_path else "Save cancelled."
        show_snackbar(status.value)

    recorder = far.AudioRecorder(on_stream=handle_stream)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Stream PCM16 audio chunks and save or download "
                        "them as a WAV file."
                    ),
                    ft.Button("Start recording", on_click=handle_recording_start),
                    ft.Button("Stop and save", on_click=handle_recording_stop),
                    status := ft.Text(),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
