from datetime import datetime
from enum import Enum, IntFlag
from typing import Annotated

import flet as ft
from flet.utils.validation import V
from flet_notifications.android_styles import AndroidBitmap, AndroidStyle
from flet_notifications.validation import non_negative_duration

__all__ = [
    "AndroidAudioAttributesUsage",
    "AndroidForegroundServiceType",
    "AndroidGroup",
    "AndroidGroupAlertBehavior",
    "AndroidImportance",
    "AndroidNotificationCategory",
    "AndroidNotificationFlag",
    "AndroidOptions",
    "AndroidPriority",
    "AndroidProgress",
    "AndroidScheduleMode",
    "AndroidServiceStartType",
    "AndroidVisibility",
    "NotificationChannel",
]


class AndroidAudioAttributesUsage(Enum):
    """
    Intended use of an Android notification's sound.

    Note:
        Used by :attr:`flet_notifications.NotificationChannel.audio_attributes_usage`
        to help Android apply audio routing, volume, and interruption policies. This
        describes the sound; it does not grant permission to bypass the user's sound or
        Do Not Disturb settings. An existing channel retains its audio configuration.

    See Android's [audio usage
    reference](https://developer.android.com/reference/android/media/AudioAttributes).
    """

    ALARM = "alarm"
    """Audio for an alarm, such as a wake-up alarm."""

    ASSISTANCE_ACCESSIBILITY = "assistanceAccessibility"
    """Audio for accessibility assistance, such as a screen reader."""

    ASSISTANCE_NAVIGATION_GUIDANCE = "assistanceNavigationGuidance"
    """Spoken directions or other navigation guidance."""

    ASSISTANCE_SONIFICATION = "assistanceSonification"
    """Short sounds accompanying user-interface actions."""

    ASSISTANT = "assistant"
    """Responses from an assistant, such as spoken answers or reminders."""

    GAME = "game"
    """Audio associated with gameplay."""

    MEDIA = "media"
    """Media playback, such as music or video audio."""

    NOTIFICATION = "notification"
    """Audio drawing attention to a notification."""

    NOTIFICATION_EVENT = "notificationEvent"
    """Audio for an event that needs attention, such as a reminder."""

    NOTIFICATION_RINGTONE = "notificationRingtone"
    """Ringtone audio announcing an incoming call."""

    UNKNOWN = "unknown"
    """Audio whose intended use is unspecified."""

    VOICE_COMMUNICATION = "voiceCommunication"
    """Speech used for a telephone or VoIP conversation."""

    VOICE_COMMUNICATION_SIGNALLING = "voiceCommunicationSignalling"
    """Call-signalling sounds, such as a dial tone or busy tone."""


class AndroidNotificationFlag(IntFlag):
    """
    Additional behavior bits for an Android notification.

    Combine members with `|` and pass the result to
    :attr:`flet_notifications.AndroidOptions.additional_flags`.

    Note:
        These bits are added after the notification is built; they cannot clear flags
        set by other options. Android's notification permissions, channel settings, and
        platform restrictions still apply.

    Example:
        ```python
        import flet_notifications as ftn

        options = ftn.AndroidOptions(
            additional_flags=ftn.AndroidNotificationFlag.INSISTENT
            | ftn.AndroidNotificationFlag.NO_CLEAR
        )
        ```

    Deprecated flags and system-managed status flags are omitted. To start a foreground
    service, use :meth:`flet_notifications.Notifications.start_foreground_service`.
    See Android's [notification
    flags](https://developer.android.com/reference/android/app/Notification#flags).
    """

    NONE = 0
    """Adds no flags; flags set by other notification options remain in effect."""

    ONGOING_EVENT = 2
    """
    Marks the notification as representing work currently in progress, such as a call.

    Prefer :attr:`flet_notifications.AndroidOptions.ongoing` for this behavior.
    """

    INSISTENT = 4
    """
    Requests repeating audio until cancellation or the notification window is opened.

    Sound must be enabled and permitted by the notification's channel and user settings.
    """

    ONLY_ALERT_ONCE = 8
    """
    Alerts only when the notification is first posted, rather than on later updates.

    Also stops ongoing sound, vibration, or notification-LED alerting. Prefer
    :attr:`flet_notifications.AndroidOptions.only_alert_once` for this behavior.
    """

    AUTO_CANCEL = 16
    """
    Cancels the notification when the user taps it.

    Prefer :attr:`flet_notifications.AndroidOptions.auto_cancel` for this behavior.
    """

    NO_CLEAR = 32
    """
    Requests that the notification remain when the user presses Clear all.

    This does not prevent the app from cancelling the notification or guarantee that
    the notification cannot be dismissed individually.
    """

    LOCAL_ONLY = 256
    """
    Marks the notification as relevant only to the current device.

    Recommends that the notification not be bridged to other devices.
    """

    GROUP_SUMMARY = 512
    """
    Marks the notification as the summary of a group.

    Requires :attr:`flet_notifications.AndroidOptions.group`. Prefer setting
    :attr:`flet_notifications.AndroidGroup.summary` for this behavior.
    """


