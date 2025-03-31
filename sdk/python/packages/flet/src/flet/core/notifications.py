from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Union

from flet.core.badge import BadgeValue
from flet.core.control import Control, OptionalNumber
from flet.core.exceptions import FletUnsupportedPlatformException
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import ColorValue, DurationValue, PagePlatform


class NotificationActionType(Enum):
    DEFAULT = "default"
    DISABLED = "disabled"
    KEEP_ON_TOP = "keepOnTop"
    SILENT = "silent"
    SILENT_BACKGROUND = "silentBackground"
    DISMISS = "dismiss"


class NotificationCategory(Enum):
    ALARM = "alarm"
    CALL = "call"
    EMAIL = "email"
    ERROR = "error"
    EVENT = "event"
    LOCAL_SHARING = "localSharing"
    MESSAGE = "message"
    MISSED_CALL = "missedCall"
    NAVIGATION = "navigation"
    PROGRESS = "progress"
    PROMO = "promo"
    RECOMMENDATION = "recommendation"
    REMINDER = "reminder"
    SERVICE = "service"
    SOCIAL = "social"
    STATUS = "status"
    STOPWATCH = "stopwatch"
    TRANSPORT = "transport"
    WORKOUT = "workout"


class NotificationLayout(Enum):
    DEFAULT = "default"
    BIG_PICTURE = "bigPicture"
    BIG_TEXT = "bigText"
    INBOX = "inbox"
    PROGRESS_BAR = "progressBar"
    MESSAGING = "messaging"
    MESSAGING_GROUP = "messagingGroup"
    MEDIA_PLAYER = "mediaPlayer"


class NotificationPrivacy(Enum):
    SECRET = "secret"
    PRIVATE = "private"
    PUBLIC = "public"


