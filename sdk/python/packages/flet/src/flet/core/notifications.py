from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, List

from flet.core.badge import BadgeValue
from flet.core.control import Control, OptionalNumber
from flet.core.ref import Ref
from flet.core.tooltip import TooltipValue
from flet.core.types import ColorValue, DurationValue


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
    show_when: Optional[bool] = True
    wake_up_screen: Optional[bool] = False
    full_screen_intent: Optional[bool] = False
    critical_alert: Optional[bool] = False
    rounded_large_icon: Optional[bool] = False
    rounded_big_picture: Optional[bool] = False
    auto_dismissible: Optional[bool] = True
    color: Optional[ColorValue] = None
    timeout_after: Optional[DurationValue] = None
    chronometer: Optional[DurationValue] = None
    bgcolor: Optional[ColorValue] = None
    hide_large_icon_on_expand: Optional[bool] = False
    locked: Optional[bool] = False
    progress: OptionalNumber = None
    badge: Optional[int] = None
    ticker: Optional[str] = None
    display_on_foreground: Optional[bool] = True
    display_on_background: Optional[bool] = True
    duration: Optional[DurationValue] = None
    playback_speed: OptionalNumber = None
    action_type: Optional[NotificationActionType] = NotificationActionType.DEFAULT
    category: Optional[NotificationCategory] = None
    layout: Optional[NotificationLayout] = None


@dataclass
class NotificationChannel:
    channel_key: str
    channel_name: str
    channel_description: str
    channel_group_key: Optional[str] = None
    channel_show_badge: Optional[bool] = True
    critical_alerts: Optional[bool] = False
    default_color: Optional[ColorValue] = None
    enable_lights: Optional[bool] = True
    enable_vibration: Optional[bool] = True
    led_color: Optional[ColorValue] = None
    led_on_ms: Optional[int] = None
    led_off_ms: Optional[int] = None
    only_alert_once: Optional[bool] = False
    play_sound: Optional[bool] = True
    sound_source: Optional[str] = None
    group_key: Optional[str] = None
    icon: Optional[str] = None
    locked: Optional[bool] = False
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
        channels: Optional[List[NotificationChannel]] = None,
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
        self._set_attr_json("channels", self.__channels)

    def show(
        self,
        content: NotificationContent,
        actions: Optional[List[NotificationActionButton]] = None,
    ):
        self.invoke_method(
            "show",
            arguments={
                "content": self._convert_attr_json(content),
                "action_buttons": self._convert_attr_json(actions),
            },
        )

    # channels∂
    @property
    def channels(self) -> Optional[List[NotificationChannel]]:
        return self.__channels

    # language_code
    @property
    def language_code(self) -> Optional[str]:
        return self._get_attr("languageCode")

    @language_code.setter
    def language_code(self, value: Optional[str]):
        self._set_attr("languageCode", value)
