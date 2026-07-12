import asyncio
import contextlib
import inspect
import logging
import os
import tempfile
import traceback
from collections.abc import Awaitable
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Optional

import msgpack

from flet.controls.base_control import BaseControl
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    ClientAction,
    ClientMessage,
    ControlEventBody,
    InvokeMethodResponseBody,
    RegisterClientRequestBody,
    RegisterClientResponseBody,
    UpdateControlPropsBody,
    configure_encode_object_for_msgpack,
    decode_ext_from_msgpack,
)
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub
from flet.utils import get_free_tcp_port, is_windows, random_string

if TYPE_CHECKING:
    from flet.app import AppCallable

logger = logging.getLogger("flet")
transport_log = logging.getLogger("flet_transport")


class FletSocketServer(Connection):
    """
    Socket-based transport for Flet backend messaging.

    This connection accepts a single active client at a time over TCP or Unix domain
    socket (UDS), decodes protocol frames, manages session lifecycle, and forwards
    outbound messages through an internal send queue.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        port: int = 0,
        uds_path: Optional[str] = None,
        on_session_created: Optional[Callable[[Session], Awaitable[Any]]] = None,
        before_main: Optional["AppCallable"] = None,
        blocking: bool = False,
        executor: Optional[ThreadPoolExecutor] = None,
    ):
        super().__init__()
        self.__server = None
        self.__send_loop_task: asyncio.Task | None = None
        self.__receive_loop_task: asyncio.Task | None = None
        self.__connected: bool | None = None
        self.__writer: asyncio.StreamWriter | None = None
        self.__connection_lock = asyncio.Lock()
        self.__connection_token = 0
        self.session = None
        self.__send_queue: asyncio.Queue[bytes] | None = None
        self.__port = port
        self.__uds_path = uds_path
        self.__on_session_created = on_session_created
        self.__before_main = before_main
        self.__blocking = blocking
        self.__running_tasks = set()
        # DataChannel mux registry. Keyed by channel_id minted on the Dart
        # side; populated lazily on the first Control.get_data_channel(id)
        # call. Frames for unknown ids are silently dropped.
        self._data_channels: dict[int, Any] = {}
        # UDS or localhost TCP only — always same-machine.
        self.local_data_transport = True
        self.loop = loop
        self.executor = executor
        self.pubsubhub = PubSubHub(loop=loop, executor=executor)

    async def start(self):
        """
        Starts listening for client connections.

        Transport selection:
        - TCP on Windows or when `port > 0`;
        - UDS on non-Windows when `port == 0`.

        When `blocking=True`, this method waits on `serve_forever()`. Otherwise it
        schedules serving in a background task and returns.
        """
        self.__connected = False
        self.__receive_loop_task = None
        self.__send_loop_task = None
        self.__writer = None
        self.__send_queue = None
        if is_windows() or self.__port > 0:
            # TCP
            host = "localhost"
            port = self.__port if self.__port > 0 else get_free_tcp_port()
            self.page_url = f"tcp://{host}:{port}"
            logger.info("Starting up TCP server on %s:%s", host, port)
            self.__server = await asyncio.start_server(
                self.handle_connection, host, port
            )
        else:
            # UDS
            if not self.__uds_path:
                self.__uds_path = str(
                    Path(tempfile.gettempdir()).joinpath(random_string(10))
                )
            if os.path.exists(self.__uds_path):
                os.remove(self.__uds_path)
            self.page_url = self.__uds_path
            logger.info("Starting up UDS server on %s", self.__uds_path)
            self.__server = await asyncio.start_unix_server(
                self.handle_connection, self.__uds_path
            )

        if self.__blocking:
            self.__serve_task = None
            await self.__server.serve_forever()
        else:
            self.__serve_task = asyncio.create_task(self.__server.serve_forever())

    async def handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        """
        Handles an incoming socket connection.

        Only one active connection is allowed. A new connection replaces any existing
        one, starts paired receive/send loops, and remains active until one loop
        completes or the connection is superseded.

        Args:
            reader: Socket stream reader.
            writer: Socket stream writer.
        """
        async with self.__connection_lock:
            await self.__terminate_active_connection_locked(reason="replaced")

            self.__connected = True
            self.__connection_token += 1
            connection_token = self.__connection_token
            self.__writer = writer
            send_queue: asyncio.Queue[bytes] = asyncio.Queue()
            self.__send_queue = send_queue

            logger.debug("Connected new socket client")

            receive_task = asyncio.create_task(
                self.__receive_loop(reader, connection_token)
            )
            send_task = asyncio.create_task(
                self.__send_loop(writer, send_queue, connection_token)
            )
            self.__receive_loop_task = receive_task
            self.__send_loop_task = send_task

        try:
            _, pending = await asyncio.wait(
                [receive_task, send_task],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in pending:
                task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await task
        finally:
            terminated_active = False
            async with self.__connection_lock:
                if (
                    self.__writer is writer
                    and self.__connection_token == connection_token
                ):
                    await self.__terminate_active_connection_locked(
                        reason="client_disconnected"
                    )
                    terminated_active = True

            if not terminated_active:
                writer.close()
                with contextlib.suppress(Exception):
                    await writer.wait_closed()
            logger.debug("Connection writer closed.")

    async def __terminate_active_connection_locked(self, reason: str) -> None:
        """
        Terminates the currently active connection and related tasks.

        Locking contract:
            Caller must hold `self.__connection_lock`.

        Actions performed:
        - closes current session (if present);
        - cancels receive/send and running handler tasks;
        - closes active writer and clears connection state.

        Args:
            reason: Diagnostic reason used in debug logs.
        """
        if not self.__connected and self.__writer is None:
            logger.debug("No active connection to terminate.")
            return

        logger.debug("Terminating existing connection (%s).", reason)

        session_to_close = self.session
        self.session = None

        if session_to_close is not None:
            try:
                session_to_close.close()
            except Exception:
                logger.debug("Error closing session.", exc_info=True)

        tasks_to_cancel: list[asyncio.Task] = []
        for task in [
            self.__receive_loop_task,
            self.__send_loop_task,
            *self.__running_tasks,
        ]:
            if task and not task.done():
                tasks_to_cancel.append(task)

        if tasks_to_cancel:
            for task in tasks_to_cancel:
                task.cancel()
            with contextlib.suppress(Exception):
                await asyncio.gather(*tasks_to_cancel, return_exceptions=True)

        self.__running_tasks.clear()
        self.__receive_loop_task = None
        self.__send_loop_task = None

        old_writer = self.__writer
        self.__writer = None
        self.__send_queue = None
        self.__connected = False

        if old_writer is not None:
            old_writer.close()
            with contextlib.suppress(Exception):
                await old_writer.wait_closed()

    async def __receive_loop(self, reader: asyncio.StreamReader, connection_token: int):
        """
        Reads and dispatches inbound packets from the socket.

        Wire format on the byte stream: each packet is prefixed with a 4-byte
        little-endian length, then `[type:u8][payload]`. type=0x00 is a
        MsgPack-encoded Flet protocol frame; type=0x01 is a raw DataChannel
        frame (`[channel_id:u32 LE][bytes]`).

        The loop exits when:
        - socket EOF is reached;
        - the connection token no longer matches (connection replaced);
        - the task is cancelled.

        Args:
            reader: Socket stream reader to consume bytes from.
            connection_token: Token identifying the connection generation.
        """
        try:
            while True:
                try:
                    header = await reader.readexactly(4)
                except asyncio.IncompleteReadError:
                    break  # EOF mid-stream or clean close
                length = int.from_bytes(header, "little", signed=False)
                if length == 0:
                    continue
                try:
                    packet = await reader.readexactly(length)
                except asyncio.IncompleteReadError:
                    logger.debug("Truncated packet read; aborting receive loop.")
                    break
                if self.__connection_token != connection_token:
                    return
                ptype = packet[0]
                if ptype == 0x00:
                    msg = msgpack.unpackb(packet[1:], ext_hook=decode_ext_from_msgpack)
                    await self.__on_message(msg)
                elif ptype == 0x01:
                    if len(packet) < 5:
                        logger.debug("Dropping malformed data-channel frame.")
                        continue
                    channel_id = int.from_bytes(packet[1:5], "little", signed=False)
                    self.__on_data_channel_frame(channel_id, packet[5:])
                else:
                    logger.debug("Dropping packet with unknown type 0x%02x", ptype)
        except asyncio.CancelledError:
            logger.debug("Receive loop cancelled.")
        except Exception as e:
            logger.debug("Error receiving socket data from Flet client: %s", e)
        finally:
            logger.debug("Receive loop exiting.")

    def __on_data_channel_frame(self, channel_id: int, payload: bytes) -> None:
        """Routes an inbound `[0x01][channel_id][payload]` frame to its
        registered DataChannel. Silently drops frames for unknown ids
        (handles unmount races)."""
        channel = self._data_channels.get(channel_id)
        if channel is not None:
            channel._deliver(payload)

    async def __send_loop(
        self,
        writer: asyncio.StreamWriter,
        send_queue: asyncio.Queue[bytes],
        connection_token: int,
    ):
        """
        Sends outbound frames from the queue to the active socket writer.

        The loop exits when the connection token changes (connection replaced) or
        when cancelled.

        Args:
            writer: Socket writer used to send bytes.
            send_queue: Queue of pre-encoded MsgPack frames.
            connection_token: Token identifying the connection generation.
        """
        try:
            while True:
                if self.__connection_token != connection_token:
                    return
                message = await send_queue.get()
                writer.write(message)
                await writer.drain()
        except asyncio.CancelledError:
            logger.debug("Send loop cancelled.")
        except Exception as e:
            logger.debug("Error in send loop: %s", e)
        finally:
            logger.debug("Send loop exiting.")

    async def __on_message(self, data: Any):
        """
        Processes one decoded protocol frame from the client.

        Supported actions:
        - `REGISTER_CLIENT`: create session, apply initial page patch (for new
          sessions), run `before_main`, and send register response;
        - `CONTROL_EVENT`: dispatch control event to session;
        - `UPDATE_CONTROL_PROPS`: apply property patch to a control;
        - `INVOKE_METHOD`: deliver invoke-method response back to session waiter.

        Args:
            data: Decoded frame in the form `[action_code, body]`.

        Raises:
            RuntimeError: If the action code is unknown.
        """
        action = ClientAction(data[0])
        body = data[1]
        transport_log.debug("_on_message: %s %s", action, body)
        task = None
        if action == ClientAction.REGISTER_CLIENT:
            req = RegisterClientRequestBody(**body)

            # create new session
            self.session = Session(self)

            # apply page patch
            if not req.session_id:
                self.session.apply_page_patch(req.page)

            register_error = ""
            try:
                if inspect.iscoroutinefunction(self.__before_main):
                    await self.__before_main(self.session.page)
                elif callable(self.__before_main):
                    self.__before_main(self.session.page)
            except Exception as e:
                register_error = f"{e}\n{traceback.format_exc()}"
                logger.error("Unhandled error in before_main() handler", exc_info=True)

            # register response
            self.send_message(
                ClientMessage(
                    ClientAction.REGISTER_CLIENT,
                    RegisterClientResponseBody(
                        session_id=self.session.id,
                        page_patch=self.session.get_page_patch(),
                        error=register_error,
                    ),
                )
            )

            if register_error:
                self.session.error(register_error)
            elif self.__on_session_created is not None:
                task = asyncio.create_task(self.__on_session_created(self.session))

        elif action == ClientAction.CONTROL_EVENT:
            req = ControlEventBody(**body)
            task = asyncio.create_task(
                self.session.dispatch_event(req.target, req.name, req.data)
            )

        elif action == ClientAction.UPDATE_CONTROL_PROPS:
            req = UpdateControlPropsBody(**body)
            self.session.apply_patch(req.id, req.props)

        elif action == ClientAction.INVOKE_METHOD:
            req = InvokeMethodResponseBody(**body)
            self.session.handle_invoke_method_results(
                req.control_id, req.call_id, req.result, req.error
            )

        else:
            # it's something else
            raise RuntimeError(f'Unknown message "{action}": {body}')

        if task:
            self.__running_tasks.add(task)
            task.add_done_callback(self.__running_tasks.discard)

    def send_message(self, message: ClientMessage):
        """
        Encodes and queues an outbound message for the active connection.

        Wire format: `[length:u32 LE][0x00][msgpack body]`. The send loop
        writes the bytes verbatim to the socket.

        If no active send queue exists (no connected client), the message is dropped.

        Args:
            message: Protocol message to send.
        """
        transport_log.debug("send_message: %s", message)
        body = msgpack.packb(
            [message.action, message.body],
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        packet = b"\x00" + body
        framed = len(packet).to_bytes(4, "little", signed=False) + packet
        if self.__send_queue is not None:
            self.__send_queue.put_nowait(framed)

    def send_data_channel_frame(self, channel_id: int, payload: bytes) -> None:
        """Send a raw DataChannel frame `[length][0x01][channel_id:u32 LE][bytes]`.
        Called by `_ProtocolMuxedDataChannel.send` on the Python side."""
        # Single-copy assembly — sequential concats would copy the
        # (potentially multi-MB) payload twice.
        framed = b"".join(
            [
                (5 + len(payload)).to_bytes(4, "little", signed=False),
                b"\x01",
                channel_id.to_bytes(4, "little", signed=False),
                payload,
            ]
        )
        if self.__send_queue is not None:
            self.__send_queue.put_nowait(framed)

    def data_channel_for(self, channel_id: int):
        """Resolve or construct the muxed DataChannel for `channel_id`.
        Idempotent — returns the same instance per id within the session.
        Called from `Control.get_data_channel(id)`.
        """
        from flet.data_channel import _ProtocolMuxedDataChannel

        existing = self._data_channels.get(channel_id)
        if existing is not None:
            return existing
        channel = _ProtocolMuxedDataChannel(channel_id, self)
        self._data_channels[channel_id] = channel
        return channel

    def unregister_data_channel(self, channel_id: int) -> None:
        self._data_channels.pop(channel_id, None)

    async def close(self):
        """
        Gracefully shuts down the socket server and transport resources.

        This method terminates the active connection, stops the listening server,
        shuts down the optional executor, cancels serving tasks, and removes a UDS
        socket file when used.
        """
        logger.debug("Closing connection...")

        async with self.__connection_lock:
            await self.__terminate_active_connection_locked(reason="close()")

        if self.__server:
            logger.debug("Shutting down TCP server...")
            self.__server.close()
            await self.__server.wait_closed()

        if self.executor:
            logger.debug("Shutting down thread pool...")
            self.executor.shutdown(wait=False, cancel_futures=True)

        logger.debug("Cancelling pending tasks...")

        tasks = [
            task
            for task in [
                self.__serve_task,
            ]
            if task
        ]

        for task in tasks:
            task.cancel()

        try:
            await asyncio.wait_for(
                asyncio.gather(*tasks, return_exceptions=True), timeout=1.0
            )
        except asyncio.TimeoutError:
            logger.warning("Some tasks did not exit in time, skipping.")
        except asyncio.CancelledError:
            pass
        if self.__uds_path and os.path.exists(self.__uds_path):
            os.unlink(self.__uds_path)

        logger.debug("Connection closed.")
