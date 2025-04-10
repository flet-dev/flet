import asyncio
import gc
import logging
import os
import traceback
import weakref
from typing import Any, Optional

import flet_web.fastapi as flet_fastapi
import msgpack
from fastapi import WebSocket, WebSocketDisconnect
from flet.controls.page import PageDisconnectedException
from flet.messaging.connection import Connection
from flet.messaging.protocol import (
    ClientAction,
    ClientMessage,
    ControlEventBody,
    InvokeMethodResponseBody,
    RegisterClientRequestBody,
    RegisterClientResponseBody,
    UpdateControlPropsBody,
    decode_ext_from_msgpack,
    encode_object_for_msgpack,
)
from flet.messaging.session import Session
from flet.utils import random_string, sha1
from flet_web.fastapi.flet_app_manager import app_manager
from flet_web.fastapi.oauth_state import OAuthState
from flet_web.uploads import build_upload_url

logger = logging.getLogger(flet_fastapi.__name__)

DEFAULT_FLET_SESSION_TIMEOUT = 3600
DEFAULT_FLET_OAUTH_STATE_TIMEOUT = 600


class FletApp(Connection):
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        session_handler,
        session_timeout_seconds: int = DEFAULT_FLET_SESSION_TIMEOUT,
        oauth_state_timeout_seconds: int = DEFAULT_FLET_OAUTH_STATE_TIMEOUT,
        upload_endpoint_path: Optional[str] = None,
        secret_key: Optional[str] = None,
    ):
        """
        Handle Flet app WebSocket connections.

        Parameters:

        * `session_handler` (Coroutine) - application entry point - an async method called for newly connected user. Handler coroutine must have 1 parameter: `page` - `Page` instance.
        * `session_timeout_seconds` (int, optional) - session lifetime, in seconds, after user disconnected.
        * `oauth_state_timeout_seconds` (int, optional) - OAuth state lifetime, in seconds, which is a maximum allowed time between starting OAuth flow and redirecting to OAuth callback URL.
        * `upload_endpoint_path` (str, optional) - absolute URL of upload endpoint, e.g. `/upload`.
        * `secret_key` (str, optional) - secret key to sign upload requests.
        """
        super().__init__()
        self.__id = random_string(8)
        logger.info(f"New FletApp: {self.__id}")

        self.__session = None
        self.__loop = loop
        self.__session_handler = session_handler
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

        app_id = self.__id
        weakref.finalize(
            self, lambda: logger.debug(f"FletApp was garbage collected: {app_id}")
        )

    async def handle(self, websocket: WebSocket):
        """
        Handle WebSocket connection.

        Parameters:

        * `websocket` (WebSocket) - Websocket instance.
        """
        self.__websocket = websocket

        self.client_ip = (
            self.__websocket.client.host if self.__websocket.client else ""
        ).split(":")[0]
        self.client_user_agent = (
            self.__websocket.headers["user-agent"]
            if "user-agent" in self.__websocket.headers
            else ""
        )

        self.pubsubhub = app_manager.get_pubsubhub(
            self.__session_handler, loop=self.__loop
        )
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
        assert self.__session
        logger.info(f"Start session: {self.__session.id}")
        try:
            assert self.__session_handler is not None
            if asyncio.iscoroutinefunction(self.__session_handler):
                await self.__session_handler(self.__session.page)
            else:
                self.__session_handler(self.__session.page)
            self.__session.auto_update(self.__session.page)
        except PageDisconnectedException:
            logger.debug(
                f"Session handler attempted to update disconnected page: {self.__session.id}"
            )
        except BrokenPipeError:
            logger.info(f"Session handler terminated: {self.__session.id}")
        except Exception as e:
            print(
                f"Unhandled error processing page session {self.__session.id}:",
                traceback.format_exc(),
            )
            assert self.__session
            self.__session.error(
                f"There was an error while processing your request: {e}"
            )

    async def __send_loop(self):
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
        assert self.__websocket
        try:
            while True:
                data = await self.__websocket.receive_bytes()
                await self.__on_message(
                    msgpack.unpackb(data, ext_hook=decode_ext_from_msgpack)
                )
        except Exception as e:
            if not isinstance(e, WebSocketDisconnect):
                logger.warning(f"Receive loop error: {e}", exc_info=True)
            if self.__session:
                # terminate __send_loop
                await self.__send_queue.put(None)

    async def __on_message(self, data: Any):
        action = ClientAction(data[0])
        body = data[1]
        print(f"_on_message: {action} {body}")
        task = None
        if action == ClientAction.REGISTER_CLIENT:
            req = RegisterClientRequestBody(**body)

            new_session = False

            # try to retrieve existing session
            if req.session_id:
                self.__session = await app_manager.get_session(
                    self.__get_unique_session_id(req.session_id)
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

            original_route = self.__session.page.route

            # apply page patch
            self.__session.apply_page_patch(req.page)

            # register response
            self.send_message(
                ClientMessage(
                    ClientAction.REGISTER_CLIENT,
                    RegisterClientResponseBody(
                        session_id=self.__session.id,
                        page_patch=self.__session.get_page_patch(),
                        error="",
                    ),
                )
            )

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
                    self.__session.page.go(self.__session.page.route)

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
            raise Exception(f'Unknown message "{action}": {body}')

        if task:
            self.__running_tasks.add(task)
            task.add_done_callback(self.__running_tasks.discard)

    def send_message(self, message: ClientMessage):
        # print(f"Sending: {message}")
        m = msgpack.packb(
            [message.action, message.body], default=encode_object_for_msgpack
        )
        self.__send_queue.put_nowait(m)

    # def _process_get_upload_url_command(self, attrs):
    #     assert len(attrs) == 2, '"getUploadUrl" command has wrong number of attrs'
    #     assert (
    #         self.__upload_endpoint_path
    #     ), "upload_path should be specified to enable uploads"
    #     return (
    #         build_upload_url(
    #             self.__upload_endpoint_path,
    #             attrs["file"],
    #             int(attrs["expires"]),
    #             self.__secret_key,
    #         ),
    #         None,
    #     )

    # def __process_oauth_authorize_command(self, attrs: Dict[str, Any]):
    #     state_id = attrs["state"]
    #     state = OAuthState(
    #         session_id=self.__get_unique_session_id(self._client_details.sessionId),
    #         expires_at=datetime.now(timezone.utc)
    #         + timedelta(seconds=self.__oauth_state_timeout_seconds),
    #         complete_page_html=attrs.get("completePageHtml", None),
    #         complete_page_url=attrs.get("completePageUrl", None),
    #     )
    #     app_manager.store_state(state_id, state)
    #     return (
    #         "",
    #         None,
    #     )

    def __get_unique_session_id(self, session_id: str):
        client_hash = sha1(f"{self.client_ip}{self.client_user_agent}")
        return f"{self.page_name}_{session_id}_{client_hash}"

    def dispose(self):
        logger.info(f"Disposing FletApp: {self.__id}")
        self.__session = None
