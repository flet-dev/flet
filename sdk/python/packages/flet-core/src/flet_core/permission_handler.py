from enum import Enum
import json
from typing import Any, Optional
from dataclasses import dataclass, field
from flet_core.control import Control
from flet_core.ref import Ref


@dataclass
class PermissionStatus:
    is_granted: Optional[bool] = field(default=None)
    is_denied: Optional[bool] = field(default=None)
    is_permanently_denied: Optional[bool] = field(default=None)
    is_limited: Optional[bool] = field(default=None)
    is_provisional: Optional[bool] = field(default=None)
    is_restricted: Optional[bool] = field(default=None)


class PermissionTemplate(Control):
    def __init__(self, permission_of, invoke_method, invoke_method_async):

        self.__permission_of = permission_of
        self.invoke_method = invoke_method
        self.invoke_method_async = invoke_method_async

    def check_permission(self, wait_timeout: Optional[float] = 5) -> PermissionStatus:
        permission = self.invoke_method(
            "checkPermission",
            {"permissionOf": self.__permission_of},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        if permission != "null":
            return PermissionStatus(**json.loads(permission))
        else:
            return PermissionStatus()

    async def check_permission_async(self, wait_timeout: Optional[float] = 5) -> PermissionStatus:
        permission = await self.invoke_method_async(
            "checkPermission",
            {"permissionOf": self.__permission_of},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        if permission != "null":
            return PermissionStatus(**json.loads(permission))
        else:
            return PermissionStatus()

    def request_permission(self, wait_timeout: Optional[float] = 25) -> PermissionStatus:
        permission = self.invoke_method(
            "requestPermission",
            {"permissionOf": self.__permission_of},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        if permission != "null":
            return PermissionStatus(**json.loads(permission))
        else:
            return PermissionStatus()

    async def request_permission_async(
        self, wait_timeout: Optional[float] = 25
    ) -> PermissionStatus:
        permission = await self.invoke_method_async(
            "requestPermission",
            {"permissionOf": self.__permission_of},
            wait_for_result=True,
            wait_timeout=wait_timeout,
        )
        if permission != "null":
            return PermissionStatus(**json.loads(permission))
        else:
            return PermissionStatus()


class PermissionHandler(Control):
    """
    A control that allows you check and request permission from your device.
    This control is non-visual and should be added to `page.overlay` list


    -----

    Online docs: https://flet.dev/docs/controls/flet_permission_handler
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
        self.accessMediaLocation = PermissionTemplate(
            "accessMediaLocation", self.invoke_method, self.invoke_method_async
        )
        self.accessNotificationPolicy = PermissionTemplate(
            "accessNotificationPolicy", self.invoke_method, self.invoke_method_async
        )
        self.activityRecognition = PermissionTemplate(
            "activityRecognition", self.invoke_method, self.invoke_method_async
        )
        self.appTrackingTransparency = PermissionTemplate(
            "appTrackingTransparency", self.invoke_method, self.invoke_method_async
        )
        self.assistant = PermissionTemplate(
            "assistant", self.invoke_method, self.invoke_method_async
        )
        self.audio = PermissionTemplate(
            "audio", self.invoke_method, self.invoke_method_async
        )
        self.backgroundRefresh = PermissionTemplate(
            "backgroundRefresh", self.invoke_method, self.invoke_method_async
        )
        self.bluetooth = PermissionTemplate(
            "bluetooth", self.invoke_method, self.invoke_method_async
        )
        self.bluetoothAdvertise = PermissionTemplate(
            "bluetoothAdvertise", self.invoke_method, self.invoke_method_async
        )
        self.bluetoothConnect = PermissionTemplate(
            "bluetoothConnect", self.invoke_method, self.invoke_method_async
        )
        self.bluetoothScan = PermissionTemplate(
            "bluetoothScan", self.invoke_method, self.invoke_method_async
        )
        self.calendarFullAccess = PermissionTemplate(
            "calendarFullAccess", self.invoke_method, self.invoke_method_async
        )
        self.calendarWriteOnly = PermissionTemplate(
            "calendarWriteOnly", self.invoke_method, self.invoke_method_async
        )
        self.camera = PermissionTemplate(
            "camera", self.invoke_method, self.invoke_method_async
        )
        self.contacts = PermissionTemplate(
            "contacts", self.invoke_method, self.invoke_method_async
        )
        self.criticalAlerts = PermissionTemplate(
            "criticalAlerts", self.invoke_method, self.invoke_method_async
        )
        self.ignoreBatteryOptimizations = PermissionTemplate(
            "ignoreBatteryOptimizations", self.invoke_method, self.invoke_method_async
        )
        self.location = PermissionTemplate(
            "location", self.invoke_method, self.invoke_method_async
        )
        self.locationAlways = PermissionTemplate(
            "locationAlways", self.invoke_method, self.invoke_method_async
        )
        self.locationWhenInUse = PermissionTemplate(
            "locationWhenInUse", self.invoke_method, self.invoke_method_async
        )
        self.manageExternalStorage = PermissionTemplate(
            "manageExternalStorage", self.invoke_method, self.invoke_method_async
        )
        self.mediaLibrary = PermissionTemplate(
            "mediaLibrary", self.invoke_method, self.invoke_method_async
        )
        self.microphone = PermissionTemplate(
            "microphone", self.invoke_method, self.invoke_method_async
        )
        self.nearbyWifiDevices = PermissionTemplate(
            "nearbyWifiDevices", self.invoke_method, self.invoke_method_async
        )
        self.notification = PermissionTemplate(
            "notification", self.invoke_method, self.invoke_method_async
        )
        self.phone = PermissionTemplate(
            "phone", self.invoke_method, self.invoke_method_async
        )
        self.photos = PermissionTemplate(
            "photos", self.invoke_method, self.invoke_method_async
        )
        self.photosAddOnly = PermissionTemplate(
            "photosAddOnly", self.invoke_method, self.invoke_method_async
        )
        self.reminders = PermissionTemplate(
            "reminders", self.invoke_method, self.invoke_method_async
        )
        self.requestInstallPackages = PermissionTemplate(
            "requestInstallPackages", self.invoke_method, self.invoke_method_async
        )
        self.scheduleExactAlarm = PermissionTemplate(
            "scheduleExactAlarm", self.invoke_method, self.invoke_method_async
        )
        self.sensors = PermissionTemplate(
            "sensors", self.invoke_method, self.invoke_method_async
        )
        self.sensorsAlways = PermissionTemplate(
            "sensorsAlways", self.invoke_method, self.invoke_method_async
        )
        self.sms = PermissionTemplate(
            "sms", self.invoke_method, self.invoke_method_async
        )
        self.speech = PermissionTemplate(
            "speech", self.invoke_method, self.invoke_method_async
        )
        self.storage = PermissionTemplate(
            "storage", self.invoke_method, self.invoke_method_async
        )
        self.systemAlertWindow = PermissionTemplate(
            "systemAlertWindow", self.invoke_method, self.invoke_method_async
        )
        self.unknown = PermissionTemplate(
            "unknown", self.invoke_method, self.invoke_method_async
        )
        self.videos = PermissionTemplate(
            "videos", self.invoke_method, self.invoke_method_async
        )

    def _get_control_name(self):
        return "permission_handler"
