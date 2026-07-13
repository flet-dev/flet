import asyncio
import inspect
import logging
import os
import traceback
import weakref
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import msgpack
from fastapi import WebSocket, WebSocketDisconnect

import flet_web.fastapi as flet_fastapi
from flet.app import AppCallable
from flet.controls.base_control import BaseControl
from flet.controls.context import _context_page, context
from flet.controls.exceptions import FletPageDisconnectedException
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
from flet.utils import random_string, sha1
from flet_web.fastapi.flet_app_manager import app_manager
from flet_web.fastapi.oauth_state import OAuthState
from flet_web.uploads import build_upload_url

logger = logging.getLogger(flet_fastapi.__name__)
transport_log = logging.getLogger("flet_transport")

DEFAULT_FLET_SESSION_TIMEOUT = 3600
DEFAULT_FLET_OAUTH_STATE_TIMEOUT = 600


class FletApp(Connection):
    """
    Handle Flet app WebSocket connections.

    Args:
        loop: `asyncio` event loop (`asyncio.get_running_loop()`).
        executor: Thread pool executor (`app_manager.executor`).
        main: Application entry point - an async method called for newly
            connected user. Handler coroutine must have
            1 parameter of instance `Page`.
        before_main: Called before `main`.
        session_timeout_seconds: Session lifetime, in seconds,
            after user disconnected.
        oauth_state_timeout_seconds: OAuth state lifetime, in seconds, which
            is a maximum allowed time between starting OAuth flow
            and redirecting to OAuth callback URL.
        upload_endpoint_path: Absolute URL of upload endpoint, e.g. `/upload`.
        secret_key: Secret key to sign upload requests.
    """

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        executor: ThreadPoolExecutor,
        main: AppCallable,
        before_main: Optional[AppCallable],
        session_timeout_seconds: int = DEFAULT_FLET_SESSION_TIMEOUT,
        oauth_state_timeout_seconds: int = DEFAULT_FLET_OAUTH_STATE_TIMEOUT,
        upload_endpoint_path: Optional[str] = None,
        secret_key: Optional[str] = None,
    ):
        super().__init__()
        self.__id = random_string(8)
        logger.info(f"New FletApp: {self.__id}")

        self.__session = None
        self.loop = loop
        self.executor = executor
        self.__main = main
        self.__before_main = before_main
        self.__session_timeout_seconds = session_timeout_seconds
        self.__oauth_state_timeout_seconds = oauth_state_timeout_seconds
        self.__running_tasks = set()

        env_session_timeout_seconds = os.getenv("FLET_SESSION_TIMEOUT")
        if env_session_timeout_seconds:
            self.__session_timeout_seconds = int(env_session_timeout_seconds)

        env_oauth_state_timeout_seconds = os.getenv("FLET_OAUTH_STATE_TIMEOUT")
        if env_oauth_state_timeout_seconds:
            self.__oauth_state_timeout_seconds = int(env_oauth_state_timeout_seconds)

        self.__upload_endpoint_path = upload_endpoint_path
        self.__secret_key = secret_key

        # DataChannel mux registry keyed by channel_id minted on the Dart
        # side. Populated lazily on the first Control.get_data_channel(id)
        # call. Frames for unknown ids are silently dropped.
        self._data_channels: dict[int, Any] = {}

        app_id = self.__id
        weakref.finalize(
            self, lambda: logger.info(f"FletApp was garbage collected: {app_id}")
        )

    async def handle(self, websocket: WebSocket):
        """
        Handle WebSocket connection.

        Args:
            websocket: WebSocket instance.
        """
        self.__websocket = websocket

        self.__client_ip = (
            self.__websocket.client.host if self.__websocket.client else ""
        )
        self.__client_user_agent = self.__websocket.headers.get("user-agent", "")
        self.__oauth_state_id = self.__websocket.cookies.get("flet_oauth_state")

        self.pubsubhub = app_manager.get_pubsubhub(self.__main, loop=self.loop)
        self.page_url = str(websocket.url).rsplit("/", 1)[0]
        self.page_name = websocket.url.path.rsplit("/", 1)[0].lstrip("/")

        if not self.__upload_endpoint_path:
            self.__upload_endpoint_path = (
                f"{'' if self.page_name == '' else '/'}{self.page_name}/upload"
            )

        await self.__websocket.accept()
        self.__send_queue = asyncio.Queue()
        send_loop_task = asyncio.create_task(self.__send_loop())
        await self.__receive_loop()
        await send_loop_task

        # disconnect this connection from a session
        await app_manager.disconnect_session(
            self.__get_unique_session_id(self.__session.id),
            self.__session_timeout_seconds,
        )

    async def __on_session_created(self):
        """
        Run app entry handler for a newly created session.

        Initializes page context, executes `main` in supported callable forms
        (coroutine, generator, async generator, sync function), and performs
        post-event updates.
        """

        assert self.__session
        logger.info(f"Start session: {self.__session.id}")
        try:
            assert self.__main is not None
            _context_page.set(self.__session.page)
            context.reset_auto_update()

            if inspect.iscoroutinefunction(self.__main):
                await self.__main(self.__session.page)

            elif inspect.isasyncgenfunction(self.__main):
                async for _ in self.__main(self.__session.page):
                    await self.__session.after_event(self.__session.page)

            elif inspect.isgeneratorfunction(self.__main):
                for _ in self.__main(self.__session.page):
                    await self.__session.after_event(self.__session.page)
            else:
                self.__main(self.__session.page)

            await self.__session.after_event(self.__session.page)
        except FletPageDisconnectedException:
            logger.debug(
                "Session handler attempted to update disconnected page: "
                f"{self.__session.id}"
            )
        except BrokenPipeError:
            logger.info(
                "Session handler terminated: "
                f"{self.__session.id if self.__session else ''}"
            )
        except Exception as e:
            logger.error(
                "Unhandled error processing page session: "
                f"{self.__session.id if self.__session else ''}",
                exc_info=True,
            )
            if self.__session:
                self.__session.error(str(e))

    async def __send_loop(self):
        """
        Drain outbound message queue and forward packed frames to WebSocket.

        The loop stops when `None` sentinel is received, then clears transport
        references.
        """

        assert self.__websocket
        assert self.__send_queue
        while True:
            message = await self.__send_queue.get()
            if message is None:
                break

            try:
                await self.__websocket.send_bytes(message)
            except Exception:
                # re-enqueue the message to repeat it when re-connected
                # self.__send_queue.put_nowait(message)
                raise
        self.__websocket = None
        self.__send_queue = None

    async def __receive_loop(self):
        """
        Receive binary frames from WebSocket and dispatch decoded client messages.

        Wire format: each WebSocket binary frame is one packet —
        `[type:u8][payload]`. type=0x00 is a MsgPack-encoded Flet protocol
        frame; type=0x01 is a raw DataChannel frame
        (`[channel_id:u32 LE][bytes]`).

        On disconnect/error, terminates send loop via queue sentinel when a
        session is active.
        """

        assert self.__websocket
        try:
            while True:
                data = await self.__websocket.receive_bytes()
                if not data:
                    continue
                ptype = data[0]
                if ptype == 0x00:
                    await self.__on_message(
                        msgpack.unpackb(data[1:], ext_hook=decode_ext_from_msgpack)
                    )
                elif ptype == 0x01:
                    if len(data) < 5:
                        logger.debug("Dropping malformed data-channel frame.")
                        continue
                    channel_id = int.from_bytes(data[1:5], "little", signed=False)
                    channel = self._data_channels.get(channel_id)
                    if channel is not None:
                        channel._deliver(data[5:])
                else:
                    logger.debug("Dropping packet with unknown type 0x%02x", ptype)
        except Exception as e:
            if not isinstance(e, WebSocketDisconnect):
                logger.warning(f"Receive loop error: {e}", exc_info=True)
            if self.__session:
                # terminate __send_loop
                await self.__send_queue.put(None)

    async def __on_message(self, data: Any):
        """
        Handle one decoded client message and dispatch
        by `ClientAction`.

        Args:
            data: Decoded message payload from msgpack transport.

        Raises:
            RuntimeError: If message action is unknown.
        """

        action = ClientAction(data[0])
        body = data[1]
        transport_log.debug(f"_on_message: {action} {body}")
        task = None
        if action == ClientAction.REGISTER_CLIENT:
            req = RegisterClientRequestBody(**body)

            new_session = False

            # try to retrieve existing session
            if req.session_id:
                candidate = await app_manager.get_session(
                    self.__get_unique_session_id(req.session_id)
                )
                if candidate is not None and candidate.connection is None:
                    self.__session = candidate
                else:
                    self.__session = None

            oauth_state = None
            if self.__oauth_state_id:
                oauth_state = app_manager.retrieve_state(self.__oauth_state_id)
                if oauth_state:
                    self.__session = await app_manager.get_session(
                        oauth_state.session_id
                    )

            # re-create session
            if self.__session is None:
                new_session = True

                # create new session
                self.__session = Session(self)

                # register session
                await app_manager.add_session(
                    self.__get_unique_session_id(self.__session.id),
                    self.__session,
                )

            _context_page.set(self.__session.page)

            original_route = self.__session.page.route

            # apply page patch
            self.__session.apply_page_patch(req.page)

            register_error = ""
            if new_session:
                # update IP and user-agent
                self.__session.page.client_ip = self.__client_ip
                self.__session.page.client_user_agent = self.__client_user_agent

                # run before_main
                try:
                    if inspect.iscoroutinefunction(self.__before_main):
                        await self.__before_main(self.__session.page)
                    elif callable(self.__before_main):
                        self.__before_main(self.__session.page)
                except Exception as e:
                    register_error = f"{e}\n{traceback.format_exc()}"
                    logger.error(
                        "Unhandled error in before_main() handler", exc_info=True
                    )

            # register response
            self.send_message(
                ClientMessage(
                    ClientAction.REGISTER_CLIENT,
                    RegisterClientResponseBody(
                        session_id=self.__session.id,
                        page_patch=self.__session.get_page_patch()
                        if new_session
                        else self.__session.page,
                        error=register_error,
                    ),
                )
            )

            if register_error:
                self.__session.error(register_error)
                return

            # start session
            if new_session:
                asyncio.create_task(self.__on_session_created())
            else:
                await app_manager.reconnect_session(
                    self.__get_unique_session_id(self.__session.id), self
                )

                if (
                    self.__session.page.route
                    and self.__session.page.route != original_route
                ):
                    asyncio.create_task(
                        self.__session.page._trigger_event(
                            "route_change", {"route": self.__session.page.route}
                        )
                    )

                if oauth_state:
                    await self.__session.page._authorize_callback(
                        {
                            "state": self.__oauth_state_id,
                            "code": oauth_state.code,
                            "error": oauth_state.error,
                            "error_description": oauth_state.error_description,
                        }
                    )

        elif action == ClientAction.CONTROL_EVENT:
            req = ControlEventBody(**body)
            task = asyncio.create_task(
                self.__session.dispatch_event(req.target, req.name, req.data)
            )

        elif action == ClientAction.UPDATE_CONTROL_PROPS:
            req = UpdateControlPropsBody(**body)
            self.__session.apply_patch(req.id, req.props)

        elif action == ClientAction.INVOKE_METHOD:
            req = InvokeMethodResponseBody(**body)
            self.__session.handle_invoke_method_results(
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
        Serialize and enqueue a server message for transport to the client.

        Wire format: one packet per `send_bytes` call —
        `[0x00][msgpack body]`. WebSocket preserves message boundaries so
        no length prefix is needed.

        Args:
            message: Outbound protocol message.
        """

        transport_log.debug(f"send_message: {message}")
        body = msgpack.packb(
            [message.action, message.body],
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        self.__send_queue.put_nowait(b"\x00" + body)

    def send_data_channel_frame(self, channel_id: int, payload: bytes) -> None:
        """Send a raw DataChannel frame `[0x01][channel_id:u32 LE][bytes]`
        over the WebSocket. Called by `_ProtocolMuxedDataChannel.send`."""
        if self.__send_queue is None:
            return  # client disconnected — the frame is moot
        header = b"\x01" + channel_id.to_bytes(4, "little", signed=False)
        self.__send_queue.put_nowait(header + payload)

    def data_channel_for(self, channel_id: int):
        """Resolve or construct the muxed DataChannel for `channel_id`."""
        from flet.data_channel import _ProtocolMuxedDataChannel

        existing = self._data_channels.get(channel_id)
        if existing is not None:
            return existing
        channel = _ProtocolMuxedDataChannel(channel_id, self)
        self._data_channels[channel_id] = channel
        return channel

    def unregister_data_channel(self, channel_id: int) -> None:
        self._data_channels.pop(channel_id, None)

    def get_upload_url(self, file_name: str, expires: int) -> str:
        """
        Build signed upload URL for a file.

        Args:
            file_name: File name to be uploaded.
            expires: URL lifetime in seconds.

        Returns:
            Signed relative upload URL.

        Raises:
            RuntimeError: If upload endpoint is not configured.
        """

        if not self.__upload_endpoint_path:
            raise RuntimeError("upload_path should be specified to enable uploads")
        return build_upload_url(
            self.__upload_endpoint_path,
            file_name,
            expires,
            self.__secret_key,
        )

    def oauth_authorize(self, attrs: dict[str, Any]):
        """
        Persist OAuth state metadata for a pending authorization flow.

        Args:
            attrs: OAuth attributes payload containing `state` and optional
                completion page data.
        """

        state_id = attrs["state"]
        state = OAuthState(
            session_id=self.__get_unique_session_id(self.__session.id),
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=self.__oauth_state_timeout_seconds),
            complete_page_html=attrs.get("completePageHtml"),
            complete_page_url=attrs.get("completePageUrl"),
        )
        app_manager.store_state(state_id, state)

    def __get_unique_session_id(self, session_id: str) -> str:
        """
        Compose a stable unique session key scoped to page and client identity.

        Args:
            session_id: Session identifier generated for current client.

        Returns:
            Unique session key combining page name, session ID, and client hash.
        """

        ip = self.__client_ip
        if ip in ["127.0.0.1", "::1"]:
            ip = ""
        client_hash = sha1(f"{ip}{self.__client_user_agent}")
        return f"{self.page_name}_{session_id}_{client_hash}"

    def dispose(self):
        """
        Release app-level session reference during teardown.
        """

        logger.info(f"Disposing FletApp: {self.__id}")
        self.__session = None
