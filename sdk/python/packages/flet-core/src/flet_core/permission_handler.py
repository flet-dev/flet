from enum import Enum
from typing import Any, Optional

from flet_core.control import Control
from flet_core.ref import Ref


class PermissionStatus(Enum):
    GRANTED = "granted"
    DENIED = "denied"
    PERMANENTLY_DENIED = "permanentlyDenied"
    LIMITED = "limited"
    PROVISIONAL = "provisional"
    RESTRICTED = "restricted"


class PermissionType(Enum):
    ACCESS_MEDIA_LOCATION = "accessMediaLocation"
    ACCESS_NOTIFICATION_POLICY = "accessNotificationPolicy"
    ACTIVITY_RECOGNITION = "activityRecognition"
    APP_TRACKING_TRANSPARENCY = "appTrackingTransparency"
    ASSISTANT = "assistant"
    AUDIO = "audio"
    BACKGROUND_REFRESH = "backgroundRefresh"
    BLUETOOTH = "bluetooth"
    BLUETOOTH_ADVERTISE = "bluetoothAdvertise"
    BLUETOOTH_CONNECT = "bluetoothConnect"
    BLUETOOTH_SCAN = "bluetoothScan"
    CALENDAR_FULL_ACCESS = "calendarFullAccess"
    CALENDAR_WRITE_ONLY = "calendarWriteOnly"
    CAMERA = "camera"
    CONTACTS = "contacts"
    CRITICAL_ALERTS = "criticalAlerts"
    IGNORE_BATTERY_OPTIMIZATIONS = "ignoreBatteryOptimizations"
    LOCATION = "location"
    LOCATION_ALWAYS = "locationAlways"
    LOCATION_WHEN_IN_USE = "locationWhenInUse"
    MANAGE_EXTERNAL_STORAGE = "manageExternalStorage"
    MEDIA_LIBRARY = "mediaLibrary"
    MICROPHONE = "microphone"
    NEARBY_WIFI_DEVICES = "nearbyWifiDevices"
    NOTIFICATION = "notification"
    PHONE = "phone"
    PHOTOS = "photos"
    PHOTOS_ADD_ONLY = "photosAddOnly"
    REMINDERS = "reminders"
    REQUEST_INSTALL_PACKAGES = "requestInstallPackages"
    SCHEDULE_EXACT_ALARM = "scheduleExactAlarm"
    SENSORS = "sensors"
    SENSORS_ALWAYS = "sensorsAlways"
    SMS = "sms"
    SPEECH = "speech"
    STORAGE = "storage"
    SYSTEM_ALERT_WINDOW = "systemAlertWindow"
    UNKNOWN = "unknown"
    VIDEOS = "videos"


class PermissionHandler(Control):
    """
    A control that allows you check and request permission from your device.
    This control is non-visual and should be added to `page.overlay` list.

    -----

    Online docs: https://flet.dev/docs/controls/permissionhandler
    """

    def __init__(
        self,
        # Control
        #
        ref: Optional[Ref] = None,
        data: Any = None,
    ):
        Control.__init__(
            self,
            ref=ref,
            data=data,
        )

    def _get_control_name(self):
        return "permission_handler"

    def check_permission(
        self, of: PermissionType, wait_timeout: Optional[float] = 25
    ) -> Optional[PermissionStatus]:
        out = self.invoke_method(
            "check_permission",
            {"of": of.value if isinstance(of, PermissionType) else of},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return PermissionStatus(out) if out is not None else None

    async def check_permission_async(
        self, of: PermissionType, wait_timeout: Optional[float] = 25
    ) -> Optional[PermissionStatus]:
        out = await self.invoke_method_async(
            "check_permission",
            {"of": of.value if isinstance(of, PermissionType) else of},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return PermissionStatus(out) if out is not None else None

    def request_permission(
        self, of: PermissionType, wait_timeout: Optional[float] = 25
    ) -> Optional[PermissionStatus]:
        out = self.invoke_method(
            "request_permission",
            {"of": of.value if isinstance(of, PermissionType) else of},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return PermissionStatus(out) if out is not None else None

    async def request_permission_async(
        self, of: PermissionType, wait_timeout: Optional[float] = 25
    ) -> Optional[PermissionStatus]:
        out = await self.invoke_method_async(
            "request_permission",
            {"of": of.value if isinstance(of, PermissionType) else of},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return PermissionStatus(out) if out is not None else None

    def open_app_settings(self, wait_timeout: Optional[float] = 10) -> bool:
        opened = self.invoke_method(
            "open_app_settings",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return opened == "true"

    async def open_app_settings_async(self, wait_timeout: Optional[float] = 10) -> bool:
        opened = await self.invoke_method_async(
            "open_app_settings",
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        return opened == "true"