class AndroidScheduleMode(Enum):
    """
    How Android schedules the alarm that delivers a notification.

    Inexact modes need no special access but may deliver some minutes late, as
    Android batches alarms to save power. Exact modes deliver on time and need
    exact-alarm access:

    - Declare it in `pyproject.toml`:

      ```toml
      [tool.flet.android.permission]
      "android.permission.SCHEDULE_EXACT_ALARM" = true
      ```

    - On Android 14+, the access is off until the user turns it on in system
      settings. Check it with
      :meth:`flet_notifications.Notifications.can_schedule_exact_alarms`
      and open that settings screen with
      :meth:`flet_notifications.Notifications.request_exact_alarm_permission`.
    - Scheduling in an exact mode without the access raises
      :class:`flet_notifications.NotificationPermissionException`.
    - The user or the system can revoke the access at any time. Android then stops
      the app and cancels its future exact alarms, so those notifications are not
      delivered. Check the access when the app starts and reschedule once it is
      granted again. See Android's
      [exact alarm permission](https://developer.android.com/develop/background-work/services/alarms/schedule#exact-permission-declare)
      documentation.

    Note:
        Delivery in every mode remains subject to Android's alarm quotas and
        background-execution restrictions.
    """

    ALARM_CLOCK = "alarmClock"
    """
    Schedules an exact alarm-clock notification that can run during idle mode.

    Uses Android's alarm-clock mechanism and can appear in its next-alarm UI. Requires
    exact-alarm access.
    """

    EXACT = "exact"
    """
    Schedules for the requested time, with deferral possible during idle mode.

    Requires exact-alarm access.
    """

    EXACT_ALLOW_WHILE_IDLE = "exactAllowWhileIdle"
    """
    Schedules an exact alarm that can execute during low-power idle mode.

    Requires exact-alarm access.
    """

    INEXACT = "inexact"
    """
    Schedules approximately at the requested time, allowing idle-mode deferral.

    Does not require exact-alarm access.
    """

    INEXACT_ALLOW_WHILE_IDLE = "inexactAllowWhileIdle"
    """
    Schedules approximately at the requested time, including during idle mode.

    Does not require exact-alarm access; Android may batch or delay delivery. This is
    the default of :meth:`flet_notifications.Notifications.schedule` and
    :meth:`flet_notifications.Notifications.periodically_show`.
    """


class AndroidImportance(Enum):
    """
    Importance of an Android notification channel on Android 8.0 and later.

    Controls how prominently notifications interrupt the user. After a channel is
    created, its importance is controlled by the user in system settings; posting
    another notification does not override that choice. Use
    :class:`~flet_notifications.AndroidPriority` for Android 7.1 and earlier.
    """

    UNSPECIFIED = "unspecified"
    """
    Sentinel indicating that no importance has been specified.

    Maps to Android's `IMPORTANCE_UNSPECIFIED`. It is not an importance level for
    creating a new channel; choose an explicit level instead.
    """

    MIN = "min"
    """Shows notifications quietly, with minimal prominence and no status-bar icon."""

    NONE = "none"
    """Disables notifications from the channel."""

    LOW = "low"
    """Shows notifications without sound."""

    DEFAULT = "default"
    """Uses normal prominence, including sound when enabled for the channel."""

    HIGH = "high"
    """Uses high prominence, including sound and a heads-up display when allowed."""

    MAX = "max"
    """
    Maps to Android's maximum-importance constant.

    Android documents this level as unused; use :attr:`HIGH` for urgent channels.
    """


class AndroidGroupAlertBehavior(Enum):
    """
    Which Android notifications in a group may play sound or vibrate.

    This controls alerting, not whether a notification is visible. Apply the same
    behavior to the group's children and summary for consistent results.
    """

    ALL = "all"
    """Allows both the group summary and child notifications to alert."""

    SUMMARY = "summary"
    """Allows only the group summary to alert; silences its children."""

    CHILDREN = "children"
    """Allows only child notifications to alert; silences the group summary."""


