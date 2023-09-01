import asyncio
import logging
import shutil
import traceback
from datetime import datetime
from typing import Optional

import flet_fastapi
from flet_core.connection import Connection
from flet_core.page import Page
from flet_fastapi.oauth_state import OAuthState

logger = logging.getLogger(flet_fastapi.__name__)


class FletAppManager:
    """
    Manage application sessions and their lifetime.
    """

    def __init__(self):
        self.__sessions_lock = asyncio.Lock()
        self.__sessions: dict[str, Page] = {}
        self.__evict_sessions_task = None
        self.__states_lock = asyncio.Lock()
        self.__states: dict[str, OAuthState] = {}
        self.__evict_oauth_states_task = None
        self.__temp_dirs = {}

    async def start(self):
        """
        Background task evicting expired app data. Must be called at FastAPI application startup.
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

    async def get_session(self, session_id: str) -> Optional[Page]:
        async with self.__sessions_lock:
            return self.__sessions.get(session_id)

    async def add_session(self, session_id: str, conn: Page):
        async with self.__sessions_lock:
            self.__sessions[session_id] = conn
            logger.info(
                f"New session created ({len(self.__sessions)} total): {session_id}"
            )

    async def reconnect_session(self, session_id: str, conn: Connection):
        logger.info(f"Session reconnected: {session_id}")
        async with self.__sessions_lock:
            if session_id in self.__sessions:
                await self.__sessions[session_id]._connect(conn)

    async def disconnect_session(self, session_id: str, session_timeout_seconds: int):
        logger.info(f"Session disconnected: {session_id}")
        async with self.__sessions_lock:
            if session_id in self.__sessions:
                await self.__sessions[session_id]._disconnect(session_timeout_seconds)

    async def delete_session(self, session_id: str):
        async with self.__sessions_lock:
            page = self.__sessions.pop(session_id, None)
            total = len(self.__sessions)
        if page is not None:
            logger.info(f"Delete session ({total} left): {session_id}")
            try:
                await page._close_async()
            except Exception as e:
                logger.error(
                    f"Error deleting expired session: {e} {traceback.format_exc()}"
                )

    async def store_state(self, state_id: str, state: OAuthState):
        logger.info(f"Store oauth state: {state_id}")
        async with self.__states_lock:
            self.__states[state_id] = state

    async def retrieve_state(self, state_id: str) -> Optional[OAuthState]:
        async with self.__states_lock:
            return self.__states.pop(state_id, None)

    def add_temp_dir(self, temp_dir: str):
        self.__temp_dirs[temp_dir] = True

    async def __evict_expired_sessions(self):
        while True:
            await asyncio.sleep(10)
            session_ids = []
            async with self.__sessions_lock:
                for session_id, page in self.__sessions.items():
                    if page.expires_at and datetime.utcnow() > page.expires_at:
                        session_ids.append(session_id)
            for session_id in session_ids:
                await self.delete_session(session_id)

    async def __evict_expired_oauth_states(self):
        while True:
            await asyncio.sleep(10)
            ids = []
            async with self.__states_lock:
                for id, state in self.__states.items():
                    if state.expires_at and datetime.utcnow() > state.expires_at:
                        ids.append(id)
            for id in ids:
                logger.info(f"Delete expired oauth state: {id}")
                await self.retrieve_state(id)

    def delete_temp_dirs(self):
        for temp_dir in self.__temp_dirs.keys():
            logger.info(f"Deleting temp dir: {temp_dir}")
            shutil.rmtree(temp_dir, ignore_errors=True)


app_manager = FletAppManager()
