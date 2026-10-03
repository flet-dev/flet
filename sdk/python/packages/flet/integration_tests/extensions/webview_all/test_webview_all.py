import pytest

import flet as ft
import flet.testing as ftt
import flet_webview_all as fwa


@pytest.mark.asyncio(loop_scope="module")
async def test_webview_all_renders_html(flet_app: ftt.FletTestApp):
    flet_app.page.clean()
    flet_app.page.add(
        fwa.WebViewAll(
            html="<!doctype html><html><body><h1>Flet</h1></body></html>",
            height=120,
            key="webview-all",
        )
    )
    await flet_app.tester.pump(duration=ft.Duration(milliseconds=500))
    assert (await flet_app.tester.find_by_key("webview-all")).count == 1