class AndroidNotificationCategory(Enum):
    """
    Semantic category Android uses to classify and rank a notification.

    Set :attr:`~flet_notifications.AndroidOptions.category`. Category describes
    content; it does not grant permissions or change channel importance.
    """

    ALARM = "alarm"
    """Alarm or timer requiring attention."""

    CALL = "call"
    """Incoming voice or video call, or a similar live communication request."""

    EMAIL = "email"
    """Incoming email or another asynchronous bulk message."""

    ERROR = "error"
    """Failure in a background operation or authentication flow."""

    EVENT = "event"
    """Calendar event."""

    LOCATION_SHARING = "locationSharing"
    """Temporary location-sharing activity."""

    MESSAGE = "message"
    """Incoming direct message, such as SMS or a chat message."""

    MISSED_CALL = "missedCall"
    """Missed voice or video call."""

    NAVIGATION = "navigation"
    """Turn-by-turn navigation instruction."""

    PROGRESS = "progress"
    """Progress of a long-running background operation."""

    PROMO = "promo"
    """Promotion or advertisement."""

    RECOMMENDATION = "recommendation"
    """Timely recommendation for a specific item, such as a news story."""

    REMINDER = "reminder"
    """Reminder scheduled by the user."""

    SERVICE = "service"
    """Indication of a running background service."""

    SOCIAL = "social"
    """Social-network or sharing update."""

    STATUS = "status"
    """Ongoing device or contextual status information."""

    STOPWATCH = "stopwatch"
    """Running stopwatch."""

    SYSTEM = "system"
    """System or device-status update. Reserved for system use."""

    TRANSPORT = "transport"
    """Media playback or transport controls."""

    WORKOUT = "workout"
    """Tracking of the user's workout."""


class AndroidServiceStartType(Enum):
    """
    Android restart policy for the extension's foreground service.

    Note:
        Used by :meth:`flet_notifications.Notifications.start_foreground_service`.
        These policies govern native service recreation, not Python task restart.
        Android's foreground-service start restrictions still apply.
    """

    START_STICKY_COMPATIBILITY = "startStickyCompatibility"
    """
    Uses the compatibility form of Android's sticky-service policy.

    Unlike :attr:`START_STICKY`, it does not guarantee a restart callback after
    the service process is killed.
    """

    START_STICKY = "startSticky"
    """
    Asks Android to recreate the service after its process is killed.

    The previous start intent is not retained; a recreated service may receive
    a null intent. This policy does not guarantee uninterrupted execution.
    """

    START_NOT_STICKY = "startNotSticky"
    """
    Doesn't recreate a killed service unless there are pending start requests.

    The app must explicitly start new work when appropriate.
    """

    START_REDELIVER_INTENT = "startRedeliverIntent"
    """
    Asks Android to recreate a killed service and redeliver its last start intent.

    Application work must tolerate being restarted or delivered again.
    """


