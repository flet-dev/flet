import logging
import traceback

import flet_js
from flet.pyodide_connection import PyodideConnection
from flet_core.event import Event
from flet_core.page import Page
from flet_core.utils import is_coroutine

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

WEB_BROWSER = "web_browser"
FLET_APP = "flet_app"
FLET_APP_HIDDEN = "flet_app_hidden"


def app(
    target,
    name="",
    host=None,
    port=0,
    view=None,
    assets_dir=None,
    upload_dir=None,
    web_renderer=None,
    route_url_strategy=None,
    auth_token=None,
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
        route_url_strategy=route_url_strategy,
        auth_token=auth_token,
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
    route_url_strategy=None,
    auth_token=None,
):
    async def on_event(e):
        if e.sessionID in conn.sessions:
            await conn.sessions[e.sessionID].on_event_async(
                Event(e.eventTarget, e.eventName, e.eventData)
            )
            if e.eventTarget == "page" and e.eventName == "close":
                logging.info(f"Session closed: {e.sessionID}")
                del conn.sessions[e.sessionID]

    async def on_session_created(session_data):
        page = Page(conn, session_data.sessionID)
        await page.fetch_page_details_async()
        conn.sessions[session_data.sessionID] = page
        logging.info(f"Session started: {session_data.sessionID}")
        try:
            assert target is not None
            if is_coroutine(target):
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
