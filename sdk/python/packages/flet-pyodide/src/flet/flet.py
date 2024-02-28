import asyncio
import logging
import traceback

import flet
import flet_js
from flet.pyodide_connection import PyodideConnection
from flet_core.event import Event
from flet_core.page import Page

logger = logging.getLogger(flet.__name__)


def app(
    target,
    name="",
    host=None,
    port=0,
    view=None,
    assets_dir=None,
    upload_dir=None,
    web_renderer=None,
    use_color_emoji=False,
    route_url_strategy=None,
):
    app_async(
        target=target,
        name=name,
        host=host,
        port=port,
        view=view,
        assets_dir=assets_dir,
        upload_dir=upload_dir,
        web_renderer=web_renderer,
        use_color_emoji=use_color_emoji,
        route_url_strategy=route_url_strategy,
    )


def app_async(
    target,
    name="",
    host=None,
    port=0,
    view=None,
    assets_dir=None,
    upload_dir=None,
    web_renderer=None,
    use_color_emoji=False,
    route_url_strategy=None,
):
    async def on_event(e):
        if e.sessionID in conn.sessions:
            await conn.sessions[e.sessionID].on_event_async(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logger.info(f"Session closed: {e.sessionID}")
                del conn.sessions[e.sessionID]

    async def on_session_created(session_data):
        page = Page(conn, session_data.sessionID, loop=asyncio.get_running_loop())
        await page.fetch_page_details_async()
        conn.sessions[session_data.sessionID] = page
        logger.info("App session started")
        try:
            assert target is not None
            if asyncio.iscoroutinefunction(target):
                await target(page)
            else:
                target(page)
        except Exception as e:
            print(
                f"Unhandled error processing page session {page.session_id}:",
                traceback.format_exc(),
            )
            await page.error_async(
                f"There was an error while processing your request: {e}"
            )

    conn = PyodideConnection(
        on_event=on_event,
        on_session_created=on_session_created,
    )
