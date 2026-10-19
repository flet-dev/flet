# NOTE: deliberately no `from __future__ import annotations` — Flet's event
# resolver (`get_event_field_type`) evaluates class-level handler
# annotations as real objects and raises on PEP 563 strings, which would
# silently break on_tap/on_action/on_dismissed dispatch.

import json
from datetime import datetime, timedelta

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
from flet_notifications.styles import Style, prepare_style
from flet_notifications.types import (
    AndroidForegroundServiceType,
    AndroidScheduleMode,
    AndroidServiceStartType,
    DateTimeComponents,
    GroupAlertBehavior,
    RepeatInterval,
)

__all__ = ["LocalNotifications"]


@ft.control("LocalNotifications")
class LocalNotifications(ft.Service):
    """
    Native local notifications for Android, iOS, macOS, Windows, Linux, and Web.

    Create one service per page and keep its reference for sending notifications and
    handling responses. It registers with the page automatically and does not need to be
    added to the page's visual controls. Initialization occurs when the service reaches
    the client; method calls wait for it to finish.

    Feature support varies: rich styles and progress are Android-specific; calendar and
    interval recurrence are available on Android, iOS, and macOS; Windows supports
    one-shot scheduling; Linux and Web do not provide scheduling through this extension.
    Platform permissions and native configuration still apply. See the notification
    service's requirements in the user guide.

    Notification response handlers receive
    :class:`flet_notifications.NotificationEvent`. When a background action runs
    without the app UI, a native Dart handler persists the event for replay when the
    service next initializes; it does not execute Python in the background.

    Example:
        ```python
        import flet as ft
        import flet_notifications as ftn


        def main(page: ft.Page):
            notifications = ftn.LocalNotifications(
                on_tap=lambda e: print("Opened:", e.payload)
            )

            async def notify(e):
                if await notifications.request_permissions():
                    await notifications.show(
                        id=1,
                        title="Download complete",
                        body="Your file is ready.",
                        payload="download:42",
                    )

            page.add(ft.OutlinedButton(content="Notify", on_click=notify))


        ft.run(main)
        ```
    """

    default_icon: str | None = None
    """
    Default small Android notification icon.

    Supply a bundled drawable resource name, such as `"ic_stat_notify"`, without an
    extension. `None` uses `"@mipmap/ic_launcher"`. Android notification icons have
    platform-specific size and transparency requirements.
    """

    request_alert_permission: bool = True
    """
    Whether to request iOS/macOS alert authorization during initialization.

    Also controls which authorization is requested by :meth:`request_permissions`. Set
    this, :attr:`request_sound_permission`, and :attr:`request_badge_permission` to
    `False` to defer those prompts. Set the desired flags to `True` before calling
    :meth:`request_permissions`.
    """

    request_sound_permission: bool = True
    """
    Whether to request iOS/macOS sound authorization during initialization.

    Also used by :meth:`request_permissions`. Authorization permits sounds;
    :attr:`flet_notifications.DarwinOptions.present_sound` controls presentation.
    """

    request_badge_permission: bool = True
    """
    Whether to request iOS/macOS badge authorization during initialization.

    Also used by :meth:`request_permissions`. Set the badge value through
    :attr:`flet_notifications.DarwinOptions.badge_number`.
    """

    request_critical_permission: bool = False
    """
    Whether to request iOS/macOS critical-alert authorization.

    Used during initialization and by :meth:`request_permissions`. Requires Apple's
    critical-alert entitlement; this flag does not obtain that entitlement. See
    :attr:`flet_notifications.InterruptionLevel.CRITICAL`.
    """

    app_name: str | None = None
    """
    Application name used by the Windows notification backend.

    Set a name identifying your application.
    """

    app_user_model_id: str | None = None
    """
    Windows AppUserModelID identifying the source of notifications.

    Choose a stable ID unique to your app and consistent with its Windows packaging and
    shortcut identity.
    """

    windows_guid: str | None = None
    """
    GUID identifying the Windows toast activation component.

    Use a stable, application-specific GUID to avoid sharing an identity with other
    apps.
    """

    on_tap: ft.EventHandler[NotificationEvent["LocalNotifications"]] | None = None
    """
    Called when the user selects the notification body.

    The event includes the notification ID and application payload. A response that
    launched the app is replayed after initialization when launch details are available.
    Full-screen Android notification launches also use this handler.
    """

    on_action: ft.EventHandler[NotificationEvent["LocalNotifications"]] | None = None
    """
    Called when the user selects a notification action button.

    Use :attr:`flet_notifications.NotificationEvent.action_id` to identify the button
    and :attr:`flet_notifications.NotificationEvent.input` for reply text. Background
    Android/iOS actions are queued and replayed on the next service initialization;
    Python is not run in the background isolate.
    """

    on_dismissed: ft.EventHandler[NotificationEvent["LocalNotifications"]] | None = None
    """
    Called if the native backend reports a notification dismissal.

    The bridge currently does not configure Android dismissal isolates or Apple
    dismissal categories, so this handler does not enable dismissal reporting on those
    platforms. Delivery is backend-dependent; do not rely on a dismissal event for every
    notification that disappears.
    """

    # ── Shared kwargs for show / schedule / periodically_show ────────────

    @staticmethod
    def _details_args(
        style: Style | None,
        show_progress: bool,
        max_progress: int,
        progress: int,
        indeterminate: bool,
        group_key: str | None,
        set_as_group_summary: bool,
        group_alert_behavior: GroupAlertBehavior,
        channel_id: str | None,
        options: NotificationOptions | None = None,
    ) -> dict:
        """Collect style/progress/grouping arguments for Flet's encoder."""
        return {
            "style": prepare_style(style),
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

    async def initialize(self) -> None:
        """
        Initialize or reinitialize the native notification backend.

        The service initializes automatically, and other methods wait for that
        initialization. Call explicitly to retry a failed initialization or apply
        changed initialization properties. Initialization can request Apple permissions
        according to the service's permission flags.

        Note:
            Explicit reinitialization currently supplies no previously accumulated Apple
            action categories. Avoid using it just to refresh notifications after
            creating action buttons; posting notifications handles category registration
            automatically.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(await self._invoke_method("initialize"))

    async def show(
        self,
        id: int,
        title: str | None = None,
        body: str | None = None,
        payload: str = "",
        actions: list[NotificationAction] | None = None,
        style: Style | None = None,
        show_progress: bool = False,
        max_progress: int = 0,
        progress: int = 0,
        indeterminate: bool = False,
        group_key: str | None = None,
        set_as_group_summary: bool = False,
        group_alert_behavior: GroupAlertBehavior = GroupAlertBehavior.ALL,
        channel_id: str | None = None,
        options: NotificationOptions | None = None,
    ) -> None:
        """
        Display a local notification immediately.

        Reusing an ID normally updates the existing notification, which is useful for
        progress updates. Android's :attr:`flet_notifications.AndroidOptions.tag` also
        participates in identifying immediately displayed notifications. Visible
        content, action support, and alerting depend on the current platform and the
        user's notification settings. On Web, obtain browser permission with
        :meth:`request_permissions` before showing a notification.

        Args:
            id: Notification identifier. Reuse it to update the same notification;
                on Android, a tag also participates in identifying immediately shown
                notifications. Native platforms can impose identifier range limits.
            title: Notification title. `None` omits the title.
            body: Notification body. `None` omits the body.
            payload: Application-defined string returned with tap and action events.
                The service does not interpret this value.
            actions: Action buttons; see :class:`flet_notifications.NotificationAction`
                for platform support and background-response behavior.
            style: Expanded Android layout; see :class:`~flet_notifications.Style`.
                Other platforms ignore this argument.
            show_progress: Whether to show an Android progress bar.
            max_progress: Maximum value of the Android determinate progress bar.
            progress: Current Android progress value, normally between `0` and
                `max_progress`. Update the same ID to advance the bar.
            indeterminate: Whether the Android progress bar shows ongoing activity
                without a known completion amount. Requires `show_progress=True`.
            group_key: Android group identifier for related notifications. This is
                distinct from a notification-channel group and from Apple threads.
            set_as_group_summary: Whether this Android notification summarizes the
                notifications sharing `group_key`.
            group_alert_behavior: Which Android group members may sound or vibrate;
                see :class:`~flet_notifications.GroupAlertBehavior`.
            channel_id: Android channel ID. Takes precedence over
                :attr:`flet_notifications.AndroidOptions.channel_id`. Missing channels
                are created automatically. Pre-create a channel to customize its name or
                group.
            options: Additional per-platform details; see
                :class:`~flet_notifications.NotificationOptions`.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(
            await self._invoke_method(
                "show",
                {
                    "id": id,
                    "title": title,
                    "body": body,
                    "payload": payload,
                    "actions": actions or None,
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
                },
            )
        )

    async def cancel(self, id: int, tag: str | None = None) -> None:
        """
        Remove a displayed notification and cancel its scheduled request.

        On Android, a tag applies only to notifications posted immediately; scheduled
        alarms are identified by ID. On Windows, removal requires an MSIX package
        identity. Calling this method does not synthesize an :attr:`on_dismissed` event.

        Args:
            id: Identifier of the notification to remove.
            tag: Android tag supplied in :attr:`flet_notifications.AndroidOptions.tag`.
                Matches both tag and ID when provided; ignored on other platforms.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(
            await self._invoke_method(
                "cancel", {"id": id, "tag": tag} if tag else {"id": id}
            )
        )

    async def cancel_all(self) -> None:
        """
        Remove all of the app's displayed and scheduled notifications.

        To remove only undelivered requests, use :meth:`cancel_pending`. Windows removal
        requires an MSIX package identity. Does not remove Android channels or channel
        groups.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(await self._invoke_method("cancel_all"))

    async def request_permissions(self) -> bool:
        """
        Request notification authorization where the platform supports a prompt.

        On Android 13+, requests `POST_NOTIFICATIONS`; older Android versions do not
        show that runtime prompt. On iOS/macOS, requests the alert, sound, badge, and
        critical permissions selected by this service's corresponding
        `request_*_permission` properties. A previous denial may require the user to
        change system settings rather than displaying another prompt.

        On Web, requests browser notification permission. Call from a user interaction,
        such as an :attr:`flet.Button.on_click` handler, over HTTPS or a trusted
        localhost origin. An existing denial returns `False` without prompting again;
        the user must change the site's browser permissions. Dismissing the prompt
        without granting access also returns `False`. Unsupported browsers return
        `False`.

        On Windows and Linux, this bridge returns `True` without requesting or checking
        permission.

        Returns:
            Whether the native permission request succeeded, or `True` on platforms
            where this bridge performs no request. It does not guarantee delivery
            through per-channel restrictions, Focus, or Do Not Disturb.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        # Permission dialogs can take a while; allow more than the default.
        return to_bool(await self._invoke_method("request_permissions", timeout=300))

    async def schedule(
        self,
        id: int,
        when: datetime | timedelta,
        title: str | None = None,
        body: str | None = None,
        payload: str = "",
        actions: list[NotificationAction] | None = None,
        match_components: DateTimeComponents | None = None,
        options: NotificationOptions | None = None,
        schedule_mode: AndroidScheduleMode = AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE,
        time_zone: str | None = None,
        style: Style | None = None,
        show_progress: bool = False,
        max_progress: int = 0,
        progress: int = 0,
        indeterminate: bool = False,
        group_key: str | None = None,
        set_as_group_summary: bool = False,
        group_alert_behavior: GroupAlertBehavior = GroupAlertBehavior.ALL,
        channel_id: str | None = None,
    ) -> None:
        """
        Schedule a notification for a date, a delay, or a recurring calendar match.

        Supported on Android, iOS, macOS, and Windows. Windows schedules a single
        delivery even when calendar components are supplied. Linux and Web do not
        support this operation. Android needs the scheduling receivers and permissions
        described in the notification service requirements; restoring schedules after a
        reboot also requires the boot receiver.

        Calendar recurrence and fixed intervals are different: use
        :meth:`periodically_show` for notifications repeating after an elapsed interval
        rather than at a particular local time.

        Note:
            iOS retains at most 64 pending notifications per app on supported system
            versions. Plan schedules within this limit and query
            :meth:`get_pending_notifications` when managing pending requests.

        Args:
            id: Notification identifier. Reuse it to update the same notification;
                on Android, a tag also participates in identifying immediately shown
                notifications. Native platforms can impose identifier range limits.
            when: Delivery time as a `datetime`, or a delay as a `timedelta`.
                Naive datetimes are wall-clock times in `time_zone` or the device
                timezone; aware datetimes preserve their exact instant. Native
                scheduling has at best second precision, and delay fractions are
                truncated to whole seconds.
            title: Notification title. `None` omits the title.
            body: Notification body. `None` omits the body.
            payload: Application-defined string returned with tap and action events.
                The service does not interpret this value.
            actions: Action buttons; see :class:`~flet_notifications.NotificationAction`
                for platform support and background-response behavior.
            match_components: Calendar components used for recurrence on Android,
                iOS, and macOS. `None` schedules once. The first delivery is the next
                matching occurrence, which may precede the full date in `when`. Windows
                ignores this argument and schedules once.
            options: Additional per-platform details; see
                :class:`~flet_notifications.NotificationOptions`.
            schedule_mode: Android alarm precision and idle-mode behavior; see
                :class:`~flet_notifications.AndroidScheduleMode`. Exact modes require
                the applicable exact-alarm access. Ignored on other platforms.
            time_zone: IANA timezone name, such as `"Europe/Paris"`, for calendar
                interpretation and recurrence. When `None`, uses the device timezone;
                the bridge falls back to UTC if timezone lookup fails.
            style: Expanded Android layout; see :class:`~flet_notifications.Style`.
                Other platforms ignore this argument.
            show_progress: Whether to show an Android progress bar.
            max_progress: Maximum value of the Android determinate progress bar.
            progress: Current Android progress value, normally between `0` and
                `max_progress`. Update the same ID to advance the bar.
            indeterminate: Whether the Android progress bar shows ongoing activity
                without a known completion amount. Requires `show_progress=True`.
            group_key: Android group identifier for related notifications. This is
                distinct from a notification-channel group and from Apple threads.
            set_as_group_summary: Whether this Android notification summarizes the
                notifications sharing `group_key`.
            group_alert_behavior: Which Android group members may sound or vibrate;
                see :class:`~flet_notifications.GroupAlertBehavior`.
            channel_id: Android channel ID. Takes precedence over
                :attr:`flet_notifications.AndroidOptions.channel_id`. Missing channels
                are created automatically. Pre-create a channel to customize its name or
                group.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.

        Example:
            ```python
            from datetime import datetime
            import flet_notifications as ftn

            await notifications.schedule(
                id=2,
                when=datetime(2027, 1, 1, 9, 0),
                title="Morning reminder",
                match_components=ftn.DateTimeComponents.TIME,
                time_zone="Europe/Paris",
                schedule_mode=ftn.AndroidScheduleMode.INEXACT_ALLOW_WHILE_IDLE,
            )
            ```
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
        title: str | None = None,
        body: str | None = None,
        payload: str = "",
        actions: list[NotificationAction] | None = None,
        schedule_mode: AndroidScheduleMode = AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE,
        repeat_duration_seconds: int | None = None,
        style: Style | None = None,
        show_progress: bool = False,
        max_progress: int = 0,
        progress: int = 0,
        indeterminate: bool = False,
        group_key: str | None = None,
        set_as_group_summary: bool = False,
        group_alert_behavior: GroupAlertBehavior = GroupAlertBehavior.ALL,
        channel_id: str | None = None,
        options: NotificationOptions | None = None,
    ) -> None:
        """
        Schedule a notification repeating after a fixed elapsed interval.

        The first delivery is one interval after this call, not immediately. Supported
        on Android, iOS, and macOS; Windows, Linux, and Web do not support this
        operation. Android requires the scheduling setup described in the notification
        service requirements. Actual timing is subject to OS power management and alarm
        policies.

        For a specific local time such as 09:00 every day, use :meth:`schedule` with
        :class:`~flet_notifications.DateTimeComponents` instead.

        Args:
            id: Notification identifier. Reuse it to update the same notification;
                on Android, a tag also participates in identifying immediately shown
                notifications. Native platforms can impose identifier range limits.
            repeat_interval: Standard repeat interval, used unless
                `repeat_duration_seconds` is provided. The argument remains required
                even when a custom duration overrides it.
            title: Notification title. `None` omits the title.
            body: Notification body. `None` omits the body.
            payload: Application-defined string returned with tap and action events.
                The service does not interpret this value.
            actions: Action buttons; see :class:`~flet_notifications.NotificationAction`
                for platform support and background-response behavior.
            schedule_mode: Android alarm precision and idle-mode behavior; see
                :class:`~flet_notifications.AndroidScheduleMode`. Exact modes require
                the applicable exact-alarm access. Ignored on other platforms.
            repeat_duration_seconds: Custom interval in whole seconds, at least
                `60`. Overrides `repeat_interval`. `None` uses the enum interval.
            style: Expanded Android layout; see :class:`~flet_notifications.Style`.
                Other platforms ignore this argument.
            show_progress: Whether to show an Android progress bar.
            max_progress: Maximum value of the Android determinate progress bar.
            progress: Current Android progress value, normally between `0` and
                `max_progress`. Update the same ID to advance the bar.
            indeterminate: Whether the Android progress bar shows ongoing activity
                without a known completion amount. Requires `show_progress=True`.
            group_key: Android group identifier for related notifications. This is
                distinct from a notification-channel group and from Apple threads.
            set_as_group_summary: Whether this Android notification summarizes the
                notifications sharing `group_key`.
            group_alert_behavior: Which Android group members may sound or vibrate;
                see :class:`~flet_notifications.GroupAlertBehavior`.
            channel_id: Android channel ID. Takes precedence over
                :attr:`flet_notifications.AndroidOptions.channel_id`. Missing channels
                are created automatically. Pre-create a channel to customize its name or
                group.
            options: Additional per-platform details; see
                :class:`~flet_notifications.NotificationOptions`.

        Raises:
            ValueError: If `repeat_duration_seconds` is less than `60`.
            NotificationError: If the bridge reports initialization or scheduling
                failure.
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
        """
        Cancel all scheduled notifications without removing displayed ones.

        Supported on Android, iOS, and macOS. Other platforms report an unsupported
        operation. Use :meth:`cancel` to remove a specific pending request.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(await self._invoke_method("cancel_pending"))

    async def get_pending_notifications(self) -> list[PendingNotification]:
        """
        Query notifications scheduled for future delivery.

        Supported by Android, iOS, macOS, and the Windows backend. Windows query support
        depends on package identity. Unsupported queries can report a
        :class:`~flet_notifications.NotificationError`; an empty list is not a universal
        unsupported-platform response.

        Returns:
            Snapshots of pending requests. These do not include every platform detail
            and cannot be edited to change the native schedule.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
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
        """
        Decode a query result: Dart returns decoded collections or a JSON string \
        depending on the platform (MsgPack vs method-channel transport).
        """
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
        """
        Check Android's authorization to schedule exact alarms.

        Android restricts exact alarms from Android 12 onward. This is separate from
        notification-display permission and channel settings.

        Returns:
            Whether the Android backend reports exact alarms are allowed. Returns `True`
            on non-Android platforms, where this Android check is not applied.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        return to_bool(await self._invoke_method("can_schedule_exact_notifications"))

    async def request_exact_alarm_permission(self) -> bool:
        """
        Request Android exact-alarm access through system settings when needed.

        Use with the `SCHEDULE_EXACT_ALARM` manifest permission. This is especially
        relevant to apps targeting Android 13+ and running on Android 14+, where the
        permission may not be granted at installation. Exact-alarm access is separate
        from :meth:`request_permissions`.

        Returns:
            Whether access is granted after the request. Returns `False` on non-Android
            platforms. A grant does not create a scheduled notification.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        return to_bool(
            await self._invoke_method("request_exact_alarm_permission", timeout=300)
        )

    # ── Channels (Android 8.0+) ─────────────────────────────────────────

    async def create_notification_channel(self, channel: NotificationChannel) -> None:
        """
        Create an Android notification channel or update its mutable details.

        Applies on Android 8.0+. Existing channel sound, vibration, lights, and
        importance cannot be reset through this call. See
        :class:`~flet_notifications.NotificationChannel` for creation-time settings.
        Non-Android platforms report an unsupported operation.

        Args:
            channel: Channel declaration. Post notifications using its ID as
                `channel_id`. Create its group first when a group ID is supplied.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(await self._invoke_method("create_notification_channel", channel))

    async def delete_notification_channel(self, channel_id: str) -> None:
        """
        Delete an Android notification channel on Android 8.0+.

        Non-Android platforms report an unsupported operation. This does not cancel
        pending schedules that still refer to the channel; cancel those separately if
        they should no longer deliver notifications.

        Args:
            channel_id: Identifier of the channel to delete.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(
            await self._invoke_method(
                "delete_notification_channel", {"channel_id": channel_id}
            )
        )

    async def get_notification_channels(self) -> list[NotificationChannel]:
        """
        Query the app's Android notification channels.

        Returns:
            Channel snapshots on supported Android versions, or an empty list on
            non-Android platforms. Returned values reflect the native channel settings,
            including changes made by the user.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
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
        title: str | None = None,
        body: str | None = None,
        payload: str = "",
        actions: list[NotificationAction] | None = None,
        style: Style | None = None,
        show_progress: bool = False,
        max_progress: int = 0,
        progress: int = 0,
        indeterminate: bool = False,
        channel_id: str | None = None,
        options: NotificationOptions | None = None,
        start_type: AndroidServiceStartType | None = None,
        foreground_service_types: list[AndroidForegroundServiceType] | None = None,
    ) -> None:
        """
        Start an Android foreground service with a visible notification.

        Requires a service declaration, appropriate foreground-service permissions, and
        types matching the actual work. See
        :class:`flet_notifications.AndroidForegroundServiceType` for the shared
        setup and each type's `pyproject.toml` entries and runtime requirements.
        Other platforms report an unsupported operation.

        This starts the plugin's native foreground service; it does not create a Python
        worker or guarantee that Android will keep the process alive indefinitely.
        Android's start restrictions and service time limits still apply. Use
        :meth:`stop_foreground_service` when the work is finished.

        Args:
            id: Nonzero identifier for the foreground-service notification.
            title: Notification title. `None` omits the title.
            body: Notification body. `None` omits the body.
            payload: Application-defined string returned with tap and action events.
                The service does not interpret this value.
            actions: Action buttons; see :class:`~flet_notifications.NotificationAction`
                for platform support and background-response behavior.
            style: Expanded Android layout; see :class:`~flet_notifications.Style`.
                Other platforms ignore this argument.
            show_progress: Whether to show an Android progress bar.
            max_progress: Maximum value of the Android determinate progress bar.
            progress: Current Android progress value, normally between `0` and
                `max_progress`. Update the same ID to advance the bar.
            indeterminate: Whether the Android progress bar shows ongoing activity
                without a known completion amount. Requires `show_progress=True`.
            channel_id: Android channel ID. Takes precedence over
                :attr:`flet_notifications.AndroidOptions.channel_id`. Missing channels
                are created automatically. Pre-create a channel to customize its name or
                group.
            options: Additional per-platform details; see
                :class:`~flet_notifications.NotificationOptions`.
            start_type: Native service restart policy; see
                :class:`~flet_notifications.AndroidServiceStartType`. This does
                not control restarting Python tasks.
            foreground_service_types: Kinds of work performed by the service;
                see :class:`~flet_notifications.AndroidForegroundServiceType`.
                Must match the manifest declarations and permissions. `None`
                or an empty list uses the manifest's service types.

        Raises:
            ValueError: If `id` is `0`.
            NotificationError: If the bridge reports initialization or service failure.
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
                    "actions": actions or None,
                    **self._details_args(
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
                    ),
                },
            )
        )

    async def stop_foreground_service(self) -> None:
        """
        Stop the Android foreground service started by this extension.

        Removes the service's foreground notification. It does not terminate Python
        tasks you started; stop the associated application work yourself. Other
        platforms report an unsupported operation.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(await self._invoke_method("stop_foreground_service"))

    # ── Probes & OS integration ─────────────────────────────────────────

    async def are_notifications_enabled(self) -> bool:
        """
        Check application-level notification authorization where supported.

        On Android, queries whether the app's notifications are enabled. On iOS/macOS,
        includes provisional authorization, which permits quiet delivery. On Web,
        checks the current browser permission without displaying a prompt; denied,
        undecided, or unsupported notification access returns `False`.

        This check does not guarantee a particular channel, sound, or alert can
        interrupt the user.

        Returns:
            Native authorization status on Android/iOS/macOS, or browser authorization
            on Web. Returns `True` unconditionally on Windows and Linux, without
            checking system notification settings.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        return to_bool(await self._invoke_method("are_notifications_enabled"))

    async def open_app_notification_settings(self) -> None:
        """
        Open the operating system's notification settings for this app.

        On iOS, the plugin tries the app's notification settings and falls back to the
        app's general settings when necessary. Unsupported platforms can report an
        error. The bridge discards the native success flag, so a successful return does
        not confirm that a settings screen opened.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(await self._invoke_method("open_app_settings"))

    async def get_active_notifications(self) -> list[ActiveNotification]:
        """
        Query delivered notifications that have not been dismissed or removed.

        Supported on Android 6.0+, iOS 10+, macOS 10.14+, and Windows with an MSIX
        package identity. The Windows backend returns an empty list without that
        identity. Linux does not support the query; unsupported backends can report an
        error rather than returning an empty list.

        Returns:
            Snapshots of active notifications, with platform-dependent fields. Missing
            text values are represented as empty strings.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
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
        """
        Query whether a notification caused this application launch.

        Use for initial routing or inspecting the launch payload. It does not consume
        the response or suppress the automatic :attr:`on_tap` / :attr:`on_action`
        replay, so avoid processing the same launch twice if you use both mechanisms.
        Linux does not provide launch details through the upstream plugin; other
        platforms may also return no details.

        Returns:
            Launch information, with `did_notification_launch_app=False` when the
            backend supplies no notification launch. The response itself can be `None`
            even when the launch flag is set.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
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
        """
        Request access to Android full-screen notification intents.

        On Android 14+, access can depend on the app's permitted use and user settings.
        Requires the `USE_FULL_SCREEN_INTENT` manifest permission. After obtaining
        access, enable :attr:`flet_notifications.AndroidOptions.full_screen_intent` on
        the notification. A grant does not guarantee full-screen presentation; Android
        may show a heads-up notification instead.

        Returns:
            Whether the Android backend reports access is granted; `False` on
            non-Android platforms.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        return to_bool(
            await self._invoke_method("request_full_screen_intent", timeout=300)
        )

    async def has_notification_policy_access(self) -> bool:
        """
        Check whether Android has granted notification-policy access.

        This access is needed before creating a channel that requests Do Not Disturb
        bypass; it is distinct from notification-display permission.

        Returns:
            Whether access is granted on Android, or `False` on other platforms.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        return to_bool(await self._invoke_method("has_notification_policy_access"))

    async def request_notification_policy_access(self) -> bool:
        """
        Open Android's notification-policy access settings when required.

        Requires `ACCESS_NOTIFICATION_POLICY` in the Android manifest. Obtain access
        before creating channels with
        :attr:`flet_notifications.NotificationChannel.bypass_dnd` enabled.

        Returns:
            Whether Android reports access after the request, or `False` on other
            platforms. The user can decline the request.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        return to_bool(
            await self._invoke_method("request_notification_policy_access", timeout=300)
        )

    # ── Channel groups (Android 8.0+) ───────────────────────────────────

    async def create_notification_channel_group(
        self, group_id: str, name: str, description: str = ""
    ) -> None:
        """
        Create a group organizing Android channels in system notification settings.

        Supported on Android 8.0+. This is distinct from grouping displayed
        notifications with `group_key`. Create the group before creating channels that
        refer to its ID. Other platforms report an unsupported operation.

        Args:
            group_id: Stable identifier for the channel group.
            name: User-visible group name.
            description: Optional explanation of the group, supported on Android 9.0+.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
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
        """
        Delete an Android notification-channel group and all its channels.

        Supported on Android 8.0+; other platforms report an unsupported operation. This
        also removes channel configuration for the group's channels. Cancel unwanted
        pending notifications separately.

        Args:
            group_id: Identifier of the group to delete.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        check_result(
            await self._invoke_method(
                "delete_notification_channel_group",
                {"group_id": group_id},
            )
        )
