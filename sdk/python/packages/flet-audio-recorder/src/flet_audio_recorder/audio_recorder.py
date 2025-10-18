from dataclasses import field
from typing import Optional

import flet as ft

from .types import (
    AudioEncoder,
    AudioRecorderConfiguration,
    AudioRecorderStateChangeEvent,
    InputDevice,
)

__all__ = ["AudioRecorder"]


@ft.control("AudioRecorder")
class AudioRecorder(ft.Service):
    """
    A control that allows you to record audio from your device.

    This control can record audio using different
    audio encoders and also allows configuration
    of various audio recording parameters such as
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
    Event handler that is called when the state of the audio recorder changes.
    """

    async def start_recording(
        self,
        output_path: Optional[str] = None,
        configuration: Optional[AudioRecorderConfiguration] = None,
    ) -> bool:
        """
        Starts recording audio and saves it to the specified output path.

        If not on the web, the `output_path` parameter must be provided.

        Args:
            output_path: The file path where the audio will be saved.
                It must be specified if not on web.
            configuration: The configuration for the audio recorder.
                If `None`, the `AudioRecorder.configuration` will be used.

        Returns:
            `True` if recording was successfully started, `False` otherwise.

        Raises:
            ValueError: If `output_path` is not provided on platforms other than web.
        """
        if not (self.page.web or output_path):
            raise ValueError("output_path must be provided on platforms other than web")
        return await self._invoke_method(
            method_name="start_recording",
            arguments={
                "output_path": output_path,
                "configuration": configuration
                if configuration is not None
                else self.configuration,
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
        Stops the audio recording and optionally returns the path to the saved file.

        Returns:
            The file path where the audio was saved or `None` if not applicable.
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
        Checks if the app has permission to record audio.

        Returns:
            `True` if the app has permission, `False` otherwise.
        """
        return await self._invoke_method("has_permission")
