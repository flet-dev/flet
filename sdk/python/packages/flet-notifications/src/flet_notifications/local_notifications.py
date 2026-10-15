"""The LocalNotifications service: cross-platform notifications for Flet."""

# NOTE: deliberately no ``from __future__ import annotations`` — Flet's event
# resolver (``get_event_field_type``) evaluates class-level handler
# annotations as real objects and raises on PEP 563 strings, which would
# silently break on_tap/on_action/on_dismissed dispatch.

import json
from datetime import datetime, timedelta
from typing import Optional

import flet as ft
from flet.utils import from_dict
from flet_notifications.actions import NotificationAction
from flet_notifications.base import (
    NotificationError,
    NotificationEvent,
    check_result,
    to_bool,
)
from flet_notifications.channels import NotificationChannel
from flet_notifications.events import (
    ActiveNotification,
    LaunchDetails,
    PendingNotification,
)
from flet_notifications.options import NotificationOptions
from flet_notifications.scheduling import (
    build_periodic_args,
    build_schedule_args,
)
from flet_notifications.styles import Style
from flet_notifications.types import (
    AndroidScheduleMode,
    DateTimeComponents,
    GroupAlertBehavior,
    RepeatInterval,
)


@ft.control("LocalNotifications")
class LocalNotifications(ft.Service):
    """Cross-platform local notifications (Android, iOS, macOS, Windows,
    Linux, Web).

    A headless service — instantiate it once and it registers itself with the
    page. No need to add it to the page's controls.

    Example:
        .. code-block:: python

            import flet as ft
            from flet_notifications import LocalNotifications


            async def main(page: ft.Page):
                notifications = LocalNotifications()

                async def on_tap(e):
                    print("tapped:", e.payload)

                notifications.on_tap = on_tap

                if await notifications.request_permissions():
                    await notifications.show(
                        id=1, title="Hello", body="from flet-notifications"
                    )


            ft.run(main)
    """

    default_icon: Optional[str] = None
    """Android default small icon drawable name (default: the app launcher icon)."""

    request_alert_permission: bool = True
    """iOS/macOS: request the alert permission during initialization."""

    request_sound_permission: bool = True
    """iOS/macOS: request the sound permission during initialization."""

    request_badge_permission: bool = True
    """iOS/macOS: request the badge permission during initialization."""

    request_critical_permission: bool = False
    """iOS/macOS: request the critical-alert permission (needs an Apple entitlement)."""

    app_name: Optional[str] = None
    """Windows: application name shown on toasts."""

    app_user_model_id: Optional[str] = None
    """Windows: AppUserModelID used to group toasts under the app."""

    windows_guid: Optional[str] = None
    """Windows: GUID identifying the toast notifier."""

    on_tap: Optional[ft.EventHandler[NotificationEvent["LocalNotifications"]]] = None
    """Fired when the notification body is tapped."""

    on_action: Optional[ft.EventHandler[NotificationEvent["LocalNotifications"]]] = None
    """Fired when an action button is pressed (``action_id`` names the button)."""

    on_dismissed: Optional[ft.EventHandler[NotificationEvent["LocalNotifications"]]] = (
        None
    )
    """Fired when the OS reports the notification was dismissed/cleared."""

    # ── Shared kwargs for show / schedule / periodically_show ────────────

    @staticmethod
    def _details_args(
        style: Optional[Style],
        show_progress: bool,
        max_progress: int,
        progress: int,
        indeterminate: bool,
        group_key: Optional[str],
        set_as_group_summary: bool,
        group_alert_behavior: GroupAlertBehavior,
        channel_id: Optional[str],
        options: Optional[NotificationOptions] = None,
    ) -> dict:
        """Collect the style/progress/grouping kwargs (unserialized)."""
        return {
            "style": style,
            "options": options,
            "show_progress": show_progress,
            "max_progress": max_progress,
            "progress": progress,
            "indeterminate": indeterminate,
            "group_key": group_key,
            "set_as_group_summary": set_as_group_summary,
            "group_alert_behavior": group_alert_behavior,
            "channel_id": channel_id,
        }

    @staticmethod
    def _serialize_details(details: dict) -> dict:
        """Convert details kwargs to JSON-ready wire form (for ``show``)."""
        out = dict(details)
        out["style"] = details["style"].to_dict() if details["style"] else None
        out["options"] = details["options"].to_dict() if details["options"] else None
        out["group_alert_behavior"] = details["group_alert_behavior"].value
        return out

    async def initialize(self) -> None:
        """Initialize the notification backend.

        Initialization happens automatically when the service is created;
        call this only to force a re-initialization.
        """
        check_result(await self._invoke_method("initialize"))

    async def show(
        self,
        id: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        payload: str = "",
        actions: Optional[list[NotificationAction]] = None,
        style: Optional[Style] = None,
        show_progress: bool = False,
        max_progress: int = 0,
        progress: int = 0,
        indeterminate: bool = False,
        group_key: Optional[str] = None,
        set_as_group_summary: bool = False,
        group_alert_behavior: GroupAlertBehavior = GroupAlertBehavior.ALL,
        channel_id: Optional[str] = None,
        options: Optional[NotificationOptions] = None,
    ) -> None:
        """Show a notification immediately.

        Args:
            id: Notification id; showing again with the same id updates it —
                this is how live progress bars are advanced.
            title: Notification title.
            body: Notification body text.
            payload: Opaque string handed back on tap (e.g. a deep link).
            actions: Action buttons shown on the notification.
            style: Rich style (big text / big picture / inbox / messaging).
            show_progress: Show a determinate (or indeterminate) progress bar.
            group_key: Group related notifications together.
            set_as_group_summary: Use this notification as the group summary.
            group_alert_behavior: Which notifications in the group alert.
            channel_id: Android channel to post on (created if missing).
        """
        check_result(
            await self._invoke_method(
                "show",
                {
                    "id": id,
                    "title": title,
                    "body": body,
                    "payload": payload,
                    "actions": [a.to_dict() for a in actions] if actions else None,
                    **self._serialize_details(
                        self._details_args(
                            style,
                            show_progress,
                            max_progress,
                            progress,
                            indeterminate,
                            group_key,
                            set_as_group_summary,
                            group_alert_behavior,
                            channel_id,
                            options,
                        )
                    ),
                },
            )
        )

    async def cancel(self, id: int, tag: Optional[str] = None) -> None:
        """Cancel a previously shown or scheduled notification.

        Args:
            id: Notification id.
            tag: Android notification tag (for grouped notifications posted
                with a tag).
        """
        check_result(
            await self._invoke_method(
                "cancel", {"id": id, "tag": tag} if tag else {"id": id}
            )
        )

    async def cancel_all(self) -> None:
        """Cancel all shown notifications."""
        check_result(await self._invoke_method("cancel_all"))

    async def request_permissions(self) -> bool:
        """Request the OS notification permission.

        On platforms where permission is implicit (Windows, Linux, Web-before-
        prompt) this returns the current status. Windows raises the
        browser prompt; Android 13+ shows the runtime dialog.
        """
        # Permission dialogs can take a while; allow more than the default.
        return to_bool(await self._invoke_method("request_permissions", timeout=300))

    async def schedule(
        self,
        id: int,
        when: datetime | timedelta,
        title: Optional[str] = None,
        body: Optional[str] = None,
        payload: str = "",
        actions: Optional[list[NotificationAction]] = None,
        match_components: Optional[DateTimeComponents] = None,
        options: Optional[NotificationOptions] = None,
        schedule_mode: AndroidScheduleMode = AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE,
        time_zone: Optional[str] = None,
        style: Optional[Style] = None,
        show_progress: bool = False,
        max_progress: int = 0,
        progress: int = 0,
        indeterminate: bool = False,
        group_key: Optional[str] = None,
        set_as_group_summary: bool = False,
        group_alert_behavior: GroupAlertBehavior = GroupAlertBehavior.ALL,
        channel_id: Optional[str] = None,
    ) -> None:
        """Schedule a notification for a future time, handled by the OS.

        Survives app restarts (and, on Android, reboots — see the README for
        the required manifest entries).

        Args:
            id: Notification id.
            when: When to deliver — a ``datetime`` (naive values are
                interpreted in ``time_zone`` or the device timezone) or a
                ``timedelta`` from now.
            match_components: Repeat on a calendar component (e.g. daily at
                this time); use :meth:`periodically_show` for interval
                recurrence.
            schedule_mode: Android alarm exactness mode.
            time_zone: IANA timezone name for naive ``when`` and recurrence
                (e.g. ``"Africa/Lagos"``); defaults to the device timezone.
            style: Rich style (big text / big picture / inbox / messaging).
            show_progress: Show a determinate (or indeterminate) progress bar.
            group_key: Group related notifications together.
            set_as_group_summary: Use this notification as the group summary.
            group_alert_behavior: Which notifications in the group alert.
            channel_id: Android channel to post on (created if missing).
        """
        check_result(
            await self._invoke_method(
                "schedule",
                build_schedule_args(
                    id=id,
                    when=when,
                    title=title,
                    body=body,
                    payload=payload,
                    actions=actions or [],
                    match_components=match_components,
                    schedule_mode=schedule_mode,
                    time_zone=time_zone,
                    **self._details_args(
                        style,
                        show_progress,
                        max_progress,
                        progress,
                        indeterminate,
                        group_key,
                        set_as_group_summary,
                        group_alert_behavior,
                        channel_id,
                        options,
                    ),
                ),
            )
        )

    async def periodically_show(
        self,
        id: int,
        repeat_interval: RepeatInterval,
        title: Optional[str] = None,
        body: Optional[str] = None,
        payload: str = "",
        actions: Optional[list[NotificationAction]] = None,
        schedule_mode: AndroidScheduleMode = AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE,
        repeat_duration_seconds: Optional[int] = None,
        style: Optional[Style] = None,
        show_progress: bool = False,
        max_progress: int = 0,
        progress: int = 0,
        indeterminate: bool = False,
        group_key: Optional[str] = None,
        set_as_group_summary: bool = False,
        group_alert_behavior: GroupAlertBehavior = GroupAlertBehavior.ALL,
        channel_id: Optional[str] = None,
        options: Optional[NotificationOptions] = None,
    ) -> None:
        """Show a notification repeating at a fixed interval.

        The first delivery happens one interval after the call. Not supported
        on Linux/Web (no OS scheduler) or Windows (one-shot only).
        """
        check_result(
            await self._invoke_method(
                "periodically_show",
                build_periodic_args(
                    id=id,
                    repeat_interval=repeat_interval,
                    title=title,
                    body=body,
                    payload=payload,
                    actions=actions or [],
                    schedule_mode=schedule_mode,
                    repeat_duration_seconds=repeat_duration_seconds,
                    **self._details_args(
                        style,
                        show_progress,
                        max_progress,
                        progress,
                        indeterminate,
                        group_key,
                        set_as_group_summary,
                        group_alert_behavior,
                        channel_id,
                        options,
                    ),
                ),
            )
        )

    async def cancel_pending(self) -> None:
        """Cancel all scheduled notifications that haven't been delivered."""
        check_result(await self._invoke_method("cancel_pending"))

    async def get_pending_notifications(self) -> list[PendingNotification]:
        """Return notifications scheduled for future delivery.

        Supported on Android and iOS/macOS; empty on other platforms.
        """
        result = await self._invoke_method("get_pending")
        check_result(result)
        return self._parse_pending(self._as_list(result))

    @staticmethod
    def _parse_pending(result: object) -> list[PendingNotification]:
        if not isinstance(result, list):
            return []
        pending = []
        for entry in result:
            if not isinstance(entry, dict):
                continue
            pending.append(
                PendingNotification(
                    id=int(entry.get("id", 0)),
                    title=str(entry.get("title") or ""),
                    body=str(entry.get("body") or ""),
                    payload=str(entry.get("payload") or ""),
                )
            )
        return pending

    @staticmethod
    def _as_list(result: object) -> list:
        """Decode a query result: Dart returns decoded collections or a JSON
        string depending on the platform (MsgPack vs method-channel transport)."""
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError as e:
                raise NotificationError("query_failed", str(e)) from e
        return result if isinstance(result, list) else []

    @staticmethod
    def _as_dict(result: object) -> dict:
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except json.JSONDecodeError as e:
                raise NotificationError("query_failed", str(e)) from e
        return result if isinstance(result, dict) else {}

    async def can_schedule_exact_notifications(self) -> bool:
        """Android: whether the app may schedule exact alarms (14+)."""
        return to_bool(await self._invoke_method("can_schedule_exact_notifications"))

    async def request_exact_alarm_permission(self) -> bool:
        """Android: open the exact-alarm permission screen (14+)."""
        return to_bool(
            await self._invoke_method("request_exact_alarm_permission", timeout=300)
        )

    # ── Channels (Android 8.0+) ─────────────────────────────────────────

    async def create_notification_channel(self, channel: NotificationChannel) -> None:
        """Create or update an Android notification channel."""
        check_result(
            await self._invoke_method("create_notification_channel", channel.to_dict())
        )

    async def delete_notification_channel(self, channel_id: str) -> None:
        """Delete an Android notification channel."""
        check_result(
            await self._invoke_method(
                "delete_notification_channel", {"channel_id": channel_id}
            )
        )

    async def get_notification_channels(self) -> list[NotificationChannel]:
        """List the app's Android notification channels."""
        result = await self._invoke_method("get_notification_channels")
        check_result(result)
        return [
            NotificationChannel.from_dict(entry)
            for entry in self._as_list(result)
            if isinstance(entry, dict)
        ]

    # ── Foreground service (Android) ────────────────────────────────────

    async def start_foreground_service(
        self,
        id: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        payload: str = "",
        actions: Optional[list[NotificationAction]] = None,
        style: Optional[Style] = None,
        show_progress: bool = False,
        max_progress: int = 0,
        progress: int = 0,
        indeterminate: bool = False,
        channel_id: Optional[str] = None,
        options: Optional[NotificationOptions] = None,
        start_type: Optional[str] = None,
        foreground_service_types: Optional[list[str]] = None,
    ) -> None:
        """Start a foreground service with a persistent notification.

        Keeps the process alive for long-running work while showing the
        notification. Requires manifest entries on Android — see the README.
        """
        if id == 0:
            raise ValueError("foreground service id must be non-zero")
        check_result(
            await self._invoke_method(
                "start_foreground_service",
                {
                    "id": id,
                    "title": title,
                    "body": body,
                    "payload": payload,
                    "start_type": start_type,
                    "foreground_service_types": foreground_service_types,
                    "actions": [a.to_dict() for a in actions] if actions else None,
                    **self._serialize_details(
                        self._details_args(
                            style,
                            show_progress,
                            max_progress,
                            progress,
                            indeterminate,
                            None,
                            False,
                            GroupAlertBehavior.ALL,
                            channel_id,
                            options,
                        )
                    ),
                },
            )
        )

    async def stop_foreground_service(self) -> None:
        """Stop the foreground service started by this app."""
        check_result(await self._invoke_method("stop_foreground_service"))

    # ── Probes & OS integration ─────────────────────────────────────────

    async def are_notifications_enabled(self) -> bool:
        """Whether the OS will deliver this app's notifications."""
        return to_bool(await self._invoke_method("are_notifications_enabled"))

    async def open_app_notification_settings(self) -> None:
        """Open the OS notification settings page for this app."""
        check_result(await self._invoke_method("open_app_settings"))

    async def get_active_notifications(self) -> list[ActiveNotification]:
        """List notifications currently shown in the tray.

        Supported on Android 6+, iOS 10+ and macOS 10.14+; empty elsewhere.
        """
        result = await self._invoke_method("get_active")
        check_result(result)
        entries = self._as_list(result)
        return [
            ActiveNotification(
                id=int(e.get("id", 0)),
                channel_id=str(e.get("channel_id") or ""),
                group_key=str(e.get("group_key") or ""),
                tag=str(e.get("tag") or ""),
                title=str(e.get("title") or ""),
                body=str(e.get("body") or ""),
                payload=str(e.get("payload") or ""),
                big_text=str(e.get("big_text") or ""),
            )
            for e in entries
            if isinstance(e, dict)
        ]

    async def get_notification_app_launch_details(self) -> LaunchDetails:
        """How the app was launched — if a notification launched it.

        Background taps are replayed automatically to ``on_tap`` /
        ``on_action``; this is for apps that want the cold-start details
        themselves.
        """
        result = await self._invoke_method("get_launch_details")
        check_result(result)
        result = self._as_dict(result)
        launched = bool(result.get("did_notification_launch_app", False))
        notification = result.get("notification")
        if not isinstance(notification, dict):
            return LaunchDetails(did_notification_launch_app=launched)
        return LaunchDetails(
            did_notification_launch_app=launched,
            notification=from_dict(
                NotificationEvent,
                {"control": self, "name": "tap", **notification},
            ),
        )

    async def request_full_screen_intent_permission(self) -> bool:
        """Android 14+: request the full-screen-intent permission."""
        return to_bool(
            await self._invoke_method("request_full_screen_intent", timeout=300)
        )

    async def has_notification_policy_access(self) -> bool:
        """Android: whether the app may bypass Do Not Disturb."""
        return to_bool(await self._invoke_method("has_notification_policy_access"))

    async def request_notification_policy_access(self) -> bool:
        """Android: open the Do-Not-Disturb access settings screen."""
        return to_bool(
            await self._invoke_method("request_notification_policy_access", timeout=300)
        )

    # ── Channel groups (Android 8.0+) ───────────────────────────────────

    async def create_notification_channel_group(
        self, group_id: str, name: str, description: str = ""
    ) -> None:
        """Create an Android notification-channel group."""
        check_result(
            await self._invoke_method(
                "create_notification_channel_group",
                {
                    "group_id": group_id,
                    "name": name,
                    "description": description,
                },
            )
        )

    async def delete_notification_channel_group(self, group_id: str) -> None:
        """Delete an Android notification-channel group and its channels."""
        check_result(
            await self._invoke_method(
                "delete_notification_channel_group",
                {"group_id": group_id},
            )
        )