class AndroidForegroundServiceType(Enum):
    """
    Kind of work performed by an Android foreground service.

    Used by :meth:`flet_notifications.Notifications.start_foreground_service`. Each
    member below includes its `pyproject.toml` entries and any additional runtime or
    eligibility requirements. The type-specific foreground-service permissions are
    required when targeting Android 14+.

    Start with this shared configuration, then merge the entries for the
    selected member into the same service and permission tables:

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    exported = false

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE" = true
    ```

    Do not repeat a TOML table header when combining examples. When using more than one
    service type, combine the manifest names with `|`, for example
    `foregroundServiceType = "location|mediaPlayback"`, and include the permissions and
    prerequisites for every selected type. Pass the matching enum members to the
    method's
    [`foreground_service_types`][flet_notifications.Notifications.start_foreground_service]
    argument.

    Note:
        Manifest declarations do not grant runtime permissions. Obtain any required
        runtime grants or consent before starting. Selecting a type does not start
        camera, recording, location, or other application work, and does not remove
        Android's background-start or execution-time restrictions.

    See the [Android service configuration guide](/docs/publish/android#services) for
    how these entries map to the Android manifest.
    """  # noqa: E501

    CAMERA = "camera"
    """
    Camera access while performing foreground-service work.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "camera"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_CAMERA" = true
    "android.permission.CAMERA" = true
    ```

    Note:
        Obtain the `CAMERA` runtime grant before starting. While-in-use restrictions
        usually require starting while the app is visible; background and boot starts
        are restricted. Declaring `CAMERA` in this file does not grant access.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#camera)
    for this type.
    """  # noqa: E501

    CONNECTED_DEVICE = "connectedDevice"
    """
    Interaction with an external device, such as a Bluetooth accessory.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`. This example uses
    Bluetooth; adapt its transport permission to your use case.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "connectedDevice"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_CONNECTED_DEVICE" = true
    "android.permission.BLUETOOTH_CONNECT" = true
    ```

    Note:
        This example is for a Bluetooth connection on Android 12+. Obtain the
        `BLUETOOTH_CONNECT` runtime grant before starting. Other operations may need
        `BLUETOOTH_SCAN` or `BLUETOOTH_ADVERTISE` instead.

    Note:
        For other transports, satisfy the applicable prerequisite: a declared network,
        Wi-Fi, NFC, or infrared permission; a granted UWB permission; or USB device
        permission obtained through Android's USB permission dialog. Use the permissions
        for the transport your app actually uses.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#connected-device)
    for this type.
    """  # noqa: E501

    DATA_SYNC = "dataSync"
    """
    Data transfer or processing, such as upload, download, backup, or import.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "dataSync"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_DATA_SYNC" = true
    ```

    Note:
        This type has no additional type-specific runtime permission prerequisite.
        Access to the actual data or network may require other permissions. Apps
        targeting Android 15+ cannot start this type from a boot-completed receiver;
        Android also applies execution time limits.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#data-sync)
    for this type.
    """  # noqa: E501

    HEALTH = "health"
    """
    Health or fitness work, such as tracking an exercise session.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`. This example uses activity
    recognition; adapt its sensor permission to your use case.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "health"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_HEALTH" = true
    "android.permission.ACTIVITY_RECOGNITION" = true
    ```

    This example is for activity recognition. Obtain the `ACTIVITY_RECOGNITION` runtime
    grant before starting.

    Other health workloads can qualify through `HIGH_SAMPLING_RATE_SENSORS` or an
    appropriate sensor permission. Body-sensor access uses `BODY_SENSORS` on API 35 and
    earlier; newer health access can use `READ_HEART_RATE`, `READ_SKIN_TEMPERATURE`, or
    `READ_OXYGEN_SATURATION`. Declare and request the permissions matching your sensor
    and Android version, rather than adding all of them.

    Note:
        For body-sensor use subject to while-in-use restrictions, background access also
        needs `BODY_SENSORS_BACKGROUND` on API 33–35 or `READ_HEALTH_DATA_IN_BACKGROUND`
        on API 36+, as applicable.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#health)
    for this type.
    """  # noqa: E501

    LOCATION = "location"
    """
    Ongoing location work, such as navigation or location sharing.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "location"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_LOCATION" = true
    "android.permission.ACCESS_COARSE_LOCATION" = true
    "android.permission.ACCESS_FINE_LOCATION" = true
    ```

    The user must enable device location services and grant coarse or fine location
    access before the service starts. Request coarse and fine together when precise
    location is needed; approximate access may be sufficient for your use case.

    Note:
        While-in-use restrictions usually require starting while the app is visible.
        Starting from the background requires `ACCESS_BACKGROUND_LOCATION` where
        applicable, as well as satisfying Android's foreground-service start rules. The
        block above does not request background location.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#location)
    for this type.
    """  # noqa: E501

    MEDIA_PLAYBACK = "mediaPlayback"
    """
    Ongoing audio or video playback.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "mediaPlayback"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_MEDIA_PLAYBACK" = true
    ```

    Note:
        This type has no additional type-specific runtime permission prerequisite. It
        does not start media playback itself. Apps targeting Android 15+ cannot start
        this type from a boot-completed receiver.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#media)
    for this type.
    """  # noqa: E501

    MEDIA_PROJECTION = "mediaProjection"
    """
    Screen capture or projection of device content.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "mediaProjection"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_MEDIA_PROJECTION" = true
    ```

    Note:
        Obtain the user's screen-capture consent through Android's
        `MediaProjectionManager.createScreenCaptureIntent()` flow before starting the
        service. A manifest permission cannot replace this consent. This extension does
        not expose that flow; the component performing screen capture must obtain it.
        Apps targeting Android 15+ cannot start this type from a boot-completed
        receiver.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#media-projection)
    for this type.
    """  # noqa: E501

    MICROPHONE = "microphone"
    """
    Ongoing microphone capture or audio recording.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "microphone"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_MICROPHONE" = true
    "android.permission.RECORD_AUDIO" = true
    ```

    Note:
        Obtain the `RECORD_AUDIO` runtime grant before starting. While-in-use
        restrictions usually require starting while the app is visible; background and
        boot starts are restricted. Declaring the permission does not start recording or
        grant microphone access.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#microphone)
    for this type.
    """  # noqa: E501

    PHONE_CALL = "phoneCall"
    """
    Continuation of a voice or video call.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`. This example is for a
    self-managed calling app.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "phoneCall"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_PHONE_CALL" = true
    "android.permission.MANAGE_OWN_CALLS" = true
    ```

    This example is for a self-managed calling app using Android's `ConnectionService`
    APIs and declaring `MANAGE_OWN_CALLS`. Alternatively, the app can qualify by holding
    the default-dialer role. Adding this block does not implement calling or obtain that
    role.

    Note:
        Apps targeting Android 15+ cannot start this type from a boot-completed
        receiver.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#phone-call)
    for this type.
    """  # noqa: E501

    REMOTE_MESSAGING = "remoteMessaging"
    """
    Transfer of text messages between devices for messaging continuity.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "remoteMessaging"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_REMOTE_MESSAGING" = true
    ```

    Note:
        This type has no additional type-specific runtime permission prerequisite. Use
        it for continuity of messaging between devices, rather than ordinary local
        notifications or an incoming push message.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#remote-messaging)
    for this type.
    """  # noqa: E501

    SHORT_SERVICE = "shortService"
    """
    Short, critical work subject to Android's short-service time limit.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "shortService"
    ```

    No type-specific foreground-service permission is required; the shared
    `FOREGROUND_SERVICE` permission is still needed.

    Note:
        Android limits this type to about three minutes and does not support sticky
        restart behavior. Use
        :attr:`flet_notifications.AndroidServiceStartType.START_NOT_STICKY` and call
        :meth:`flet_notifications.Notifications.stop_foreground_service` before the
        deadline. This type cannot start another foreground service. If combined with
        another service type, Android ignores `shortService` and applies the other
        type's requirements.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#short-service)
    for this type.
    """  # noqa: E501

    SPECIAL_USE = "specialUse"
    """
    Qualifying foreground work not covered by another service type.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "specialUse"

    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService".property]
    "android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE" = "Describe the service's actual work"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_SPECIAL_USE" = true
    ```

    Note:
        Replace the subtype description with the specific work your service performs and
        why it needs this type. Android requires this service property; Google Play
        reviews the declared use case. This type has no additional type-specific runtime
        permission prerequisite and is not a substitute for another type that already
        describes the work.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#special-use)
    for this type.
    """  # noqa: E501

    SYSTEM_EXEMPTED = "systemExempted"
    """
    System integration work that meets Android's exemption criteria.

    Merge these entries with the shared configuration in
    :class:`flet_notifications.AndroidForegroundServiceType`.

    ```toml
    [tool.flet.android.service."com.dexterous.flutterlocalnotifications.ForegroundService"]
    foregroundServiceType = "systemExempted"

    [tool.flet.android.permission]
    "android.permission.FOREGROUND_SERVICE_SYSTEM_EXEMPTED" = true
    ```

    Note:
        The app must independently meet Android's eligibility criteria, such as being a
        qualifying device-management app, a configured VPN, or holding an applicable
        exact-alarm permission for the permitted use case. Declaring the permission
        alone does not make the app eligible; Android rejects this type for ineligible
        apps. Ordinary applications cannot select it to bypass limits.

    See [Android's
    requirements](https://developer.android.com/develop/background-work/services/fgs/service-types#system-exempted)
    for this type.
    """  # noqa: E501


