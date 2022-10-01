"""Test echo text."""

import os
from pathlib import Path

import pyautogui as pag
import pytest
from beartype import beartype

import flet
from flet.protocol import Command
from flet.echo_text import EchoText


def test_echo_text_add():
    et = EchoText(message="Hello world")
    assert et._build_add_commands() == [
        Command(0, None, values=["echotext"], attrs={"message": "Hello world"})
    ]
    return


def test_echo_text_INTE(run_target):
    title = "EchoText test"

    @beartype
    def main_func(page: flet.Page):
        page.title = title
        et = EchoText(message="Hello world")
        page.add(et)
        return
    page: flet.Page = run_target(target=main_func)
    # NOTE: may need a wait here to ensure window is active before continuing
    pag.press("tab")
    pag.hotkey("ctrl", "a")
    pag.write("hi ")
    et = page.controls[0]
    assert et.message == "hi "
    assert et.echoed is None
    pag.write("there")
    pag.press(["tab", "space"])
    assert et.echoed == 'I got "hi there"...'
    return


@pytest.fixture
def run_target():
    holder = {}

    def _run(cleanup=False, **kwds):
        app(holder=holder, **kwds)
        page = holder["page"]

        if cleanup:
            page.controls.clear()
            page.update()
        return page
    yield _run
    holder["conn"].close()
    holder["fvp"].kill()
    return


def app(
    holder=None,
    name="",
    host=None,
    port=0,
    target=None,
    permissions=None,
    view: flet.AppViewer = flet.FLET_APP,
    assets_dir=None,
    upload_dir=None,
    web_renderer="canvaskit",
    route_url_strategy="hash",
):

    if target is None:
        raise Exception("target argument is not specified")

    conn = flet.flet._connect_internal(
        page_name=name,
        host=host,
        port=port,
        is_app=True,
        permissions=permissions,
        session_handler=target,
        assets_dir=assets_dir,
        upload_dir=upload_dir,
        web_renderer=web_renderer,
        route_url_strategy=route_url_strategy,
    )

    url_prefix = os.getenv("FLET_DISPLAY_URL_PREFIX")
    if url_prefix is not None:
        print(url_prefix, conn.page_url)
    else:
        print(f"App URL: {conn.page_url}")

    import time
    fvp = open_flet_view(
        conn.page_url,
        False,
        f"/tmp/local-flet-{flet.version.version}"
    )
    print("Waiting for session to be created...")

    while not conn.sessions:
        time.sleep(0.3)
    page = list(conn.sessions.values())[0]

    if holder is not None:
        holder.update({
            "conn": conn,
            "fvp": fvp,
            "page": page,
        })
    return conn, page, fvp


def open_flet_view(page_url, hidden, viewer_path=None):
    import subprocess as sp

    args = []

    if viewer_path and Path(viewer_path).exists():
        viewer_path = Path(viewer_path)

    else:
        raise OSError(f'unable to find viewer at "{viewer_path}"; try compiling and/or copying it there')
    app_path = viewer_path / "flet"
    args = [str(app_path), page_url]
    flet_env = {**os.environ}

    if hidden:
        flet_env["FLET_HIDE_WINDOW_ON_START"] = "true"
    return sp.Popen(args, env=flet_env)
