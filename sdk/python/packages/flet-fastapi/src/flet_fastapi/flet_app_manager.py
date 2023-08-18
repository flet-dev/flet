import asyncio
import logging
from datetime import datetime
from typing import Optional

import flet
from flet_core.connection import Connection
from flet_core.page import Page

logger = logging.getLogger(flet.__name__)


class FletAppManager:
    def __init__(self):
        self.__lock = asyncio.Lock()
        self.__sessions: dict[str, Page] = {}

    async def get_session(self, session_id: str) -> Optional[Page]:
        async with self.__lock:
            return self.__sessions.get(session_id)

    async def add_session(self, session_id: str, conn: Page):
        logger.info(f"New session created: {session_id}")
        async with self.__lock:
            self.__sessions[session_id] = conn

    async def reconnect_session(self, session_id: str, conn: Connection):
        logger.info(f"Session reconnected: {session_id}")
        async with self.__lock:
            if session_id in self.__sessions:
                await self.__sessions[session_id]._connect(conn)

    async def disconnect_session(
        self, session_id: str, session_expires_in_seconds: int
    ):
        logger.info(f"Session disconnected: {session_id}")
        if session_id in self.__sessions:
            await self.__sessions[session_id]._disconnect(session_expires_in_seconds)

    async def delete_session(self, session_id: str):
        async with self.__lock:
            await self.__delete_session(session_id)

    async def __delete_session(self, session_id: str):
        logger.info(f"Delete session: {session_id}")
        page = self.__sessions.pop(session_id, None)
        if page is not None:
            await page._close_async()

    async def start(self):
        logger.info("Starting up Flet App Manager")
        asyncio.create_task(self.__evict_expired_sessions())
        asyncio.create_task(self.__evict_expired_oauth_states())

    async def shutdown(self):
        logger.info("Shutting down Flet App Manager")
        # TODO

    async def __evict_expired_sessions(self):
        while True:
            await asyncio.sleep(10)
            session_ids = []
            async with self.__lock:
                for session_id, page in self.__sessions.items():
                    if page.expires_at and datetime.utcnow() > page.expires_at:
                        session_ids.append(session_id)
            for session_id in session_ids:
                await self.__delete_session(session_id)

    async def __evict_expired_oauth_states(self):
        while True:
            await asyncio.sleep(10)
            # TODO


flet_app_manager = FletAppManager()
