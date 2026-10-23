"""Example app for flet-notifications — every API, platform-aware.

House example pattern (adaptive AppBar, scrollable page, activity terminal)
plus capability gating: only the features this platform can actually run are
enabled; the rest are listed with the platforms that support them, because
developers should see everything that is possible.
"""

import asyncio
import contextlib
import datetime

import flet as ft
from flet_notifications import (
    AndroidBigTextStyle,
    AndroidGroup,
    AndroidInboxStyle,
    AndroidNotificationCategory,
    AndroidOptions,
    AndroidProgress,
    AndroidVisibility,
    DarwinOptions,
    DateTimeComponents,
    LocalNotifications,
    NotificationAction,
    NotificationActionInput,
    NotificationChannel,
    NotificationOptions,
    RepeatInterval,
)

# Activity terminal — house pattern (Courier New, #A6E22E on #0D0D0D).
TERMINAL_BG = "#0D0D0D"
TERMINAL_TEXT = "#A6E22E"

# Capability model: which features each platform supports. Anything absent
# here is available everywhere.
# Android TV runs the Android plugin (Flutter dispatches the Android
# implementation), so it gets the full Android feature set.
ANDROID_ONLY = {ft.PagePlatform.ANDROID, ft.PagePlatform.ANDROID_TV}
SCHEDULED = {
    ft.PagePlatform.ANDROID,
    ft.PagePlatform.ANDROID_TV,
    ft.PagePlatform.IOS,
    ft.PagePlatform.MACOS,
}
REQUIRED = {
    "schedule_oneshot": SCHEDULED,  # Linux/Web have no OS scheduler
    "schedule_recurring": SCHEDULED,
    "periodic": SCHEDULED,
    "cancel_pending": SCHEDULED,
    "exact_alarms": ANDROID_ONLY,  # AlarmManager alarms on Android
    "channels": ANDROID_ONLY,  # Notification channels are Android 8+
    "channel_groups": ANDROID_ONLY,
    "foreground": ANDROID_ONLY,  # Android foreground service
    "fullscreen_intent": ANDROID_ONLY,  # Android 14+ full-screen intents
    "dnd": ANDROID_ONLY,  # notification policy access
}
REASON = {
    "schedule_oneshot": "Android/iOS/macOS only — Linux/Web have no OS scheduler",
    "schedule_recurring": "Android/iOS/macOS only — Linux/Web have no OS scheduler",
    "periodic": "Android/iOS/macOS only — Linux/Web have no OS scheduler",
    "cancel_pending": "Android/iOS/macOS only — Linux/Web have no OS scheduler",
    "exact_alarms": "Android only",
    "channels": "Android only (channels are an Android 8+ concept)",
    "channel_groups": "Android only",
    "foreground": "Android only",
    "fullscreen_intent": "Android only (14+)",
    "dnd": "Android only",
}


