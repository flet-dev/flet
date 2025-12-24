import asyncio
import contextlib
import inspect
import logging
import os
import tempfile
import traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Optional

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

logger = logging.getLogger("flet")
transport_log = logging.getLogger("flet_transport")


class FletSocketServer(Connection):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        port: int = 0,
        uds_path: Optional[str] = None,
        on_session_created=None,
        before_main=None,
        blocking=False,
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
        self.loop = loop
        self.executor = executor
        self.pubsubhub = PubSubHub(loop=loop, executor=executor)

    async def start(self):
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
            logger.info(f"Starting up TCP server on {host}:{port}")
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
            logger.info(f"Starting up UDS server on {self.__uds_path}")
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
        if not self.__connected and self.__writer is None:
            logger.debug("No active connection to terminate.")
            return

        logger.debug(f"Terminating existing connection ({reason}).")

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
        unpacker = msgpack.Unpacker(ext_hook=decode_ext_from_msgpack)
        try:
            while True:
                buf = await reader.read(1024 * 1024)
                if not buf:
                    break
                unpacker.feed(buf)
                for msg in unpacker:
                    if self.__connection_token != connection_token:
                        return
                    await self.__on_message(msg)
        except asyncio.CancelledError:
            logger.debug("Receive loop cancelled.")
        except Exception as e:
            logger.debug(f"Error receiving socket data from Flet client: {e}")
        finally:
            logger.debug("Receive loop exiting.")

    async def __send_loop(
        self,
        writer: asyncio.StreamWriter,
        send_queue: asyncio.Queue[bytes],
        connection_token: int,
    ):
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
            logger.debug(f"Error in send loop: {e}")
        finally:
            logger.debug("Send loop exiting.")

    async def __on_message(self, data: Any):
        action = ClientAction(data[0])
        body = data[1]
        transport_log.debug(f"_on_message: {action} {body}")
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
        transport_log.debug(f"send_message: {message}")
        m = msgpack.packb(
            [message.action, message.body],
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        if self.__send_queue is not None:
            self.__send_queue.put_nowait(m)

    async def close(self):
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