class AndroidPriority(Enum):
    """
    Notification priority on Android 7.1 and earlier.

    Note:
        On Android 8.0 and later, channel :class:`~flet_notifications.AndroidImportance`
        determines interruption behavior instead. Priority is a presentation hint; it
        does not override the user's notification preferences.
    """

    MIN = "min"
    """Uses the lowest priority for information that does not need attention."""

    LOW = "low"
    """Uses low priority for non-urgent background information."""

    DEFAULT = "default"
    """Uses normal priority for ordinary notifications."""

    HIGH = "high"
    """Uses high priority for time-sensitive information."""

    MAX = "max"
    """Uses the highest priority for critical, immediate information."""


class AndroidVisibility(Enum):
    """
    How much Android notification content may appear on a secure lock screen.

    The user's lock-screen settings may further restrict visibility.
    """

    PUBLIC = "public"
    """Allows the entire notification to appear on any lock screen."""

    PRIVATE = "private"
    """
    Shows the notification while concealing sensitive content on secure lockscreens.
    """

    SECRET = "secret"
    """Hides the notification entirely on a secure lock screen."""


@ft.value(kw_only=True)
class NotificationChannel:
    """
    Android notification channel grouping notifications with shared behavior.

    Pass it as :attr:`flet_notifications.AndroidOptions.channel` to create the channel
    when a notification is first posted to it, or create it upfront with
    :meth:`flet_notifications.Notifications.create_notification_channel` and pass
    its :attr:`id` instead. Users manage channel preferences independently in Android
    settings. Sound, vibration, lights, and importance cannot be reset by posting
    another notification or recreating the same channel; use a new ID for a different
    configuration.

    Note:
        Channels exist on Android 8.0+. On earlier versions, the channel's sound,
        vibration, lights, and importance apply to each notification posted with it.

    Raises:
        ValueError: If :attr:`id` or :attr:`name` is empty.
    """

    id: Annotated[str, V.non_empty()]
    """Nonempty, stable channel identifier used when posting notifications."""

    name: Annotated[str, V.non_empty()]
    """Nonempty, user-visible channel name displayed in Android settings."""

    description: str | None = None
    """
    User-visible explanation of the notifications delivered through this channel.

    `None` shows no description.
    """

    group_id: str | None = None
    """
    ID of the notification-channel group containing this channel.

    Create the group first with
    :meth:`flet_notifications.Notifications.create_notification_channel_group`.
    This organizes channels in settings; it does not group notifications in the tray.
    """

    importance: AndroidImportance = AndroidImportance.DEFAULT
    """
    Initial channel importance.

    The user can change it after creation. See
    :class:`flet_notifications.AndroidImportance` for the interruption behavior of each
    level.
    """

    bypass_dnd: bool = False
    """
    Whether the channel should attempt to bypass Do Not Disturb.

    Note:
        Obtain notification-policy access with
        :meth:`flet_notifications.Notifications.request_notification_policy_access`
        before creating the channel; otherwise Android ignores the request.
    """

    play_sound: bool = True
    """
    Whether notifications in the channel play sound.

    Note:
        Fixed at channel creation. Use :attr:`sound` to choose a custom sound.
    """

    sound: str | None = None
    """
    Sound resource name or `content://` / `file://` URI on the Android device.

    A raw resource name, such as `"alert"`, refers to a file in the app's
    `res/raw` resources and omits the file extension. Add the file with the
    [`res_dir`](https://flet.dev/docs/publish/android#resources) build setting,
    for example as `raw/alert.mp3`.

    Note:
        Requires :attr:`play_sound`. `None` uses the default notification sound.
        Fixed at channel creation; changing this value does not replace an existing
        channel's sound.

        A `file://` URI of a file in the app's private storage is stored but not
        played, because the system cannot read the file.
    """

    enable_vibration: bool = True
    """
    Whether notifications in the channel vibrate.

    Note:
        Requires the Android `VIBRATE` permission. Fixed at channel creation.
    """

    vibration_pattern: list[int] | None = None
    """
    Alternating delay and vibration durations, in milliseconds.

    Note:
        For example, `[0, 200, 100, 200]` starts immediately and vibrates twice.
        Requires :attr:`enable_vibration`; fixed at channel creation.
    """

    show_badge: bool = True
    """
    Whether notifications may contribute launcher badges.

    Note:
        Requires support from the launcher and is subject to user settings.
    """

    enable_lights: bool = False
    """
    Whether to use the notification LED on supported devices.

    Note:
        Fixed at channel creation.
    """

    led_color: ft.ColorValue | None = None
    """
    LED color used when :attr:`enable_lights` is enabled.

    Note:
        Accepts concrete Flet color names and hexadecimal colors. Theme-dependent colors
        cannot be resolved by this headless service. Fixed at channel creation.
    """

    audio_attributes_usage: AndroidAudioAttributesUsage = (
        AndroidAudioAttributesUsage.NOTIFICATION
    )
    """
    Intended use of the channel's sound.

    Helps Android select audio routing, volume, and interruption policies. It does not
    enable sound when :attr:`play_sound` is `False` or grant access to bypass Do Not
    Disturb.

    Note:
        Fixed at channel creation.
    """


