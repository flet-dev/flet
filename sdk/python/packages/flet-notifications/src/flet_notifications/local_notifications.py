from datetime import datetime, timedelta
from typing import Any

import flet as ft
from flet_notifications.actions import NotificationAction
from flet_notifications.base import (
    NotificationEvent,
    NotificationInvalidArgumentError,
    error_from_bridge,
    parse_query_list,
)
from flet_notifications.channels import NotificationChannel
from flet_notifications.events import (
    ActiveNotification,
    PendingNotification,
)
from flet_notifications.options import NotificationOptions
from flet_notifications.scheduling import (
    build_periodic_args,
    build_schedule_args,
)
from flet_notifications.types import (
    AndroidForegroundServiceType,
    AndroidScheduleMode,
    AndroidServiceStartType,
    DateTimeComponents,
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

    Note:
        Feature support varies: rich styles, progress, and grouping are
        Android-specific (see :class:`flet_notifications.AndroidOptions`); calendar
        and interval recurrence are available on Android, iOS, and macOS; Windows
        supports one-shot scheduling; Linux and Web do not provide scheduling through
        this extension. Platform permissions and native configuration still apply. See
        the notification service's requirements in the user guide.

    Notification response handlers receive
    :class:`flet_notifications.NotificationEvent`. When a background action runs without
    the app UI, a native Dart handler persists the event for replay when the service
    next initializes; it does not execute Python in the background.

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
    extension. See :attr:`flet_notifications.AndroidOptions.icon` for the icon's
    requirements and how to bundle it.

    `None` uses the app's launcher icon, `"@mipmap/ic_launcher"`. Android draws the
    small icon from its transparency alone, so the launcher icon usually shows as a
    plain shape rather than your app's icon.
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

    Note:
        Used during initialization and by :meth:`request_permissions`. Requires Apple's
        critical-alert entitlement; this flag does not obtain that entitlement. See
        :attr:`flet_notifications.DarwinInterruptionLevel.CRITICAL`.
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

    The event includes the notification ID and application payload. Full-screen
    Android notification launches also use this handler.

    Note:
        When selecting a notification launches the app, this handler is called for it
        once the service initializes, so set it when creating the service. It is
        called once per launch; use it, for example, to route the app to the
        notification's content.
    """

    on_action: ft.EventHandler[NotificationEvent["LocalNotifications"]] | None = None
    """
    Called when the user selects a notification action button.

    Use :attr:`flet_notifications.NotificationEvent.action_id` to identify the button
    and :attr:`flet_notifications.NotificationEvent.input` for reply text.

    Note:
        - When an action launches the app, this handler is called for it once the
          service initializes, as with :attr:`on_tap`.
        - On Windows, the event's inherited `data` mapping contains reply values
          keyed by :attr:`flet_notifications.NotificationAction.id`. For an action
          with the ID `"reply"`, read `e.data["reply"]`. When exactly one value is
          returned, :attr:`flet_notifications.NotificationEvent.input` also contains
          that text.
        - Background Android/iOS actions are queued and replayed on the next service
          initialization; Python is not run in the background isolate.
    """

    on_dismiss: ft.EventHandler[NotificationEvent["LocalNotifications"]] | None = None
    """
    Called if the native backend reports a notification dismissal.

    Note:
        Dismissal reporting is not supported on Android, iOS, or macOS. Delivery on
        other platforms depends on native support; do not rely on a dismissal event
        for every notification that disappears.
    """

    async def _call(
        self,
        method_name: str,
        arguments: Any = None,
        timeout: float | None = None,
    ) -> Any:
        """Invoke a bridge method, raising its failures as `NotificationError`."""
        try:
            return await self._invoke_method(method_name, arguments, timeout=timeout)
        except RuntimeError as e:
            raise error_from_bridge(str(e)) from None

    async def initialize(self) -> None:
        """
        Initialize or reinitialize the native notification backend.

        The service initializes automatically, and other methods wait for that
        initialization. Call explicitly to retry a failed initialization or apply
        changed initialization properties. Initialization can request Apple permissions
        according to the service's permission flags.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call("initialize")

    async def show(
        self,
        id: int,
        title: str | None = None,
        body: str | None = None,
        payload: str = "",
        actions: list[NotificationAction] | None = None,
        options: NotificationOptions | None = None,
    ) -> None:
        """
        Display a local notification immediately.

        Note:
            Reusing an ID normally updates the existing notification, which is useful
            for :attr:`flet_notifications.AndroidOptions.progress` updates. Android's
            :attr:`flet_notifications.AndroidOptions.tag` also participates in
            identifying immediately displayed notifications. Visible content, action
            support, and alerting depend on the current platform and the user's
            notification settings. On Web, obtain browser permission with
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
            options: Additional per-platform details; see
                :class:`~flet_notifications.NotificationOptions`.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call(
            "show",
            {
                "id": id,
                "title": title,
                "body": body,
                "payload": payload,
                "actions": actions or None,
                "options": options,
            },
        )

    async def cancel(self, id: int, tag: str | None = None) -> None:
        """
        Remove a displayed notification and cancel its scheduled request.

        Note:
            On Android, a tag applies only to notifications posted immediately;
            scheduled alarms are identified by ID. On Windows, removal requires an MSIX
            package identity. Calling this method does not synthesize an
            :attr:`on_dismiss` event.

        Args:
            id: Identifier of the notification to remove.
            tag: Android tag supplied in :attr:`flet_notifications.AndroidOptions.tag`.
                Matches both tag and ID when provided; ignored on other platforms.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call("cancel", {"id": id, "tag": tag} if tag else {"id": id})

    async def cancel_all(self) -> None:
        """
        Remove all of the app's displayed and scheduled notifications.

        Note:
            To remove only undelivered requests, use :meth:`cancel_pending`. Windows
            removal requires an MSIX package identity. Does not remove Android channels
            or channel groups.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call("cancel_all")

    async def request_permissions(self) -> bool:
        """
        Request notification authorization where the platform supports a prompt.

        Note:
            On Android 13+, requests `POST_NOTIFICATIONS`; older Android versions do not
            show that runtime prompt. On iOS/macOS, requests the alert, sound, badge,
            and critical permissions selected by this service's corresponding
            `request_*_permission` properties. A previous denial may require the user to
            change system settings rather than displaying another prompt.

            On Web, requests browser notification permission. Call from a user
            interaction, such as an :attr:`flet.Button.on_click` handler, over HTTPS or
            a trusted localhost origin. An existing denial returns `False` without
            prompting again; the user must change the site's browser permissions.
            Dismissing the prompt without granting access also returns `False`.
            Unsupported browsers return `False`.

            On Windows and Linux, returns `True` without requesting or
            checking permission.

        Returns:
            Whether the native permission request succeeded, or `True` on platforms
            where no permission request is performed. It does not guarantee delivery
            through per-channel restrictions, Focus, or Do Not Disturb.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        # Permission dialogs can take a while; allow more than the default.
        return await self._call("request_permissions", timeout=300)

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
    ) -> None:
        """
        Schedule a notification for a date, a delay, or a recurring calendar match.

        Note:
            Supported only on Android, iOS, macOS, and Windows. Windows schedules a
            single
            delivery even when calendar components are supplied. Android needs the
            scheduling receivers and
            permissions described in the notification service requirements; restoring
            schedules after a reboot also requires the boot receiver.

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
                Naive datetimes are wall-clock times in the device timezone; aware
                datetimes preserve their exact instant. For calendar recurrence in a
                particular timezone, use a
                [`ZoneInfo`](https://docs.python.org/3/library/zoneinfo.html#zoneinfo.ZoneInfo)
                time zone, such as
                `datetime(2027, 1, 1, 9, tzinfo=ZoneInfo("Europe/Paris"))`; other
                values recur in the device timezone, which falls back to UTC if
                lookup fails. Native scheduling has at best second precision, and
                delay fractions are truncated to whole seconds.
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

        Raises:
            NotificationPermissionError: If an exact `schedule_mode` lacks Android
                exact-alarm access.
            NotificationError: If the bridge reports another failure.

        Example:
            ```python
            from datetime import datetime
            from zoneinfo import ZoneInfo

            import flet_notifications as ftn

            await notifications.schedule(
                id=2,
                when=datetime(2027, 1, 1, 9, 0, tzinfo=ZoneInfo("Europe/Paris")),
                title="Morning reminder",
                match_components=ftn.DateTimeComponents.TIME,
                schedule_mode=ftn.AndroidScheduleMode.INEXACT_ALLOW_WHILE_IDLE,
            )
            ```
        """
        await self._call(
            "schedule",
            {
                "id": id,
                "title": title,
                "body": body,
                "payload": payload,
                "actions": actions or None,
                **build_schedule_args(
                    when=when,
                    match_components=match_components,
                    schedule_mode=schedule_mode,
                ),
                "options": options,
            },
        )

    async def periodically_show(
        self,
        id: int,
        repeat_interval: RepeatInterval | ft.DurationValue,
        title: str | None = None,
        body: str | None = None,
        payload: str = "",
        actions: list[NotificationAction] | None = None,
        schedule_mode: AndroidScheduleMode = AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE,
        options: NotificationOptions | None = None,
    ) -> None:
        """
        Schedule a notification repeating after a fixed elapsed interval.

        For a specific local time such as 09:00 every day, use :meth:`schedule` with
        :class:`~flet_notifications.DateTimeComponents` instead.

        Note:
            - The first delivery is one interval after this call, not immediately.
            - Supported only on Android, iOS, and macOS. Android requires the scheduling
              setup described in the notification service requirements. Actual timing
              is subject to OS power management and alarm policies.

        Args:
            id: Notification identifier. Reuse it to update the same notification;
                on Android, a tag also participates in identifying immediately shown
                notifications. Native platforms can impose identifier range limits.
            repeat_interval: Standard repeat interval or a custom duration of at least
                one minute, such as `ft.Duration(minutes=15)`. Integer values are
                interpreted as milliseconds.
            title: Notification title. `None` omits the title.
            body: Notification body. `None` omits the body.
            payload: Application-defined string returned with tap and action events.
                The service does not interpret this value.
            actions: Action buttons; see :class:`~flet_notifications.NotificationAction`
                for platform support and background-response behavior.
            schedule_mode: Android alarm precision and idle-mode behavior; see
                :class:`~flet_notifications.AndroidScheduleMode`. Exact modes require
                the applicable exact-alarm access. Ignored on other platforms.
            options: Additional per-platform details; see
                :class:`~flet_notifications.NotificationOptions`.

        Raises:
            NotificationInvalidArgumentError: If `repeat_interval` is not a
                :class:`~flet_notifications.RepeatInterval`, :class:`~flet.Duration`,
                or integer, or if a custom duration is less than one minute.
            NotificationPermissionError: If an exact `schedule_mode` lacks Android
                exact-alarm access.
            NotificationError: If the bridge reports another failure.
        """
        await self._call(
            "periodically_show",
            {
                "id": id,
                "title": title,
                "body": body,
                "payload": payload,
                "actions": actions or None,
                **build_periodic_args(
                    repeat_interval=repeat_interval,
                    schedule_mode=schedule_mode,
                ),
                "options": options,
            },
        )

    async def cancel_pending(self) -> None:
        """
        Cancel all scheduled notifications without removing displayed ones.

        Note:
            Supported only on Android, iOS, and macOS. Other platforms report an
            unsupported
            operation. Use :meth:`cancel` to remove a specific pending request.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call("cancel_pending")

    async def get_pending_notifications(self) -> list[PendingNotification]:
        """
        Query notifications scheduled for future delivery.

        Note:
            Supported only on Android, iOS, macOS, and Windows. Windows query
            support depends on package identity. Unsupported queries can report a
            :class:`~flet_notifications.NotificationError`; an empty list is not a
            universal unsupported-platform response.

        Returns:
            Snapshots of pending requests. These do not include every platform detail
            and cannot be edited to change the native schedule.

        Raises:
            NotificationError: If the backend reports a failure or returns malformed
                query data.
        """
        return parse_query_list(
            await self._call("get_pending"),
            PendingNotification,
            defaults={"id": 0},
        )

    async def can_schedule_exact_notifications(self) -> bool:
        """
        Check Android's authorization to schedule exact alarms.

        Note:
            Android restricts exact alarms from Android 12 onward. This is separate from
            notification-display permission and channel settings.

        Returns:
            Whether the Android backend reports exact alarms are allowed. Returns `True`
            on non-Android platforms, where exact scheduling is not restricted.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        return await self._call("can_schedule_exact_notifications")

    async def request_exact_alarm_permission(self) -> bool:
        """
        Request Android exact-alarm access through system settings when needed.

        Use with the `SCHEDULE_EXACT_ALARM` manifest permission. This is especially
        relevant to apps targeting Android 13+ and running on Android 14+, where the
        permission may not be granted at installation. Exact-alarm access is separate
        from :meth:`request_permissions`.

        Returns:
            Whether access is granted after the request. Returns `True` on non-Android
            platforms, where exact scheduling is not restricted. A grant does not
            create a scheduled notification.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        return await self._call("request_exact_alarm_permission", timeout=300)

    # ── Channels (Android 8.0+) ─────────────────────────────────────────

    async def create_notification_channel(self, channel: NotificationChannel) -> None:
        """
        Create an Android notification channel or update its mutable details.

        Note:
            Applies on Android 8.0+. Existing channel sound, vibration, lights, and
            importance cannot be reset through this call. See
            :class:`~flet_notifications.NotificationChannel` for creation-time settings.
            Does nothing on other platforms, which have no channels.

        Args:
            channel: Channel declaration. Post notifications to it by passing its ID
                as :attr:`flet_notifications.AndroidOptions.channel`. Create its group
                first when a group ID is supplied.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call("create_notification_channel", channel)

    async def delete_notification_channel(self, channel_id: str) -> None:
        """
        Delete an Android notification channel on Android 8.0+.

        Note:
            This does not cancel pending schedules that still refer to the channel;
            cancel those separately if they should no longer deliver notifications.
            Does nothing on other platforms, which have no channels.

        Args:
            channel_id: Identifier of the channel to delete.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call("delete_notification_channel", {"channel_id": channel_id})

    async def get_notification_channels(self) -> list[NotificationChannel]:
        """
        Query the app's Android notification channels.

        Returns:
            Channel snapshots on supported Android versions, or an empty list on
            non-Android platforms. Returned values reflect the native channel settings,
            including changes made by the user.

        Raises:
            NotificationError: If the backend reports a failure or returns malformed
                query data.
        """
        return parse_query_list(
            await self._call("get_notification_channels"), NotificationChannel
        )

    # ── Foreground service (Android) ────────────────────────────────────

    async def start_foreground_service(
        self,
        id: int,
        title: str | None = None,
        body: str | None = None,
        payload: str = "",
        actions: list[NotificationAction] | None = None,
        options: NotificationOptions | None = None,
        start_type: AndroidServiceStartType | None = None,
        foreground_service_types: list[AndroidForegroundServiceType] | None = None,
    ) -> None:
        """
        Start an Android foreground service with a visible notification.

        Note:
            Requires a service declaration, appropriate foreground-service permissions,
            and types matching the actual work. See
            :class:`flet_notifications.AndroidForegroundServiceType` for the shared
            setup and each type's `pyproject.toml` entries and runtime requirements.
            Other platforms report an unsupported operation.

            This starts the plugin's native foreground service; it does not create a
            Python worker or guarantee that Android will keep the process alive
            indefinitely. Android's start restrictions and service time limits still
            apply. Use :meth:`stop_foreground_service` when the work is finished.

        Args:
            id: Nonzero identifier for the foreground-service notification.
            title: Notification title. `None` omits the title.
            body: Notification body. `None` omits the body.
            payload: Application-defined string returned with tap and action events.
                The service does not interpret this value.
            actions: Action buttons; see :class:`~flet_notifications.NotificationAction`
                for platform support and background-response behavior.
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
            NotificationInvalidArgumentError: If `id` is `0`.
            NotificationUnsupportedPlatformError: Outside Android.
            NotificationError: If the bridge reports another failure.
        """
        if id == 0:
            raise NotificationInvalidArgumentError(
                "foreground service id must be non-zero"
            )
        await self._call(
            "start_foreground_service",
            {
                "id": id,
                "title": title,
                "body": body,
                "payload": payload,
                "start_type": start_type,
                "foreground_service_types": foreground_service_types,
                "actions": actions or None,
                "options": options,
            },
        )

    async def stop_foreground_service(self) -> None:
        """
        Stop the Android foreground service started by this extension.

        Note:
            Removes the service's foreground notification. It does not terminate Python
            tasks you started; stop the associated application work yourself. Does
            nothing on other platforms, where no foreground service can run.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call("stop_foreground_service")

    # ── Probes & OS integration ─────────────────────────────────────────

    async def are_notifications_enabled(self) -> bool:
        """
        Check application-level notification authorization where supported.

        Note:
            On Android, queries whether the app's notifications are enabled. On
            iOS/macOS, includes provisional authorization, which permits quiet delivery.
            On Web, checks the current browser permission without displaying a prompt;
            denied, undecided, or unsupported notification access returns `False`.

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
        return await self._call("are_notifications_enabled")

    async def open_app_notification_settings(self) -> None:
        """
        Open the operating system's notification settings for this app.

        Note:
            On iOS, the plugin tries the app's notification settings and falls back to
            the app's general settings when necessary. Unsupported platforms can report
            an error. The bridge discards the native success flag, so a successful
            return does not confirm that a settings screen opened.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call("open_app_settings")

    async def get_active_notifications(self) -> list[ActiveNotification]:
        """
        Query delivered notifications that have not been dismissed or removed.

        Note:
            Supported only on Android 6.0+, iOS 10+, macOS 10.14+, and Windows with an
            MSIX
            package identity. The Windows backend returns an empty list without that
            identity. Unsupported platforms can report an error rather than returning an
            empty list.

        Returns:
            Snapshots of active notifications, with platform-dependent fields. Missing
            text values are represented as empty strings.

        Raises:
            NotificationError: If the backend reports a failure or returns malformed
                query data.
        """
        return parse_query_list(await self._call("get_active"), ActiveNotification)

    async def request_full_screen_intent_permission(self) -> bool:
        """
        Request access to Android full-screen notification intents.

        Note:
            On Android 14+, access can depend on the app's permitted use and user
            settings. Requires the `USE_FULL_SCREEN_INTENT` manifest permission. After
            obtaining access, enable
            :attr:`flet_notifications.AndroidOptions.full_screen_intent` on the
            notification. A grant does not guarantee full-screen presentation; Android
            may show a heads-up notification instead.

        Returns:
            Whether the Android backend reports access is granted; `False` on
            non-Android platforms.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        return await self._call("request_full_screen_intent", timeout=300)

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
        return await self._call("has_notification_policy_access")

    async def request_notification_policy_access(self) -> bool:
        """
        Open Android's notification-policy access settings when required.

        Note:
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
        return await self._call("request_notification_policy_access", timeout=300)

    # ── Channel groups (Android 8.0+) ───────────────────────────────────

    async def create_notification_channel_group(
        self, group_id: str, name: str, description: str = ""
    ) -> None:
        """
        Create a group organizing Android channels in system notification settings.

        Note:
            Supported only on Android 8.0+. This is distinct from grouping displayed
            notifications with :attr:`flet_notifications.AndroidOptions.group`. Create
            the group before creating channels that refer to its ID. Does nothing on
            other platforms, which have no channels.

        Args:
            group_id: Stable identifier for the channel group.
            name: User-visible group name.
            description: Optional explanation of the group, supported on Android 9.0+.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call(
            "create_notification_channel_group",
            {
                "group_id": group_id,
                "name": name,
                "description": description,
            },
        )

    async def delete_notification_channel_group(self, group_id: str) -> None:
        """
        Delete an Android notification-channel group and all its channels.

        Note:
            Supported only on Android 8.0+. This also removes channel configuration for
            the group's channels. Cancel unwanted pending notifications separately.
            Does nothing on other platforms, which have no channels.

        Args:
            group_id: Identifier of the group to delete.

        Raises:
            NotificationError: If the bridge reports initialization or operation
                failure.
        """
        await self._call(
            "delete_notification_channel_group",
            {"group_id": group_id},
        )