def main(page: ft.Page):
    page.appbar = ft.AppBar(adaptive=True, title="flet-notifications Example")
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 16

    notifications = LocalNotifications()

    log_text = ft.Text(
        value="",
        font_family="Courier New",
        size=12,
        color=TERMINAL_TEXT,
        selectable=True,
    )
    log_col = ft.Column(controls=[log_text], scroll=ft.ScrollMode.AUTO, expand=True)
    log_terminal = ft.Container(
        content=log_col,
        bgcolor=TERMINAL_BG,
        padding=12,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ft.Colors.WHITE)),
        border_radius=8,
        height=320,
    )

    def log_line(message: str):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        log_text.value = (
            f"{log_text.value}\n[{ts}] {message}"
            if log_text.value
            else f"[{ts}] {message}"
        )
        page.update(log_text)

        async def _scroll_to_end():
            await asyncio.sleep(0.05)
            with contextlib.suppress(Exception):
                await log_col.scroll_to(offset=-1)  # offset=-1: jump to newest

        page.run_task(_scroll_to_end)

    # Plain `flet run` uses the prebuilt client without this extension's
    # Dart half; invokes time out. Reported separately from calls this
    # platform genuinely doesn't implement.
    missing_backend = {"warned": False}

    def warn_no_backend(method: str):
        if missing_backend["warned"]:
            return
        missing_backend["warned"] = True
        log_line(f"{method}: no notification backend in this runner.")
        log_line("Run a built app instead: a release artifact, or")
        log_line("  uv run flet build windows|macos|linux|apk")

    def report_error(method: str, exc: Exception):
        """Classify: unsupported on this platform vs no backend at all."""
        if getattr(exc, "code", "") == "unsupported_platform":
            msg = getattr(exc, "message", "") or "unsupported"
            log_line(f"{method}: not available on this platform ({msg})")
            return
        warn_no_backend(method)

    def guarded(coro, method: str):
        async def _run():
            try:
                await coro
            except Exception as exc:  # noqa: BLE001 - classify and degrade
                report_error(method, exc)

        page.run_task(_run)

    def guarded_async(make_coro, method: str):
        """For handlers that build their coroutine inside a task."""

        async def _run():
            try:
                await make_coro()
            except Exception as exc:  # noqa: BLE001
                report_error(method, exc)

        page.run_task(_run)

    # ── Events ──
    notifications.on_tap = lambda e: log_line(f"tap: id={e.id} payload={e.payload!r}")
    notifications.on_action = lambda e: log_line(
        f"action: {e.action_id!r} payload={e.payload!r} input={e.input!r}"
    )
    notifications.on_dismissed = lambda e: log_line(f"dismissed: id={e.id}")

    # ── Handlers ──
    def show_plain(e):
        guarded(
            notifications.show(
                id=1, title="Hello", body="A plain notification.", payload="plain"
            ),
            "show",
        )

    def show_actions(e):
        guarded(
            notifications.show(
                id=2,
                title="Action buttons",
                body="Tap a button — the reply field returns text.",
                actions=[
                    NotificationAction(id="open", title="Open"),
                    NotificationAction(
                        id="reply",
                        title="Reply",
                        foreground=False,
                        input=NotificationActionInput(label="Type a reply"),
                    ),
                ],
            ),
            "show",
        )

    def show_big_text(e):
        guarded(
            notifications.show(
                id=5,
                title="Long read",
                body="Tap to expand.",
                options=NotificationOptions(
                    android=AndroidOptions(
                        style=AndroidBigTextStyle(
                            big_text="The quick brown fox jumps over the lazy dog. " * 3
                        )
                    )
                ),
            ),
            "show",
        )

    def show_inbox(e):
        guarded(
            notifications.show(
                id=6,
                title="Inbox",
                body="3 unread.",
                options=NotificationOptions(
                    android=AndroidOptions(
                        style=AndroidInboxStyle(lines=["First", "Second", "Third"])
                    )
                ),
            ),
            "show",
        )

    def show_progress(e):
        guarded(
            notifications.show(
                id=7,
                title="Downloading",
                body="25%",
                options=NotificationOptions(
                    android=AndroidOptions(progress=AndroidProgress(value=25))
                ),
            ),
            "show",
        )

    def show_grouped(e):
        guarded(
            notifications.show(
                id=8,
                title="Summary",
                body="Group summary.",
                options=NotificationOptions(
                    android=AndroidOptions(
                        group=AndroidGroup(key="demo_group", summary=True)
                    )
                ),
            ),
            "show",
        )

    def show_options(e):
        guarded(
            notifications.show(
                id=9,
                title="Silent alarm",
                body="Full platform options.",
                options=NotificationOptions(
                    android=AndroidOptions(
                        silent=True,
                        category=AndroidNotificationCategory.ALARM,
                        visibility=AndroidVisibility.PUBLIC,
                    ),
                    ios=DarwinOptions(interruption_level="passive"),
                ),
            ),
            "show",
        )

    def request_permissions(e):
        async def _req():
            granted = await notifications.request_permissions()
            log_line(f"permissions granted: {granted}")

        guarded_async(_req, "request_permissions")

    def schedule_delayed(e):
        guarded(
            notifications.schedule(
                id=3,
                when=datetime.timedelta(seconds=10),
                title="Delayed",
                body="10 seconds after you tapped.",
            ),
            "schedule",
        )

    def schedule_daily(e):
        guarded(
            notifications.schedule(
                id=4,
                when=(datetime.datetime.now() + datetime.timedelta(days=1)).replace(
                    hour=8, minute=30, second=0, microsecond=0
                ),
                title="Daily reminder",
                body="Every day at 08:30.",
                match_components=DateTimeComponents.TIME,
            ),
            "schedule",
        )

    def schedule_hourly(e):
        guarded(
            notifications.periodically_show(
                id=10,
                repeat_interval=RepeatInterval.HOURLY,
                title="Hourly",
                body="An hourly notification.",
            ),
            "periodically_show",
        )

    def list_pending(e):
        async def _list():
            pending = await notifications.get_pending_notifications()
            log_line(f"pending: {[p.id for p in pending]}")

        guarded_async(_list, "get_pending_notifications")

    def cancel_pending(e):
        guarded(notifications.cancel_pending(), "cancel_pending")

    def check_exact(e):
        async def _check():
            allowed = await notifications.can_schedule_exact_notifications()
            log_line(f"exact alarms allowed: {allowed}")
            if not allowed:
                await notifications.request_exact_alarm_permission()

        guarded_async(_check, "can_schedule_exact_notifications")

    def create_channel(e):
        guarded(
            notifications.create_notification_channel(
                NotificationChannel(
                    id="alerts", name="Alerts", description="High-priority alerts"
                )
            ),
            "create_notification_channel",
        )

    def list_channels(e):
        async def _list():
            channels = await notifications.get_notification_channels()
            log_line(f"channels: {[c.id for c in channels]}")

        guarded_async(_list, "get_notification_channels")

    def start_fgs(e):
        guarded(
            notifications.start_foreground_service(
                id=11, title="Foreground service", body="Work in progress…"
            ),
            "start_foreground_service",
        )

    def stop_fgs(e):
        guarded(notifications.stop_foreground_service(), "stop_foreground_service")

    def check_enabled(e):
        async def _check():
            log_line(f"enabled: {await notifications.are_notifications_enabled()}")

        guarded_async(_check, "are_notifications_enabled")

    def open_settings(e):
        guarded(
            notifications.open_app_notification_settings(),
            "open_app_notification_settings",
        )

    def list_active(e):
        async def _list():
            active = await notifications.get_active_notifications()
            log_line(f"active: {[a.id for a in active]}")

        guarded_async(_list, "get_active_notifications")

    def check_policy(e):
        async def _check():
            granted = await notifications.has_notification_policy_access()
            log_line(f"DND access: {granted}")
            if not granted:
                await notifications.request_notification_policy_access()

        guarded_async(_check, "has_notification_policy_access")

    def channel_groups(e):
        guarded(
            notifications.create_notification_channel_group("demo", "Demo group"),
            "create_notification_channel_group",
        )

    # ── Feature catalog ──────────────────────────────────────────────────
    # (key, label, handler). The key decides platform availability.
    FEATURES = [
        ("all", "Show", show_plain),
        ("all", "Show with actions", show_actions),
        ("all", "Request permissions", request_permissions),
        ("all", "Big text style", show_big_text),
        ("all", "Inbox style", show_inbox),
        ("all", "Progress", show_progress),
        ("all", "Grouped", show_grouped),
        ("all", "Options (per-platform)", show_options),
        ("all", "Are enabled", check_enabled),
        ("all", "Open settings", open_settings),
        ("all", "Active list", list_active),
        ("schedule_oneshot", "Schedule in 10s", schedule_delayed),
        ("schedule_recurring", "Schedule daily 08:30", schedule_daily),
        ("periodic", "Schedule hourly", schedule_hourly),
        ("cancel_pending", "List pending", list_pending),
        ("cancel_pending", "Cancel pending", cancel_pending),
        ("exact_alarms", "Check exact alarms", check_exact),
        ("channels", "Create channel", create_channel),
        ("channels", "List channels", list_channels),
        ("foreground", "Start foreground service", start_fgs),
        ("foreground", "Stop foreground service", stop_fgs),
        ("dnd", "DND access", check_policy),
        ("channel_groups", "Channel group", channel_groups),
    ]

    def supported(key: str) -> bool:
        required = REQUIRED.get(key)
        return required is None or page.platform in required

    available = [f for f in FEATURES if supported(f[0])]
    unavailable = [f for f in FEATURES if not supported(f[0])]

    # ── Layout: available features, then a revealable "elsewhere" section ──
    show_unavailable = {"on": False}

    def rebuild():
        summary.value = (
            f"{page.platform.name}: {len(available)} of {len(FEATURES)} "
            f"features available here"
        )
        controls = [
            summary,
            ft.Text("Available on this platform", weight=ft.FontWeight.BOLD),
        ]
        for _key, label, handler in available:
            controls.append(ft.OutlinedButton(content=label, on_click=handler))
        toggle.content = (
            f"Show {len(unavailable)} features not available on this platform"
            if not show_unavailable["on"]
            else "Hide unavailable features"
        )
        controls.append(toggle)
        if show_unavailable["on"]:
            controls.append(
                ft.Text("Available on other platforms", weight=ft.FontWeight.BOLD)
            )
            for key, label, _ in unavailable:
                controls.append(
                    ft.OutlinedButton(
                        content=f"{label} — {REASON.get(key, 'other platforms')}",
                        disabled=True,
                    )
                )
        controls.append(ft.Divider())
        controls.append(ft.Text("Event log", weight=ft.FontWeight.BOLD))
        controls.append(log_terminal)
        page.controls[0].controls = controls
        page.update(page.controls[0])

    def toggle_unavailable(e):
        show_unavailable["on"] = not show_unavailable["on"]
        rebuild()

    toggle = ft.OutlinedButton(content="", on_click=toggle_unavailable)
    summary = ft.Text("", size=13)
    page.add(ft.Column(controls=[], spacing=8))
    rebuild()
    log_line(f"Running on {page.platform.name} — {len(available)} features available")
    if unavailable:
        log_line(
            f"{len(unavailable)} features exist on other platforms "
            "(see below the buttons)"
        )


if __name__ == "__main__":
    ft.run(main)
