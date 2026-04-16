import wave

import flet as ft
import flet_audio_recorder as far

SAMPLE_RATE = 44100
CHANNELS = 1
BYTES_PER_SAMPLE = 2
OUTPUT_FILE = "streamed-recording.wav"


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.appbar = ft.AppBar(title=ft.Text("Audio Recorder Stream"), center_title=True)

    buffer = bytearray()
    status = ft.Text("Waiting to record...")

    def show_snackbar(message: str):
        page.show_dialog(ft.SnackBar(content=ft.Text(message)))

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

        with wave.open(OUTPUT_FILE, "wb") as wav:
            wav.setnchannels(CHANNELS)
            wav.setsampwidth(BYTES_PER_SAMPLE)
            wav.setframerate(SAMPLE_RATE)
            wav.writeframes(buffer)

        status.value = f"Saved {len(buffer)} bytes to {OUTPUT_FILE}."
        show_snackbar(status.value)

    recorder = far.AudioRecorder(
        configuration=far.AudioRecorderConfiguration(
            encoder=far.AudioEncoder.PCM16BITS,
            sample_rate=SAMPLE_RATE,
            channels=CHANNELS,
        ),
        on_stream=handle_stream,
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text("Record PCM16 audio chunks and save them as a WAV file."),
                    ft.Button("Start streaming", on_click=handle_recording_start),
                    ft.Button("Stop and save", on_click=handle_recording_stop),
                    status,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
