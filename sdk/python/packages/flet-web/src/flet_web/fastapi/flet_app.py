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
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop,
        executor: ThreadPoolExecutor,
        main,
        before_main,
        session_timeout_seconds: int = DEFAULT_FLET_SESSION_TIMEOUT,
        oauth_state_timeout_seconds: int = DEFAULT_FLET_OAUTH_STATE_TIMEOUT,
        upload_endpoint_path: Optional[str] = None,
        secret_key: Optional[str] = None,
    ):
        """
        Handle Flet app WebSocket connections.

        Parameters:

        * `session_handler` (Coroutine) - application entry point - an async method
           called for newly connected user. Handler coroutine must have
           1 parameter: `page` - `Page` instance.
        * `session_timeout_seconds` (int, optional) - session lifetime, in seconds,
           after user disconnected.
        * `oauth_state_timeout_seconds` (int, optional) - OAuth state lifetime,
           in seconds, which is a maximum allowed time between starting OAuth flow
           and redirecting to OAuth callback URL.
        * `upload_endpoint_path` (str, optional) - absolute URL of upload endpoint,
           e.g. `/upload`.
        * `secret_key` (str, optional) - secret key to sign upload requests.
        """
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
        assert self.__session
        logger.info(f"Start session: {self.__session.id}")
        try:
            assert self.__main is not None
            _context_page.set(self.__session.page)
            context.reset_auto_update()

            if asyncio.iscoroutinefunction(self.__main):
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
        transport_log.debug(f"_on_message: {action} {body}")
        task = None
        if action == ClientAction.REGISTER_CLIENT:
            req = RegisterClientRequestBody(**body)

            new_session = False

            # try to retrieve existing session
            if req.session_id:
                self.__session = await app_manager.get_session(
                    self.__get_unique_session_id(req.session_id)
                )

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
                    if asyncio.iscoroutinefunction(self.__before_main):
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
        transport_log.debug(f"send_message: {message}")
        m = msgpack.packb(
            [message.action, message.body],
            default=configure_encode_object_for_msgpack(BaseControl),
        )
        self.__send_queue.put_nowait(m)

    def get_upload_url(self, file_name: str, expires: int) -> str:
        if not self.__upload_endpoint_path:
            raise RuntimeError("upload_path should be specified to enable uploads")
        return build_upload_url(
            self.__upload_endpoint_path,
            file_name,
            expires,
            self.__secret_key,
        )

    def oauth_authorize(self, attrs: dict[str, Any]):
        state_id = attrs["state"]
        state = OAuthState(
            session_id=self.__get_unique_session_id(self.__session.id),
            expires_at=datetime.now(timezone.utc)
            + timedelta(seconds=self.__oauth_state_timeout_seconds),
            complete_page_html=attrs.get("completePageHtml"),
            complete_page_url=attrs.get("completePageUrl"),
        )
        app_manager.store_state(state_id, state)

    def __get_unique_session_id(self, session_id: str):
        ip = self.__client_ip
        if ip in ["127.0.0.1", "::1"]:
            ip = ""
        client_hash = sha1(f"{ip}{self.__client_user_agent}")
        return f"{self.page_name}_{session_id}_{client_hash}"

    def dispose(self):
        logger.info(f"Disposing FletApp: {self.__id}")
        self.__session = None
