import asyncio
import logging
import shutil
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import Optional

import flet_web.fastapi as flet_fastapi
from flet.messaging.connection import Connection
from flet.messaging.session import Session
from flet.pubsub.pubsub_hub import PubSubHub
from flet_web.fastapi.oauth_state import OAuthState

logger = logging.getLogger(flet_fastapi.__name__)


class FletAppManager:
    """
    Manage application sessions and their lifetime.
    """

    def __init__(self):
        self.__sessions: dict[str, Session] = {}
        self.__evict_sessions_task = None
        self.__states: dict[str, OAuthState] = {}
        self.__evict_oauth_states_task = None
        self.__temp_dirs = {}
        self.__executor = ThreadPoolExecutor(thread_name_prefix="flet_fastapi")
        self.__pubsubhubs = {}

    @property
    def executor(self):
        """
        Thread pool executor shared by app sessions and pub/sub hubs.
        """

        return self.__executor

    def get_pubsubhub(
        self, session_handler, loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        """
        Get or create pub/sub hub associated with a session handler.

        Args:
            session_handler: Session entry handler used as cache key.
            loop: Event loop for new hub creation.

        Returns:
            Existing or newly created [`PubSubHub`][flet.pubsub.pubsub_hub.].
        """

        psh = self.__pubsubhubs.get(session_handler, None)
        if psh is None:
            psh = PubSubHub(
                loop=loop or asyncio.get_running_loop(),
                executor=self.__executor,
            )
            self.__pubsubhubs[session_handler] = psh
        return psh

    async def start(self):
        """
        Background task evicting expired app data. Must be called at FastAPI
        application startup.
        """
        if not self.__evict_sessions_task:
            logger.info("Starting up Flet App Manager")
            self.__evict_sessions_task = asyncio.create_task(
                self.__evict_expired_sessions()
            )
            self.__evict_oauth_states_task = asyncio.create_task(
                self.__evict_expired_oauth_states()
            )

    async def shutdown(self):
        """
        Cleanup temporary Flet resources on application shutdown.
        """
        logger.info("Shutting down Flet App Manager")
        self.delete_temp_dirs()
        if self.__evict_sessions_task:
            self.__evict_sessions_task.cancel()
        if self.__evict_oauth_states_task:
            self.__evict_oauth_states_task.cancel()

    async def get_session(self, session_id: str) -> Optional[Session]:
        """
        Retrieve session by unique session ID.

        Args:
            session_id: Unique session key.

        Returns:
            Session instance or `None` if not found.
        """

        return self.__sessions.get(session_id)

    async def add_session(self, session_id: str, session: Session):
        """
        Register a new active session.

        Args:
            session_id: Unique session key.
            session: Session instance to register.
        """

        self.__sessions[session_id] = session
        logger.info(f"New session created ({len(self.__sessions)} total): {session_id}")

    async def reconnect_session(self, session_id: str, conn: Connection):
        """
        Reconnect transport to an existing session.

        Args:
            session_id: Unique session key.
            conn: New active transport connection.

        Raises:
            RuntimeError: If session is expired or not found.
        """

        logger.info(f"Session reconnected: {session_id}")
        if session_id in self.__sessions:
            session = self.__sessions[session_id]
            session.attach_connection(conn)

            # Run connect event handlers asynchronously so websocket receive loop
            # isn't blocked by user handlers (e.g., on_connect invoking _invoke_method).

            async def _connect():
                try:
                    await session.dispatch_connect_event()
                except Exception as e:
                    logger.error(
                        f"Unhandled error reconnecting session {session_id}: {e}",
                        exc_info=True,
                    )
                    try:
                        session.error(str(e))
                    except Exception:
                        logger.error(
                            "Failed to report reconnect error to session",
                            exc_info=True,
                        )

            asyncio.create_task(_connect())
        else:
            raise RuntimeError(f"Session has expired or not found: {session_id}")

    async def disconnect_session(self, session_id: str, session_timeout_seconds: int):
        """
        Mark session disconnected and set expiration timeout.

        Args:
            session_id: Unique session key.
            session_timeout_seconds: Retention period before eviction.
        """

        logger.info(f"Session disconnected: {session_id}")
        if session_id in self.__sessions:
            await self.__sessions[session_id].disconnect(session_timeout_seconds)

    async def delete_session(self, session_id: str):
        """
        Remove session from registry and close it if present.

        Args:
            session_id: Unique session key.
        """

        session = self.__sessions.pop(session_id, None)
        total = len(self.__sessions)
        if session is not None:
            logger.info(f"Delete session ({total} left): {session_id}")
            try:
                session.close()
            except Exception as e:
                logger.error(
                    f"Error deleting expired session: {e} {traceback.format_exc()}"
                )

    def store_state(self, state_id: str, state: OAuthState):
        """
        Store OAuth state payload by state ID.

        Args:
            state_id: OAuth state identifier.
            state: OAuth state payload.
        """

        logger.info(f"Store oauth state: {state_id}")
        self.__states[state_id] = state

    def retrieve_state(self, state_id: str) -> Optional[OAuthState]:
        """
        Retrieve and remove OAuth state payload.

        Args:
            state_id: OAuth state identifier.

        Returns:
            Stored OAuth state, or `None` if missing.
        """

        return self.__states.pop(state_id, None)

    def add_temp_dir(self, temp_dir: str):
        """
        Register temporary directory for cleanup on shutdown.

        Args:
            temp_dir: Path to temporary directory.
        """

        self.__temp_dirs[temp_dir] = True

    async def __evict_expired_sessions(self):
        """
        Periodically evict expired disconnected sessions.
        """

        while True:
            await asyncio.sleep(10)
            session_ids = []
            for session_id, session in self.__sessions.items():
                if (
                    session.expires_at
                    and datetime.now(timezone.utc) > session.expires_at
                ):
                    session_ids.append(session_id)
            for session_id in session_ids:
                await self.delete_session(session_id)

    async def __evict_expired_oauth_states(self):
        """
        Periodically evict expired OAuth authorization states.
        """

        while True:
            await asyncio.sleep(10)
            ids = []
            for id, state in self.__states.items():
                if state.expires_at and datetime.now(timezone.utc) > state.expires_at:
                    ids.append(id)
            for id in ids:
                logger.info(f"Delete expired oauth state: {id}")
                self.retrieve_state(id)

    def delete_temp_dirs(self):
        """
        Delete all registered temporary directories.
        """

        for temp_dir in self.__temp_dirs:
            logger.info(f"Deleting temp dir: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)


app_manager = FletAppManager()