@ft.value(kw_only=True)
class AndroidProgress:
    """
    Progress bar shown in an Android notification.

    Set it as :attr:`flet_notifications.AndroidOptions.progress`. To advance the bar,
    show the notification again with the same ID and an updated :attr:`value`;
    combine with :attr:`flet_notifications.AndroidOptions.only_alert_once` to avoid
    alerting on each update.
    """

    value: Annotated[int, V.ge(0), V.le_field("max")] = 0
    """Current progress, between `0` and :attr:`max`."""

    max: Annotated[int, V.gt(0)] = 100
    """Value at which the progress bar is full."""

    indeterminate: bool = False
    """
    Whether to show ongoing activity without a known completion amount.

    When `True`, :attr:`value` and :attr:`max` are ignored.
    """


@ft.value(kw_only=True)
class AndroidGroup:
    """
    Group of related notifications bundled together in the Android notification tray.

    Set it as :attr:`flet_notifications.AndroidOptions.group`. Notifications sharing a
    :attr:`key` are bundled; one of them can act as the group's summary. This is
    distinct from a notification-channel group and from Apple threads (see
    :attr:`flet_notifications.DarwinOptions.thread_identifier`).
    """

    key: Annotated[str, V.non_empty()]
    """Identifier shared by every notification in the group."""

    summary: bool = False
    """Whether this notification summarizes the other notifications in the group."""

    alert_behavior: AndroidGroupAlertBehavior = AndroidGroupAlertBehavior.ALL
    """
    Which members of the group may sound or vibrate.

    Apply the same behavior to the group's children and summary for consistent results.
    """


