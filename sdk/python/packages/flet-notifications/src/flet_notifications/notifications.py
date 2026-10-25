from datetime import datetime, timedelta
from typing import Any, TypeVar

import flet as ft
from flet.utils import from_dict
from flet_notifications.android import (
    AndroidForegroundServiceType,
    AndroidScheduleMode,
    AndroidServiceStartType,
    NotificationChannel,
)
from flet_notifications.events import NotificationActionEvent, NotificationEvent
from flet_notifications.exceptions import (
    NotificationException,
    NotificationInvalidArgumentException,
    NotificationUnsupportedPlatformException,
    error_from_bridge,
)
from flet_notifications.scheduling import (
    build_periodic_args,
    build_schedule_args,
)
from flet_notifications.types import (
    ActiveNotification,
    DateTimeComponents,
    NotificationAction,
    NotificationOptions,
    PendingNotification,
    RepeatInterval,
)
from flet_notifications.validation import (
    validate_arguments,
    validate_non_empty,
    validate_notification_id,
)
from flet_notifications.windows import WindowsProgress

__all__ = ["Notifications"]

_QueryItem = TypeVar("_QueryItem")


def parse_query_list(
    result: object,
    item_type: type[_QueryItem],
) -> list[_QueryItem]:
    """Reconstruct query snapshots without silently skipping malformed entries."""
    if not isinstance(result, list):
        raise NotificationException(
            f"Expected a list of {item_type.__name__}",
        )
    items = []
    for index, entry in enumerate(result):
        if not isinstance(entry, dict):
            raise NotificationException(
                f"Expected {item_type.__name__} mapping at index {index}",
            )
        try:
            items.append(from_dict(item_type, entry))
        except (TypeError, ValueError) as exc:
            raise NotificationException(
                f"Invalid {item_type.__name__} at index {index}: {exc}",
            ) from exc
    return items


