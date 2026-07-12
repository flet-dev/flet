"""
In-process dart_bridge transport for Flet's embedded mode.

`FletDartBridgeServer` is an alternative to `FletSocketServer` that exchanges
the same MsgPack-framed protocol over an in-process byte channel rather than a
Unix-domain socket. The channel is provided by the `dart_bridge` built-in
Python module, registered with CPython via `PyImport_AppendInittab` by
`libdart_bridge` (the native artifact in `flet-dev/dart-bridge`).

Activation: `flet.app.run_async` instantiates this server when
`FLET_DART_BRIDGE_PORT` is set AND `is_embedded()` is true. The Dart-side port
acts as the channel key in both directions:

- inbound  (Dart → Python): dart_bridge invokes `__on_bytes(payload)` from C
  under the GIL whenever the Dart side calls `bridge.send(bytes)`.
- outbound (Python → Dart): `send_message` calls `dart_bridge.send_bytes(
  port, packed)` which non-blockingly posts to the Dart native port.

The MsgPack protocol layer is identical to `FletSocketServer`; only the byte
transport differs.
"""

import asyncio
import contextlib
import inspect
import logging
import traceback
from collections.abc import Awaitable
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Any, Callable, Optional

import dart_bridge  # type: ignore  # provided by libdart_bridge inittab
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

if TYPE_CHECKING:
    from flet.app import AppCallable

logger = logging.getLogger("flet")
transport_log = logging.getLogger("flet_transport")


