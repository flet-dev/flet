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
        return self.__executor

    def get_pubsubhub(
        self, session_handler, loop: Optional[asyncio.AbstractEventLoop] = None
    ):
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
        return self.__sessions.get(session_id)

    async def add_session(self, session_id: str, session: Session):
        self.__sessions[session_id] = session
        logger.info(f"New session created ({len(self.__sessions)} total): {session_id}")

    async def reconnect_session(self, session_id: str, conn: Connection):
        logger.info(f"Session reconnected: {session_id}")
        if session_id in self.__sessions:
            session = self.__sessions[session_id]
            await session.connect(conn)
        else:
            raise RuntimeError(f"Session has expired or not found: {session_id}")

    async def disconnect_session(self, session_id: str, session_timeout_seconds: int):
        logger.info(f"Session disconnected: {session_id}")
        if session_id in self.__sessions:
            await self.__sessions[session_id].disconnect(session_timeout_seconds)

    async def delete_session(self, session_id: str):
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
        logger.info(f"Store oauth state: {state_id}")
        self.__states[state_id] = state

    def retrieve_state(self, state_id: str) -> Optional[OAuthState]:
        return self.__states.pop(state_id, None)

    def add_temp_dir(self, temp_dir: str):
        self.__temp_dirs[temp_dir] = True

    async def __evict_expired_sessions(self):
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
        for temp_dir in self.__temp_dirs:
            logger.info(f"Deleting temp dir: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)


app_manager = FletAppManager()