@ft.value(kw_only=True)
class AndroidOptions:
    """
    Android-specific notification settings.

    Importance, sound, vibration, lights, and badge behavior belong to the
    notification's :attr:`channel`; see
    :class:`~flet_notifications.NotificationChannel`.
    """

    channel: NotificationChannel | str | None = None
    """
    Channel the notification is posted to.

    Pass a :class:`~flet_notifications.NotificationChannel` to create the channel on
    first use, or the ID of a channel created earlier with
    :meth:`flet_notifications.Notifications.create_notification_channel`. A
    missing channel referenced only by ID is created with the name `"Notifications"`
    and default settings. `None` uses the extension's default channel.

    Note:
        Before Android 8.0, which has no channels, the channel's sound, vibration,
        lights, and importance apply to the individual notification.
    """

    style: AndroidStyle | None = None
    """
    Expanded layout of the notification; see :class:`~flet_notifications.AndroidStyle`.

    `None` uses the standard layout.
    """

    progress: AndroidProgress | None = None
    """
    Progress bar shown in the notification.

    `None` shows no progress bar.
    """

    group: AndroidGroup | None = None
    """
    Group this notification belongs to.

    `None` leaves the notification ungrouped.
    """

    icon: str | None = None
    """
    Bundled drawable resource name for this notification's small icon.

    Supply the resource name without a file extension, such as `"ic_stat_notify"`.
    `None` uses :attr:`flet_notifications.Notifications.android_default_icon`.

    Note:
        Use a white silhouette on a transparent background, with resources sized for
        the supported screen densities. Android Studio's
        [notification icon wizard](https://developer.android.com/studio/write/create-app-icons#create-notification)
        generates the appropriate drawable variants. Android uses the icon's alpha
        channel to determine its visible shape; an opaque background can appear as a
        solid block.

        Add the drawable with the
        [`res_dir`](https://flet.dev/docs/publish/android#resources) build
        setting, for example as `drawable/ic_stat_notify.png`. Bundled resources
        exist only in apps built with
        [`flet build`](https://flet.dev/docs/cli/flet-build/) or
        [`flet debug`](https://flet.dev/docs/cli/flet-debug/); under
        [`flet run`](https://flet.dev/docs/cli/flet-run/), a missing icon raises
        :class:`flet_notifications.NotificationException`.
    """

    priority: AndroidPriority | None = None
    """
    Notification priority.

    Note:
        Used on Android 7.1 and earlier. On Android 8.0+, the :attr:`channel`'s
        :attr:`~flet_notifications.NotificationChannel.importance` applies instead.
    """

    auto_cancel: bool | None = None
    """Whether tapping the notification automatically dismisses it."""

    ongoing: bool | None = None
    """
    Whether to mark the notification as an ongoing activity.

    Note:
        Android controls whether the user can dismiss ongoing notifications; this does
        not start a foreground service.
    """

    silent: bool | None = None
    """
    Whether to suppress sound and vibration for this notification.

    This is a per-notification setting, distinct from changing the channel's sound and
    vibration configuration.
    """

    color: ft.ColorValue | None = None
    """
    Android notification accent color.

    Accepts Flet color names and hexadecimal colors. Theme-dependent colors, such as
    `ft.Colors.PRIMARY`, cannot be resolved by this headless service.
    """

    colorized: bool | None = None
    """
    Whether to use :attr:`color` for the notification background.

    Note:
        When disabled, the color accents the app icon. Android usually restricts
        background coloring to foreground-service notifications.
    """

    large_icon: AndroidBitmap | None = None
    """
    Large image shown beside the notification content, such as a contact photo.

    `None` shows no large icon.
    """

    only_alert_once: bool | None = None
    """
    Whether sound, vibration, and ticker alert only on the first display.

    Enable when repeatedly updating the same notification, such as a progress
    notification, without alerting on each update.
    """

    show_timestamp: bool | None = None
    """
    Whether to display the notification timestamp.

    Set :attr:`timestamp` to override the displayed time.
    """

    timestamp: datetime | None = None
    """
    Time displayed on the notification.

    When `None`, uses the notification's posting time. This does not schedule delivery;
    use :meth:`flet_notifications.Notifications.schedule` for that.

    Timezone-aware values preserve their instant. A naive datetime is interpreted in
    the Python host's local timezone.
    """

    uses_chronometer: bool | None = None
    """
    Whether to show elapsed time from :attr:`timestamp` instead of a timestamp.

    Android updates the minutes and seconds automatically, which is useful for ongoing
    calls or timers.
    """

    chronometer_count_down: bool | None = None
    """
    Whether the chronometer counts down rather than up.

    Note:
        Supported only on Android 7.0+. Requires :attr:`uses_chronometer` to be enabled.
    """

    sub_text: str | None = None
    """
    Supplementary information displayed in the notification template.

    Note:
        Android 7.0+ places this in the header. Earlier versions use the same line as
        the progress bar, so avoid using both on those versions.
    """

    badge_number: Annotated[int | None, V.ge(0)] = None
    """
    Notification count displayed by launchers that support badge numbers.

    Note:
        Ignored when the launcher does not support this feature.
    """

    visibility: AndroidVisibility | None = None
    """
    How much content may appear on a secure lock screen.

    `None` leaves the choice to Android. See
    :class:`flet_notifications.AndroidVisibility`.
    """

    timeout_after: Annotated[ft.DurationValue | None, non_negative_duration()] = None
    """
    Time after posting before Android cancels the notification.

    `None` does not request automatic cancellation after a timeout.
    """

    category: AndroidNotificationCategory | None = None
    """
    Semantic category used by Android to rank and filter notifications.

    See :class:`~flet_notifications.AndroidNotificationCategory` for the supported
    categories. This does not change the notification channel's importance.
    """

    full_screen_intent: bool | None = None
    """
    Whether to request full-screen presentation when the notification arrives.

    Note:
        Requires Android manifest configuration and, on Android 14+, full-screen-intent
        access. See
        :meth:`flet_notifications.Notifications.request_full_screen_intent_permission`.
        Android may show a heads-up notification instead. A full-screen launch is
        reported through :attr:`flet_notifications.Notifications.on_tap`.
    """

    shortcut_id: str | None = None
    """
    ID of a published, long-lived sharing shortcut linked to the notification.

    Note:
        On Android 11+, this can help a messaging notification appear in the
        conversation section. This extension does not create the shortcut.
    """

    additional_flags: AndroidNotificationFlag | int | None = None
    """
    Additional native Android notification flags, combined using `|`.

    For example, combine :attr:`flet_notifications.AndroidNotificationFlag.INSISTENT`
    and :attr:`flet_notifications.AndroidNotificationFlag.NO_CLEAR` to request repeating
    audio and retention when the user presses Clear all.

    Note:
        Android may restrict the effect of individual flags.

    A raw integer bitmask is also accepted for Android flags not represented by
    :class:`flet_notifications.AndroidNotificationFlag`. Combine integer flag values
    using `|` in the same way. See Android's [notification
    flags](https://developer.android.com/reference/android/app/Notification#flags) for
    their meanings and restrictions.

    Flags are added after the notification is built. `None` or
    :attr:`flet_notifications.AndroidNotificationFlag.NONE` adds no flags and does not
    clear flags set by other options. Prefer dedicated options such as :attr:`ongoing`
    and :attr:`auto_cancel` when available.
    """

    ticker: str | None = None
    """Ticker text sent to Android accessibility services."""

    tag: str | None = None
    """
    Additional identifier for immediately displayed Android notifications.

    The same `(tag, id)` pair replaces a visible notification. Pass the tag to
    :meth:`flet_notifications.Notifications.cancel` to remove it. Scheduled alarms
    use only the notification ID, not this pair.
    """

    led_on_duration: Annotated[ft.DurationValue | None, non_negative_duration()] = None
    """
    Time the notification LED remains on during each blink.

    Note:
        Used only before Android 8.0, together with the :attr:`channel`'s
        :attr:`~flet_notifications.NotificationChannel.led_color`. On newer versions,
        the device controls the blinking pattern.
    """

    led_off_duration: Annotated[ft.DurationValue | None, non_negative_duration()] = None
    """
    Time the notification LED remains off between blinks.

    Note:
        Used only before Android 8.0, together with the :attr:`channel`'s
        :attr:`~flet_notifications.NotificationChannel.led_color`. On newer versions,
        the device controls the blinking pattern.
    """
