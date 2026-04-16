from dataclasses import field
from typing import Optional

import flet as ft

from .types import (
    AudioEncoder,
    AudioRecorderConfiguration,
    AudioRecorderStateChangeEvent,
    AudioRecorderStreamEvent,
    AudioRecorderUploadEvent,
    AudioRecorderUploadSettings,
    InputDevice,
)

__all__ = ["AudioRecorder"]


@ft.control("AudioRecorder")
class AudioRecorder(ft.Service):
    """
    A control that allows you to record audio from your device.

    This control can record audio using different audio encoders and also allows
    configuration of various audio recording parameters such as
    noise suppression, echo cancellation, and more.
    """

    configuration: AudioRecorderConfiguration = field(
        default_factory=lambda: AudioRecorderConfiguration()
    )
    """
    The default configuration of the audio recorder.
    """

    on_state_change: Optional[ft.EventHandler[AudioRecorderStateChangeEvent]] = None
    """
    Called when recording state changes.
    """

    on_upload: Optional[ft.EventHandler[AudioRecorderUploadEvent]] = None
    """
    Called when streaming upload progress or errors are available.
    """

    on_stream: Optional[ft.EventHandler[AudioRecorderStreamEvent]] = None
    """
    Called when a raw :attr:`~flet_audio_recorder.AudioEncoder.PCM16BITS` \
    recording chunk is available.
    """

    async def start_recording(
        self,
        output_path: Optional[str] = None,
        configuration: Optional[AudioRecorderConfiguration] = None,
        upload: Optional[AudioRecorderUploadSettings] = None,
    ) -> bool:
        """
        Starts recording audio and saves it to a file or streams it.

        If neither `upload` nor :attr:`on_stream` is used, `output_path` must be
        provided on platforms other than web.

        When streaming, use :attr:`~flet_audio_recorder.AudioEncoder.PCM16BITS` as
        the encoder. In that case, emitted or uploaded
        :attr:`~flet_audio_recorder.AudioRecorderStreamEvent.chunk`s contain raw PCM16
        data. In some use cases, these chunks can be wrapped in a container such as
        WAV if the output must be directly playable as an audio file.

        Args:
            output_path: The file path where the audio will be saved.
                It must be specified if not on web.
            configuration: The configuration for the audio recorder. If `None`, the
                :attr:`flet_audio_recorder.AudioRecorder.configuration` will be used.
            upload: Upload settings to stream recording bytes directly
                to a destination, for example a URL returned by
                :meth:`flet.Page.get_upload_url`.

        Returns:
            `True` if recording was successfully started, `False` otherwise.

        Raises:
            ValueError: If `output_path` is not provided on platforms other than web
                when neither streaming nor uploads are requested.
            ValueError: If streaming is requested with an encoder other than
                :attr:`~flet_audio_recorder.AudioEncoder.PCM16BITS`.
        """
        is_streaming = upload is not None or self.on_stream is not None
        if not is_streaming and not (self.page.web or output_path):
            raise ValueError("output_path must be provided on platforms other than web")

        effective_configuration = (
            configuration if configuration is not None else self.configuration
        )
        if is_streaming and effective_configuration.encoder != AudioEncoder.PCM16BITS:
            raise ValueError(
                "Streaming recordings require AudioEncoder.PCM16BITS as encoder."
            )

        return await self._invoke_method(
            method_name="start_recording",
            arguments={
                "output_path": output_path,
                "configuration": effective_configuration,
                "upload": upload,
            },
        )

    async def is_recording(self) -> bool:
        """
        Checks whether the audio recorder is currently recording.

        Returns:
            `True` if the recorder is currently recording, `False` otherwise.
        """
        return await self._invoke_method("is_recording")

    async def stop_recording(self) -> Optional[str]:
        """
        Stops the audio recording and optionally returns the recording location.

        Returns:
            The local file path where the audio was saved, a Blob URL on web, or
                `None` when streaming (i.e. when `upload` or :attr:`on_stream` is set).
        """
        return await self._invoke_method("stop_recording")

    async def cancel_recording(self):
        """
        Cancels the current audio recording.
        """
        await self._invoke_method("cancel_recording")

    async def resume_recording(self):
        """
        Resumes a paused audio recording.
        """
        await self._invoke_method("resume_recording")

    async def pause_recording(self):
        """
        Pauses the ongoing audio recording.
        """
        await self._invoke_method("pause_recording")

    async def is_paused(self) -> bool:
        """
        Checks whether the audio recorder is currently paused.

        Returns:
            `True` if the recorder is paused, `False` otherwise.
        """
        return await self._invoke_method("is_paused")

    async def is_supported_encoder(self, encoder: AudioEncoder) -> bool:
        """
        Checks if the given audio encoder is supported by the recorder.

        Args:
            encoder: The audio encoder to check.

        Returns:
            `True` if the encoder is supported, `False` otherwise.
        """
        return await self._invoke_method("is_supported_encoder", {"encoder": encoder})

    async def get_input_devices(self) -> list[InputDevice]:
        """
        Retrieves the available input devices for recording.

        Returns:
            A list of available input devices.
        """
        r = await self._invoke_method("get_input_devices")
        return [
            InputDevice(id=device_id, label=label) for device_id, label in r.items()
        ]

    async def has_permission(self) -> bool:
        """
        Checks if the app has permission to record audio, requesting it if needed.

        Returns:
            `True` if permission is already granted or granted after the request;
                `False` otherwise.
        """
        return await self._invoke_method("has_permission")
