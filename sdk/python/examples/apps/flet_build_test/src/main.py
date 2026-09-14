import sys

import flet_code_editor  # noqa: F401
import flet_spinkit  # noqa: F401
import numpy
import PIL
from modules.utils import greet

import flet as ft
import flet.version as fv
import flet_ads  # noqa: F401
import flet_audio  # noqa: F401
import flet_audio_recorder  # noqa: F401
import flet_charts  # noqa: F401
import flet_color_pickers  # noqa: F401
import flet_datatable2  # noqa: F401
import flet_flashlight  # noqa: F401
import flet_geolocator  # noqa: F401
import flet_lottie  # noqa: F401
import flet_map  # noqa: F401
import flet_permission_handler  # noqa: F401
import flet_rive  # noqa: F401
import flet_secure_storage  # noqa: F401
import flet_video  # noqa: F401
import flet_webview as fwv

# TEMP(webview): this app is temporarily a WebView test harness so that the
# Windows and Linux builds produced by `flet-build-test.yml` can be downloaded
# and exercised by hand. Restore the original single-greeting body before merge.

START_URL = "https://flet.dev"


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.SYSTEM

    log = ft.ListView(expand=1, spacing=2, auto_scroll=True)
    # Scroll and progress fire at frame rate; appending them would evict every
    # other line from the 200-entry log within seconds, so they update in place.
    status = ft.Text("", size=11, font_family="monospace")

    def write(message: str):
        log.controls.append(ft.Text(message, size=11, font_family="monospace"))
        if len(log.controls) > 200:
            del log.controls[: len(log.controls) - 200]
        page.update()

    def set_status(message: str):
        status.value = message
        page.update()

    webview = fwv.WebView(
        url=START_URL,
        expand=True,
        on_page_started=lambda e: write(f"page_started: {e.data}"),
        on_page_ended=lambda e: write(f"page_ended: {e.data}"),
        on_progress=lambda e: set_status(f"progress: {e.data}"),
        on_url_change=lambda e: write(f"url_change: {e.data}"),
        on_web_resource_error=lambda e: write(f"web_resource_error: {e.data}"),
        on_console_message=lambda e: write(
            f"console_message[{e.severity_level.name}]: {e.message}"
        ),
        on_scroll=lambda e: set_status(f"scroll: x={e.x} y={e.y}"),
        on_javascript_alert_dialog=lambda e: write(f"js_alert: {e.message}"),
    )

    async def call(label, coro):
        """Runs a WebView call, reporting the result or the failure into the log."""
        try:
            result = await coro
            # Several methods return the control itself for chaining; logging
            # that repr would flood the panel with an 800-char line.
            if result is None or isinstance(result, ft.BaseControl):
                write(f"{label}: ok")
            else:
                write(f"{label} -> {result!r}")
        except ft.FletUnsupportedPlatformException as e:
            write(f"{label}: UNSUPPORTED ({e})")
        except Exception as e:
            write(f"{label}: FAILED {type(e).__name__}: {e}")

    def action(label, make_coro):
        """
        Builds a zero-argument async click handler around a `WebView` call.

        A plain `lambda` cannot be used: a sync handler's return value is
        discarded, so the coroutine it built would never be awaited.
        """

        async def handler():
            await call(label, make_coro())

        return handler

    url_field = ft.TextField(
        value=START_URL,
        label="URL",
        dense=True,
        expand=True,
        on_submit=action("load_request", lambda: webview.load_request(url_field.value)),
    )

    zoom_enabled = True
    js_enabled = True

    async def toggle_zoom():
        nonlocal zoom_enabled
        zoom_enabled = not zoom_enabled
        await call(
            f"{'enable' if zoom_enabled else 'disable'}_zoom",
            webview.enable_zoom() if zoom_enabled else webview.disable_zoom(),
        )

    async def toggle_js():
        nonlocal js_enabled
        js_enabled = not js_enabled
        mode = (
            fwv.JavaScriptMode.UNRESTRICTED
            if js_enabled
            else fwv.JavaScriptMode.DISABLED
        )
        await call(
            f"set_javascript_mode({mode.name})", webview.set_javascript_mode(mode)
        )

    async def show_debug():
        """
        Writes the debug info into the log rather than a dialog.

        On Linux the WebView is a native GTK child that Flutter cannot draw over,
        so an `AlertDialog` would be painted underneath it and be unreachable --
        and this is the harness's only view of which platform code path is live.
        """
        write(f"platform: {page.platform} | web: {page.web}")
        write(f"flet: v{ft.__version__} | flutter: v{fv.flutter_version}")
        write(f"python: v{sys.version.split()[0]} | numpy: v{numpy.__version__}")
        write(f"pillow: v{PIL.__version__} | {greet('Flet')}")

    buttons = [
        ("Go", action("load_request", lambda: webview.load_request(url_field.value))),
        ("Back", action("go_back", webview.go_back)),
        ("Forward", action("go_forward", webview.go_forward)),
        ("Reload", action("reload", webview.reload)),
        ("Title", action("get_title", webview.get_title)),
        ("URL", action("get_current_url", webview.get_current_url)),
        ("UA", action("get_user_agent", webview.get_user_agent)),
        ("CanBack", action("can_go_back", webview.can_go_back)),
        # `run_javascript` returns nothing, so the result comes back through
        # `on_console_message` -- a genuine Python -> JS -> Python round trip.
        (
            "JS",
            action(
                "run_javascript",
                lambda: webview.run_javascript(
                    "console.log('js ok: ' + document.title)"
                ),
            ),
        ),
        ("Scroll", action("scroll_to", lambda: webview.scroll_to(0, 400))),
        ("ClearCache", action("clear_cache", webview.clear_cache)),
        ("ClearStorage", action("clear_local_storage", webview.clear_local_storage)),
        ("Zoom", toggle_zoom),
        # Exercises the alert path: on Linux a registered handler suppresses the
        # native dialog and fires `on_javascript_alert_dialog`; on Windows Edge
        # WebView2 shows its own dialog and the event never arrives.
        (
            "Alert",
            action(
                "run_javascript(alert)",
                lambda: webview.run_javascript("alert('alert from JS')"),
            ),
        ),
        ("JSMode", toggle_js),
        ("Debug", show_debug),
        (
            "LoadHTML",
            action(
                "load_html",
                lambda: webview.load_html(
                    "<h1>local html</h1><script>console.log('inline js')</script>"
                ),
            ),
        ),
    ]

    page.appbar = ft.AppBar(
        title=ft.Text("Flet Build Test - WebView"),
        actions=[
            ft.Container(
                content=ft.Text(f"v{ft.__version__}", weight=ft.FontWeight.BOLD),
                padding=ft.Padding.only(right=15),
            )
        ],
    )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.INFO,
        bgcolor=ft.Colors.BLUE,
        on_click=lambda: page.show_dialog(
            ft.AlertDialog(
                title="Debug Info",
                scrollable=True,
                content=ft.Column(
                    controls=[
                        ft.Text(greet("Flet")),
                        ft.Text(f"Python: v{sys.version}"),
                        ft.Text(f"Flet: v{ft.__version__}"),
                        ft.Text(f"Flutter: v{fv.flutter_version}"),
                        ft.Text(f"Platform: {page.platform}"),
                        ft.Text(f"Numpy: v{numpy.__version__}"),
                        ft.Text(f"Pillow: v{PIL.__version__}"),
                        ft.Text(f"sys.path: {sys.path}"),
                    ]
                ),
            )
        ),
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(controls=[url_field]),
                    ft.Row(
                        wrap=True,
                        spacing=4,
                        run_spacing=4,
                        controls=[
                            ft.Button(content=label, on_click=handler)
                            for label, handler in buttons
                        ],
                    ),
                    ft.Container(content=webview, expand=3),
                    ft.Divider(height=1),
                    status,
                    ft.Container(content=log, expand=1),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