class FletDartBridgeServer(Connection):
    """
    Connection transport that uses the `dart_bridge` built-in module instead
    of an asyncio Unix-domain socket. See module docstring for the rationale.

    Lifecycle: `start()` registers a byte handler with `dart_bridge`; bytes
    arrive synchronously on whatever OS thread Dart called `bridge.send` from,
    so the handler is just a thread-safe enqueue onto an asyncio.Queue that an
    inbound coroutine drains on the event loop.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        port: int,
        on_session_created: Optional[Callable[[Session], Awaitable[Any]]] = None,
        before_main: Optional["AppCallable"] = None,
        executor: Optional[ThreadPoolExecutor] = None,
    ):
        super().__init__()
        self.__port = port
        self.__on_session_created = on_session_created
        self.__before_main = before_main
        self.session: Optional[Session] = None
        self.__inbound_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self.__inbound_task: Optional[asyncio.Task] = None
        self.__running_tasks: set[asyncio.Task] = set()
        # In-process transport — DataChannel bytes move at memcpy speed.
        self.local_data_transport = True
        self.loop = loop
        self.executor = executor
        self.pubsubhub = PubSubHub(loop=loop, executor=executor)
        self.page_url = f"dartbridge://{port}"

    async def start(self):
        """
        Registers the inbound byte handler with `dart_bridge` and schedules
        the inbound dispatch coroutine. Returns immediately — there is no
        per-client handshake at the transport level (the first
        REGISTER_CLIENT frame from Dart is the application-level handshake).
        """
        logger.info("Starting up dart_bridge server on port %s", self.__port)
        dart_bridge.set_enqueue_handler_func(self.__port, self.__on_bytes)
        self.__inbound_task = asyncio.create_task(self.__inbound_loop())

    def __on_bytes(self, payload: bytes) -> None:
        """
        Receives a byte frame from `dart_bridge`. Called synchronously under
        the GIL from C — may run on a non-loop thread, so we marshal onto
        the loop via `call_soon_threadsafe`.
        """
        self.loop.call_soon_threadsafe(self.__inbound_queue.put_nowait, payload)

    async def __inbound_loop(self):
        """
        Drains the inbound queue and dispatches each packet. Each dart_bridge
        send delivers one complete packet — `[type:u8][payload]`. type=0x00
        is a MsgPack-encoded Flet control frame, decoded and dispatched as
        a protocol message; type=0x01 is a raw DataChannel frame, but on
        the dart_bridge transport that *only* carries the Flet protocol —
        DataChannels in embedded mode get their own dedicated PythonBridge,
        so a 0x01 here would be an error and we log+drop.
        """
        try:
            while True:
                packet = await self.__inbound_queue.get()
                if not packet:
                    continue
                ptype = packet[0]
                if ptype == 0x00:
                    try:
                        msg = msgpack.unpackb(
                            packet[1:], ext_hook=decode_ext_from_msgpack
                        )
                        await self.__on_message(msg)
                    except Exception:
                        logger.error(
                            "Error dispatching dart_bridge frame", exc_info=True
                        )
                elif ptype == 0x01:
                    logger.debug(
                        "dart_bridge channel received a 0x01 data frame; "
                        "DataChannels in embedded mode should use a dedicated "
                        "PythonBridge, not the protocol channel."
                    )
                else:
                    logger.debug(
                        "dart_bridge channel received packet with unknown type 0x%02x",
                        ptype,
                    )
        except asyncio.CancelledError:
            logger.debug("dart_bridge inbound loop cancelled.")

    async def __on_message(self, data: Any):
        """
        Protocol dispatch — identical to `FletSocketServer.__on_message`.
        Duplicated here to keep the two transports decoupled; refactor into
        a shared base once both have stabilised.
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
            raise RuntimeError(f'Unknown message "{action}": {body}')

        if task:
            self.__running_tasks.add(task)
            task.add_done_callback(self.__running_tasks.discard)

    def send_message(self, message: ClientMessage):
        """
        Encodes a protocol message and posts it to the Dart side via
        `dart_bridge.send_bytes`. Non-blocking; ordering is preserved by the
        Dart VM's port queue. Wire format: `[0x00][msgpack body]` — no
        length prefix (the bridge preserves message boundaries).
        """
        transport_log.debug("send_message: %s", message)
        body = msgpack.packb(
            [message.action, message.body],
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        packet = b"\x00" + body
        try:
            dart_bridge.send_bytes(self.__port, packet)
        except Exception:
            logger.error("dart_bridge.send_bytes failed", exc_info=True)

    def data_channel_for(self, channel_id: int):
        """Resolve the DataChannel for `channel_id`. In embedded native mode
        each DataChannel rides its own dedicated PythonBridge native port
        (the `channel_id` *is* the port). Idempotent.
        """
        from flet.data_channel import _DartBridgeDataChannel

        # No registry needed: _DartBridgeDataChannel is stateless wrt port
        # and the dart_bridge module routes by port number internally. We
        # still cache per port to avoid duplicate handler registrations.
        if not hasattr(self, "_data_channels"):
            self._data_channels: dict[int, Any] = {}
        existing = self._data_channels.get(channel_id)
        if existing is not None:
            return existing
        channel = _DartBridgeDataChannel(channel_id)
        self._data_channels[channel_id] = channel
        return channel

    async def close(self):
        """
        Releases the dart_bridge handler registration and cancels pending
        inbound work. Mirrors `FletSocketServer.close()` so the caller side
        in `flet.app.run_async` can treat both transports uniformly.
        """
        logger.debug("Closing dart_bridge server...")
        try:
            dart_bridge.set_enqueue_handler_func(self.__port, None)
        except Exception:
            logger.debug("Error unregistering dart_bridge handler", exc_info=True)

        session = self.session
        self.session = None
        if session is not None:
            try:
                session.close()
            except Exception:
                logger.debug("Error closing session", exc_info=True)

        if self.__inbound_task and not self.__inbound_task.done():
            self.__inbound_task.cancel()
            with contextlib.suppress(asyncio.CancelledError, Exception):
                await self.__inbound_task

        for task in list(self.__running_tasks):
            if not task.done():
                task.cancel()
        if self.__running_tasks:
            await asyncio.gather(*self.__running_tasks, return_exceptions=True)
        self.__running_tasks.clear()

        if self.executor:
            self.executor.shutdown(wait=False, cancel_futures=True)

        logger.debug("dart_bridge server closed.")