class NotificationGroupSort(Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


class NotificationImportance(Enum):
    NONE = "none"
    DEFAULT = "default"
    MAXIMUM = "maximum"
    MINIMUM = "minimum"
    HIGH = "high"
    LOW = "low"


class NotificationRingtoneType(Enum):
    ALARM = "alarm"
    NOTIFICATION = "notification"
    RINGTONE = "ringtone"


class NotificationGroupAlertBehavior(Enum):
    ALL = "all"
    SUMMARY = "summary"
    CHILDREN = "children"


class NotificationLifeCycle(Enum):
    FOREGROUND = "foreground"
    BACKGROUND = "background"
    TERMINATED = "terminated"


@dataclass
class NotificationInterval:
    interval: DurationValue
    time_zone: Optional[str] = None
    allow_while_idle: bool = False
    repeats: bool = False
    precise_alarm: bool = False


@dataclass
class NotificationCalendar:
    day: Optional[int] = None
    hour: Optional[int] = None
    minute: Optional[int] = None
    second: Optional[int] = None
    millisecond: Optional[int] = None
    month: Optional[int] = None
    weekday: Optional[int] = None
    week_of_year: Optional[int] = None
    year: Optional[int] = None
    era: Optional[int] = None
    time_zone: Optional[str] = None
    allow_while_idle: bool = False
    repeats: bool = False
    precise_alarm: bool = False


@dataclass
class NotificationContent:
    id: int
    channel_key: str
    title: Optional[str] = None
    body: Optional[str] = None
    title_loc_key: Optional[str] = None
    body_loc_key: Optional[str] = None
    title_loc_args: Optional[List[str]] = None
    body_loc_args: Optional[List[str]] = None
    group_key: Optional[str] = None
    summary: Optional[str] = None
    icon: Optional[str] = None
    large_icon: Optional[str] = None
    big_picture: Optional[str] = None
    custom_sound: Optional[str] = None
    show_when: bool = True
    wake_up_screen: bool = False
    full_screen_intent: bool = False
    critical_alert: bool = False
    rounded_large_icon: bool = False
    rounded_big_picture: bool = False
    auto_dismissible: bool = True
    color: Optional[ColorValue] = None
    timeout_after: Optional[DurationValue] = None
    chronometer: Optional[DurationValue] = None
    bgcolor: Optional[ColorValue] = None
    hide_large_icon_on_expand: bool = False
    locked: Optional[bool] = False
    progress: OptionalNumber = None
    badge: Optional[int] = None
    ticker: Optional[str] = None
    display_on_foreground: bool = True
    display_on_background: bool = True
    duration: Optional[DurationValue] = None
    playback_speed: OptionalNumber = None
    action_type: NotificationActionType = NotificationActionType.DEFAULT
    category: Optional[NotificationCategory] = None
    layout: Optional[NotificationLayout] = None


@dataclass
class NotificationChannel:
    channel_key: str
    channel_name: str
    channel_description: str
    channel_group_key: Optional[str] = None
    channel_show_badge: bool = True
    critical_alerts: bool = False
    default_color: Optional[ColorValue] = None
    enable_lights: bool = True
    enable_vibration: bool = True
    led_color: Optional[ColorValue] = None
    led_on_ms: Optional[int] = None
    led_off_ms: Optional[int] = None
    only_alert_once: bool = False
    play_sound: bool = True
    sound_source: Optional[str] = None
    group_key: Optional[str] = None
    icon: Optional[str] = None
    locked: bool = False
    privacy: Optional[NotificationPrivacy] = None
    group_sort: Optional[NotificationGroupSort] = None
    importance: Optional[NotificationImportance] = None
    ringtone_type: Optional[NotificationRingtoneType] = None
    group_alert_behavior: Optional[NotificationGroupAlertBehavior] = None


@dataclass
class NotificationActionButton:
    key: str
    label: str
    disabled: Optional[bool] = False
    requires_authentication: Optional[bool] = False
    dangerous: Optional[bool] = False
    require_text_input: Optional[bool] = False
    show_in_compact_view: Optional[bool] = True
    auto_dismissible: Optional[bool] = True
    color: Optional[ColorValue] = None
    icon: Optional[str] = None
    action_type: Optional[NotificationActionType] = None


class Notifications(Control):
    def __init__(
        self,
        channels: List[NotificationChannel],
        language_code: Optional[str] = None,
        #
        # Control
        #
        ref: Optional[Ref] = None,
        opacity: OptionalNumber = None,
        tooltip: Optional[TooltipValue] = None,
        badge: Optional[BadgeValue] = None,
        visible: Optional[bool] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            opacity=opacity,
            tooltip=tooltip,
            badge=badge,
            visible=visible,
            data=data,
        )

        self.__channels = channels
        self.language_code = language_code

    def _get_control_name(self):
        return "notifications"

    def before_update(self):
        super().before_update()
        assert self.page is not None, "Notifications must be added to page first."
        if self.page.web or self.page.platform not in [
            PagePlatform.ANDROID,
            PagePlatform.IOS,
        ]:
            raise FletUnsupportedPlatformException(
                "This control is supported on Android and iOS platforms only."
            )
        self._set_attr_json("channels", self.__channels)

    def show(
        self,
        content: NotificationContent,
        action_buttons: Optional[List[NotificationActionButton]] = None,
        schedule: Optional[Union[NotificationCalendar, NotificationInterval]] = None,
    ) -> None:
        self.invoke_method(
            "show",
            arguments={
                "content": self._convert_attr_json(content),
                "action_buttons": self._convert_attr_json(action_buttons),
                "schedule": self._convert_attr_json(schedule),
                "schedule_parser": "interval"
                if isinstance(schedule, NotificationInterval)
                else "calendar",
            },
        )

    def dismiss(
        self,
        id: Optional[int] = None,
        channel_key: Optional[str] = None,
        group_key: Optional[str] = None,
    ) -> None:
        self.invoke_method(
            "dismiss",
            arguments={
                "id": id,
                "channel_key": channel_key,
                "group_key": group_key,
            },
        )

    def dismiss_all(self) -> None:
        self.invoke_method("dismiss_all")

    def cancel(
        self,
        id: Optional[int] = None,
        channel_key: Optional[str] = None,
        group_key: Optional[str] = None,
    ) -> None:
        self.invoke_method(
            "cancel",
            arguments={
                "id": id,
                "channel_key": channel_key,
                "group_key": group_key,
            },
        )

    def cancel_schedule(
        self,
        id: Optional[int] = None,
        channel_key: Optional[str] = None,
        group_key: Optional[str] = None,
    ) -> None:
        self.invoke_method(
            "cancel_schedule",
            arguments={
                "id": id,
                "channel_key": channel_key,
                "group_key": group_key,
            },
        )

    def cancel_all_schedules(self) -> None:
        self.invoke_method("cancel_all_schedules")

    # badge_counter
    def get_badge_counter(self, wait_timeout: float = 10) -> int:
        return self.invoke_method(
            "get_badge_counter",
            wait_for_result=True,
            wait_timeout=wait_timeout,
            result_type="int",
        )

    def set_badge_counter(self, value: int) -> None:
        self.invoke_method("set_badge_counter", arguments={"value": str(value)})

    def increment_badge_counter(self, wait_timeout: float = 10) -> bool:
        return self.invoke_method(
            "increment_badge_counter",
            wait_for_result=True,
            wait_timeout=wait_timeout,
            result_type="bool",
        )

    def decrement_badge_counter(self, wait_timeout: float = 10) -> bool:
        return self.invoke_method(
            "decrement_badge_counter",
            wait_for_result=True,
            wait_timeout=wait_timeout,
            result_type="bool",
        )

    def reset_badge_counter(self) -> None:
        self.invoke_method("reset_badge_counter")

    # channels
    def set_channel(
        self, channel: NotificationChannel, force_update: bool = False
    ) -> None:
        self.invoke_method(
            "set_channel",
            arguments={
                "channel": self._convert_attr_json(channel),
                "force_update": force_update,
            },
        )

    def remove_channel(self, channel_key: str) -> None:
        self.invoke_method("remove_channel", arguments={"channel_key": channel_key})

    # permissions
    def is_allowed(self, wait_timeout: float = 10) -> bool:
        return self.invoke_method(
            "is_allowed",
            wait_for_result=True,
            wait_timeout=wait_timeout,
            result_type="bool",
        )

    def request_permission(self, wait_timeout: float = 10) -> bool:
        return self.invoke_method(
            "request_permission",
            wait_for_result=True,
            wait_timeout=wait_timeout,
            result_type="bool",
        )

    # time
    def get_local_timezone_identifier(self, wait_timeout: float = 10) -> str:
        return self.invoke_method(
            "get_local_timezone_identifier",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    def get_utc_timezone_identifier(self, wait_timeout: float = 10) -> str:
        return self.invoke_method(
            "get_utc_timezone_identifier",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    # others
    def show_alarm_page(self) -> None:
        self.invoke_method("show_alarm_page")

    def get_initial_action(self, remove_from_action_events: bool = False) -> str:
        return self.invoke_method(
            "get_initial_action",
            arguments={"remove_from_action_events": str(remove_from_action_events)},
        )

    def show_global_dnd_override_page(self) -> None:
        self.invoke_method("show_global_dnd_override_page")

    def get_lifecycle(self, wait_timeout: float = 10) -> NotificationLifeCycle:
        result = self.invoke_method(
            "get_app_lifecycle",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return NotificationLifeCycle(result)

    def get_localization(self, wait_timeout: float = 10) -> str:
        return self.invoke_method(
            "get_localization",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )

    def is_active_on_status_bar(self, id: int, wait_timeout: float = 10) -> bool:
        return self.invoke_method(
            "is_active_on_status_bar",
            arguments={"id": str(id)},
            wait_for_result=True,
            wait_timeout=wait_timeout,
            result_type="bool",
        )

    def get_ids_active_on_status_bar(self, wait_timeout: float = 10) -> List[int]:
        return self.invoke_method(
            "get_ids_active_on_status_bar",
            wait_for_result=True,
            wait_timeout=wait_timeout,
            result_type="json_encoded",
        )

    # channels
    @property
    def channels(self) -> List[NotificationChannel]:
        return self.__channels

    # language_code
    @property
    def language_code(self) -> Optional[str]:
        return self._get_attr("languageCode")

    @language_code.setter
    def language_code(self, value: Optional[str]):
        self._set_attr("languageCode", value)