@ft.control("Notifications")
class Notifications(ft.Service):
    """
    Provides native local notifications for Android, iOS, macOS, Windows, Linux,
    and Web.

    Create one service per page and keep its reference for sending notifications and
    handling responses. It registers with the page automatically and does not need to be
    added to the page's visual controls. The native backend initializes when the
    service reaches the client, and method calls wait for it to finish. Changing
    :attr:`android_default_icon` initializes it again with the new value; a failed
    initialization is retried on the next method call. Windows keeps the identity
    the app's notifications first registered with until the app exits, so changes
    to :attr:`windows_app_name`, :attr:`windows_app_user_model_id`, and
    :attr:`windows_guid` apply from its next launch.

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
            notifications = ftn.Notifications(
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

    android_default_icon: str = "flet_notifications_icon"
    """
    Default small Android notification icon.

    Supply a bundled drawable resource name, such as `"ic_stat_notify"`, without an
    extension. See :attr:`flet_notifications.AndroidOptions.icon` for the icon's
    requirements and how to bundle it.

    The default is a silhouette of the Flet logo that this extension provides. Android
    draws the small icon from its transparency alone, so use a silhouette of your own
    to show your app's brand instead.
    """

    windows_app_name: str | None = None
    """
    Name Windows shows for the app's notifications, and in its notification settings.

    `None` uses the app's product name, from its executable's version information.
    """

    windows_app_user_model_id: str | None = None
    """
    Windows AppUserModelID identifying the source of the app's notifications.

    Windows keeps notification settings and history per AppUserModelID, so apps must
    not share one. `None` derives one from the app's executable, such as
    `"Flet.myapp.3f2a9c1e"`, that is stable across launches and differs between apps.
    Set one when Windows should treat the app as the one with that ID, such as the ID
    of its Start menu shortcut or installer.

    Note:
        Windows shows the app's icon, from `flet build`, on its notifications, and
        keeps the icon it first showed for an AppUserModelID: after changing the app's
        icon, set a new ID to see the new one.
    """

    windows_guid: str | None = None
    """
    GUID of the component Windows activates when the user selects a notification.

    `None` derives one from :attr:`windows_app_user_model_id`, so it differs between
    apps.
    """

    on_tap: ft.EventHandler[NotificationEvent["Notifications"]] | None = None
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

    on_action: ft.EventHandler[NotificationActionEvent["Notifications"]] | None = None
    """
    Called when the user selects a notification action button.

    Its handler receives a :class:`flet_notifications.NotificationActionEvent`; use
    its :attr:`~flet_notifications.NotificationActionEvent.action_id` to identify
    the button and :attr:`~flet_notifications.NotificationActionEvent.input` for
    reply text.

    Note:
        - When an action launches the app, this handler is called for it once the
          service initializes, as with :attr:`on_tap`.
        - On Windows, the event's inherited `data` mapping contains reply values
          keyed by :attr:`flet_notifications.NotificationAction.id`. For an action
          with the ID `"reply"`, read `e.data["reply"]`. When exactly one value is
          returned,
          :attr:`flet_notifications.NotificationActionEvent.input` also contains
          that text.
        - Background Android/iOS actions are queued and replayed on the next service
          initialization; Python is not run in the background isolate.
    """

    def _require_platform(
        self, method: str, platforms: set[ft.PagePlatform], *, web: bool = False
    ) -> None:
        """
        Raise unless the app runs on one of `platforms`, or in a browser if `web`.

        Raises:
            NotificationUnsupportedPlatformException: Elsewhere, naming `method` and the
                platforms it is supported on.
        """
        page = self.page
        if web if page.web else page.platform in platforms:
            return

        _PLATFORM_NAMES = {
            ft.PagePlatform.ANDROID: "Android",
            ft.PagePlatform.ANDROID_TV: "Android",
            ft.PagePlatform.IOS: "iOS",
            ft.PagePlatform.MACOS: "macOS",
            ft.PagePlatform.WINDOWS: "Windows",
            ft.PagePlatform.LINUX: "Linux",
        }
        names = list(
            dict.fromkeys(n for p, n in _PLATFORM_NAMES.items() if p in platforms)
        )
        if web:
            names.append("the web")
        listed = (
            names[0] if len(names) == 1 else f"{', '.join(names[:-1])} and {names[-1]}"
        )
        raise NotificationUnsupportedPlatformException(
            f"{method}() is only supported on {listed}"
        )

    async def _call(self, method_name: str, arguments: Any = None) -> Any:
        """Invoke a bridge method, raising its failures as `NotificationException`."""
        try:
            return await self._invoke_method(method_name, arguments)
        except RuntimeError as e:
            raise error_from_bridge(str(e)) from None

    async def show(
        self,
        id: int,
        *,
        title: str | None = None,
        body: str | None = None,
        payload: str | None = None,
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
                The service does not interpret this value. `None` attaches no
                payload.
            actions: Action buttons; see :class:`flet_notifications.NotificationAction`
                for platform support and background-response behavior.
            options: Additional per-platform details; see
                :class:`~flet_notifications.NotificationOptions`.

        Raises:
            NotificationInvalidArgumentException: If `id` doesn't fit a 32-bit signed
                integer.
            NotificationInvalidArgumentException: If a value in `actions` or
                `options` is invalid, such as an empty action title or a progress
                value above its maximum.
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        validate_notification_id(id)
        validate_arguments(actions, options)
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

    async def cancel(self, id: int, *, tag: str | None = None) -> None:
        """
        Remove a displayed notification and cancel its scheduled request.

        Note:
            On Android, a tag applies only to notifications posted immediately;
            scheduled alarms are identified by ID. On Windows, removal requires an MSIX
            package identity.

        Args:
            id: Identifier of the notification to remove.
            tag: Android tag supplied in :attr:`flet_notifications.AndroidOptions.tag`.
                Matches both tag and ID when provided; ignored on other platforms.

        Raises:
            NotificationInvalidArgumentException: If `id` doesn't fit a 32-bit signed
                integer.
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        validate_notification_id(id)
        await self._call("cancel", {"id": id, "tag": tag} if tag else {"id": id})

    async def cancel_all(self) -> None:
        """
        Remove all of the app's displayed and scheduled notifications.

        Note:
            To remove only undelivered requests, use :meth:`cancel_all_pending`. Windows
            removal requires an MSIX package identity. Does not remove Android channels
            or channel groups.

        Raises:
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        await self._call("cancel_all")

    async def request_permissions(
        self,
        *,
        alert: bool = True,
        sound: bool = True,
        badge: bool = True,
        critical: bool = False,
        provisional: bool = False,
    ) -> bool:
        """
        Request notification authorization where the platform supports a prompt.

        The service never prompts on its own; call this when the app is ready to
        explain why it needs notifications.

        Note:
            - On Android 13+, requests `POST_NOTIFICATIONS`; older Android versions
              do not show that runtime prompt. On iOS/macOS, requests the kinds of
              authorization selected by the arguments. A previous denial may require
              the user to change system settings rather than displaying another prompt.

            - On Web, requests browser notification permission. Call from a user
              interaction, such as an :attr:`flet.Button.on_click` handler,
              over HTTPS or a trusted localhost origin. An existing denial returns
              `False` without prompting again; the user must change the site's
              browser permissions. Dismissing the prompt without granting access also
              returns `False`. Unsupported browsers return `False`.

            - On Windows and Linux, returns `True` without requesting or
              checking permission.

        Args:
            alert: Whether to request permission to display alerts. iOS/macOS only.
            sound: Whether to request permission to play sounds. Whether a sound
                plays also depends on
                :attr:`flet_notifications.DarwinOptions.present_sound`.
                **Has effect on iOS/macOS only**.
            badge: Whether to request permission to badge the app icon; set the
                value with :attr:`flet_notifications.DarwinOptions.badge_number`.
                **Has effect on iOS/macOS only**.
            critical: Whether to request permission for critical alerts, which sound
                through mute and Do Not Disturb. Requires Apple's critical-alert
                entitlement in the app; see
                :attr:`flet_notifications.DarwinInterruptionLevel.CRITICAL`.
                **Has effect on iOS/macOS only**.
            provisional: Whether to request provisional authorization instead of
                prompting: notifications are delivered quietly to Notification
                Center, where the user can keep or turn them off. No prompt is shown.
                **Has effect on iOS/macOS only**.

        Returns:
            Whether the native permission request succeeded, or `True` on platforms
                where no permission request is performed. It does not guarantee delivery
                through per-channel restrictions, Focus, or Do Not Disturb.

        Raises:
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        return await self._call(
            "request_permissions",
            {
                "alert": alert,
                "sound": sound,
                "badge": badge,
                "critical": critical,
                "provisional": provisional,
            },
        )

    async def schedule(
        self,
        id: int,
        *,
        when: datetime | timedelta,
        title: str | None = None,
        body: str | None = None,
        payload: str | None = None,
        actions: list[NotificationAction] | None = None,
        match_components: DateTimeComponents | None = None,
        options: NotificationOptions | None = None,
        schedule_mode: AndroidScheduleMode = (
            AndroidScheduleMode.INEXACT_ALLOW_WHILE_IDLE
        ),
    ) -> None:
        """
        Schedule a notification for a date, a delay, or a recurring calendar match.

        To repeat after a fixed elapsed interval rather than at a particular local
        time, use :meth:`periodically_show`.

        Note:
            - Supported on Android, iOS, macOS, and Windows. Windows delivers once,
              ignoring `match_components`.
            - On Android, schedules are restored after a reboot or an app update,
              through the `RECEIVE_BOOT_COMPLETED` permission flet-notifications adds
              by default.
            - iOS keeps at most 64 pending notifications per app. Check
              :meth:`get_pending_notifications` when scheduling many.

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
                The service does not interpret this value. `None` attaches no
                payload.
            actions: Action buttons; see :class:`~flet_notifications.NotificationAction`
                for platform support and background-response behavior.
            match_components: Calendar components used for recurrence on Android,
                iOS, and macOS. `None` schedules once. The first delivery is the next
                matching occurrence, which may precede the full date in `when`. Windows
                ignores this argument and schedules once.
            options: Additional per-platform details; see
                :class:`~flet_notifications.NotificationOptions`.
            schedule_mode: Android alarm precision and idle-mode behavior; see
                :class:`~flet_notifications.AndroidScheduleMode`. The default needs
                no special access, but Android may deliver the notification some
                minutes late. Exact modes deliver on time and require exact-alarm
                access. Ignored on other platforms.

        Raises:
            NotificationUnsupportedPlatformException: If called on Linux or the web,
                which don't support scheduled notifications.
            NotificationInvalidArgumentException: If `when` is not in the future.
            NotificationInvalidArgumentException: If `id` doesn't fit a 32-bit signed
                integer.
            NotificationInvalidArgumentException: If a value in `actions` or
                `options` is invalid.
            NotificationPermissionException: If an exact `schedule_mode` lacks Android
                exact-alarm access.
            NotificationException: If the bridge reports another failure.

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
            )
            ```
        """
        self._require_platform(
            "schedule",
            {
                ft.PagePlatform.ANDROID,
                ft.PagePlatform.ANDROID_TV,
                ft.PagePlatform.IOS,
                ft.PagePlatform.MACOS,
                ft.PagePlatform.WINDOWS,
            },
        )
        validate_notification_id(id)
        validate_arguments(actions, options)
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
        *,
        repeat_interval: RepeatInterval | ft.DurationValue,
        title: str | None = None,
        body: str | None = None,
        payload: str | None = None,
        actions: list[NotificationAction] | None = None,
        schedule_mode: AndroidScheduleMode = (
            AndroidScheduleMode.INEXACT_ALLOW_WHILE_IDLE
        ),
        options: NotificationOptions | None = None,
    ) -> None:
        """
        Schedule a notification repeating after a fixed elapsed interval.

        For a specific local time such as 09:00 every day, use :meth:`schedule` with
        :class:`~flet_notifications.DateTimeComponents` instead.

        Note:
            - The first delivery is one interval after this call, not immediately.
            - Supported on Android, iOS, and macOS. Actual timing is subject to the
              system's power management and alarm policies.
            - On Android, schedules are restored after a reboot or an app update,
              through the `RECEIVE_BOOT_COMPLETED` permission flet-notifications adds
              by default.

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
                The service does not interpret this value. `None` attaches no
                payload.
            actions: Action buttons; see :class:`~flet_notifications.NotificationAction`
                for platform support and background-response behavior.
            schedule_mode: Android alarm precision and idle-mode behavior. The
                default needs no special access, but Android may deliver the
                notification some minutes late. Exact modes deliver on time and
                require exact-alarm access. Ignored on other platforms.
            options: Additional per-platform details.

        Raises:
            NotificationUnsupportedPlatformException: If called on Windows, Linux or
                the web, which don't support repeating notifications.
            NotificationInvalidArgumentException: If `repeat_interval` isn't a
                :class:`~flet_notifications.RepeatInterval` or a duration of at
                least one minute.
            NotificationInvalidArgumentException: If `id` doesn't fit a 32-bit signed
                integer.
            NotificationInvalidArgumentException: If a value in `actions` or
                `options` is invalid.
            NotificationPermissionException: If an exact `schedule_mode` lacks Android
                exact-alarm access.
            NotificationException: If the bridge reports another failure.
        """
        self._require_platform(
            "periodically_show",
            {
                ft.PagePlatform.ANDROID,
                ft.PagePlatform.ANDROID_TV,
                ft.PagePlatform.IOS,
                ft.PagePlatform.MACOS,
            },
        )
        validate_notification_id(id)
        validate_arguments(actions, options)
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

    async def cancel_all_pending(self) -> None:
        """
        Cancel all scheduled notifications without removing displayed ones.

        Note:
            Supported on Android, iOS, and macOS. Does nothing on the web, which has
            no scheduled notifications. Use :meth:`cancel` to remove a specific
            pending request.

        Raises:
            NotificationUnsupportedPlatformException: If called on Windows, which
                can't cancel pending notifications all at once, or on Linux, which
                doesn't support scheduled notifications.
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        self._require_platform(
            "cancel_all_pending",
            {
                ft.PagePlatform.ANDROID,
                ft.PagePlatform.ANDROID_TV,
                ft.PagePlatform.IOS,
                ft.PagePlatform.MACOS,
            },
            web=True,
        )
        await self._call("cancel_all_pending")

    async def get_pending_notifications(self) -> list[PendingNotification]:
        """
        Query notifications scheduled for future delivery.

        Note:
            Supported on Android, iOS, macOS, and Windows, where the query depends on
            package identity. Returns an empty list on the web, which has no scheduled
            notifications.

        Returns:
            Snapshots of pending requests. These do not include every platform detail
                and cannot be edited to change the native schedule.

        Raises:
            NotificationUnsupportedPlatformException: If called on Linux, which doesn't
                support scheduled notifications.
            NotificationException: If the backend reports a failure or returns malformed
                query data.
        """
        self._require_platform(
            "get_pending_notifications",
            {
                ft.PagePlatform.ANDROID,
                ft.PagePlatform.ANDROID_TV,
                ft.PagePlatform.IOS,
                ft.PagePlatform.MACOS,
                ft.PagePlatform.WINDOWS,
            },
            web=True,
        )
        return parse_query_list(await self._call("get_pending"), PendingNotification)

    async def can_schedule_exact_alarms(self) -> bool:
        """
        Check Android's authorization to schedule exact alarms.

        Note:
            Android restricts exact alarms from Android 12 onward. This is separate from
            notification-display permission and channel settings.

        Returns:
            Whether the Android backend reports exact alarms are allowed. Returns `True`
                on non-Android platforms, where exact scheduling is not restricted.

        Raises:
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        return await self._call("can_schedule_exact_alarms")

    async def request_exact_alarm_permission(self) -> bool:
        """
        Request Android exact-alarm access through system settings when needed.

        Opens the system settings screen where the user can allow the app's alarms;
        it is not a dialog. Returns once the user leaves that screen. On Android 14+,
        the access is off until the user turns it on there. Exact-alarm access is
        separate from :meth:`request_permissions`.

        Note:
            Requires `SCHEDULE_EXACT_ALARM` in the app's permissions; without it, the
            settings screen cannot grant access and this returns `False`. See
            :class:`flet_notifications.AndroidScheduleMode` for what exact
            scheduling involves.

        Returns:
            Whether access is granted after the request. Returns `True` on non-Android
                platforms, where exact scheduling is not restricted. A grant does not
                create a scheduled notification.

        Raises:
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        return await self._call("request_exact_alarm_permission")

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
            NotificationInvalidArgumentException: If `channel` has an empty
                :attr:`~flet_notifications.NotificationChannel.id`.
            NotificationInvalidArgumentException: If `channel` has an empty
                :attr:`~flet_notifications.NotificationChannel.name`.
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        validate_arguments(channel)
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
            NotificationInvalidArgumentException: If `channel_id` is empty.
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        validate_non_empty(channel_id=channel_id)
        await self._call("delete_notification_channel", {"channel_id": channel_id})

    async def get_notification_channels(self) -> list[NotificationChannel]:
        """
        Query the app's Android notification channels.

        Returns:
            Channel snapshots on supported Android versions, or an empty list on
                non-Android platforms. Returned values reflect the native channel
                settings, including changes made by the user.

        Raises:
            NotificationException: If the backend reports a failure or returns malformed
                query data.
        """
        return parse_query_list(
            await self._call("get_notification_channels"), NotificationChannel
        )

    async def start_foreground_service(
        self,
        id: int,
        title: str | None = None,
        body: str | None = None,
        payload: str | None = None,
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

            This starts the plugin's native foreground service; it does not create a
            Python worker or guarantee that Android will keep the process alive
            indefinitely. Android's start restrictions and service time limits still
            apply. Use :meth:`stop_foreground_service` when the work is finished.

        Args:
            id: Nonzero identifier for the foreground-service notification.
            title: Notification title. `None` omits the title.
            body: Notification body. `None` omits the body.
            payload: Application-defined string returned with tap and action events.
                The service does not interpret this value. `None` attaches no
                payload.
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
            NotificationUnsupportedPlatformException: If called on a platform other
                than Android, where foreground services don't exist.
            NotificationInvalidArgumentException: If `id` is `0`.
            NotificationInvalidArgumentException: If `id` doesn't fit a 32-bit signed
                integer.
            NotificationInvalidArgumentException: If a value in `actions` or
                `options` is invalid.
            NotificationException: If the bridge reports another failure.
        """
        self._require_platform(
            "start_foreground_service",
            {ft.PagePlatform.ANDROID, ft.PagePlatform.ANDROID_TV},
        )
        if id == 0:
            raise NotificationInvalidArgumentException(
                "foreground service id must be non-zero"
            )
        validate_notification_id(id)
        validate_arguments(actions, options)
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
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        await self._call("stop_foreground_service")

    async def update_windows_progress(self, id: int, progress: WindowsProgress) -> bool:
        """
        Update the progress bar of a shown Windows notification in place.

        Unlike showing the notification again, the update doesn't pop the toast up
        again. The notification must already have been shown with
        :attr:`flet_notifications.WindowsOptions.progress`; to advance it, change
        the values of the same progress object and pass it here.

        Note:
            Windows only updates the bar itself and its label:

            - :attr:`~flet_notifications.WindowsProgress.value`,
              :attr:`~flet_notifications.WindowsProgress.max` and
              :attr:`~flet_notifications.WindowsProgress.indeterminate` apply.
            - :attr:`~flet_notifications.WindowsProgress.status` and
              :attr:`~flet_notifications.WindowsProgress.title` keep the values the
              notification was shown with; changes to them are ignored.
            - :attr:`~flet_notifications.WindowsProgress.label` can only be updated
              if the notification was shown with one, and setting it to `None`
              keeps the last label shown.

        Args:
            id: Identifier of the notification to update.
            progress: The progress to show.

        Returns:
            Whether the notification was updated; `False` when it is no longer
                shown, such as after the user dismissed it.

        Raises:
            NotificationUnsupportedPlatformException: If called on a platform other
                than Windows, including a web app opened on Windows.
            NotificationInvalidArgumentException: If `id` doesn't fit a 32-bit signed
                integer.
            NotificationInvalidArgumentException: If `progress` is invalid, such as a
                :attr:`~flet_notifications.WindowsProgress.value` above its
                :attr:`~flet_notifications.WindowsProgress.max`.
            NotificationException: If the bridge reports another failure.

        Example:
            ```python
            import flet_notifications as ftn

            progress = ftn.WindowsProgress(status="Downloading...", label="0/10")
            await notifications.show(
                id=7,
                title="report.pdf",
                options=ftn.NotificationOptions(
                    windows=ftn.WindowsOptions(progress=progress)
                ),
            )
            for step in range(1, 11):
                progress.value = step * 10
                progress.label = f"{step}/10"
                await notifications.update_windows_progress(7, progress)
            ```
        """
        self._require_platform("update_windows_progress", {ft.PagePlatform.WINDOWS})
        validate_notification_id(id)
        validate_arguments(progress)
        return await self._call(
            "update_windows_progress", {"id": id, "progress": progress}
        )

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
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        return await self._call("are_notifications_enabled")

    async def open_app_notification_settings(self) -> None:
        """
        Open the operating system's notification settings for this app.

        Note:
            On iOS, the plugin tries the app's notification settings and falls back to
            the app's general settings when necessary. The bridge discards the native
            success flag, so a successful return does not confirm that a settings
            screen opened.

        Raises:
            NotificationUnsupportedPlatformException: If called on Windows, Linux or
                the web, where the app's notification settings can't be opened.
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        self._require_platform(
            "open_app_notification_settings",
            {
                ft.PagePlatform.ANDROID,
                ft.PagePlatform.ANDROID_TV,
                ft.PagePlatform.IOS,
                ft.PagePlatform.MACOS,
            },
        )
        await self._call("open_app_settings")

    async def get_active_notifications(self) -> list[ActiveNotification]:
        """
        Query delivered notifications that have not been dismissed or removed.

        Note:
            Supported on Android 6.0+, iOS 10+, macOS 10.14+, the web, and Windows with
            an MSIX package identity. Without that identity, Windows returns an empty
            list.

        Returns:
            Snapshots of active notifications, with platform-dependent fields.
                Unavailable values are `None`.

        Raises:
            NotificationUnsupportedPlatformException: If called on Linux, which can't
                list the notifications it shows.
            NotificationException: If the backend reports a failure or returns malformed
                query data.
        """
        self._require_platform(
            "get_active_notifications",
            {
                ft.PagePlatform.ANDROID,
                ft.PagePlatform.ANDROID_TV,
                ft.PagePlatform.IOS,
                ft.PagePlatform.MACOS,
                ft.PagePlatform.WINDOWS,
            },
            web=True,
        )
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
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        return await self._call("request_full_screen_intent")

    async def has_notification_policy_access(self) -> bool:
        """
        Check whether Android has granted notification-policy access.

        This access is needed before creating a channel that requests Do Not Disturb
        bypass; it is distinct from notification-display permission.

        Returns:
            Whether access is granted on Android, or `False` on other platforms.

        Raises:
            NotificationException: If the bridge reports initialization or operation
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
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        return await self._call("request_notification_policy_access")

    async def create_notification_channel_group(
        self, group_id: str, *, name: str, description: str | None = None
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
            NotificationInvalidArgumentException: If `group_id` is empty.
            NotificationInvalidArgumentException: If `name` is empty.
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        validate_non_empty(group_id=group_id, name=name)
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
            NotificationInvalidArgumentException: If `group_id` is empty.
            NotificationException: If the bridge reports initialization or operation
                failure.
        """
        validate_non_empty(group_id=group_id)
        await self._call(
            "delete_notification_channel_group",
            {"group_id": group_id},
        )
