import "dart:async";
import "dart:convert";

import "package:permission_handler/permission_handler.dart";

Permission? parsePermissionInstance(String permissionOf) {
  switch (permissionOf) {
    case "accessMediaLocation":
      return Permission.accessMediaLocation;
    case "accessNotificationPolicy":
      return Permission.accessNotificationPolicy;
    case "activityRecognition":
      return Permission.activityRecognition;
    case "appTrackingTransparency":
      return Permission.appTrackingTransparency;
    case "assistant":
      return Permission.assistant;
    case "audio":
      return Permission.audio;
    case "backgroundRefresh":
      return Permission.backgroundRefresh;
    case "bluetooth":
      return Permission.bluetooth;
    case "bluetoothAdvertise":
      return Permission.bluetoothAdvertise;
    case "bluetoothConnect":
      return Permission.bluetoothConnect;
    case "bluetoothScan":
      return Permission.bluetoothScan;
    case "calendarFullAccess":
      return Permission.calendarFullAccess;
    case "calendarWriteOnly":
      return Permission.calendarWriteOnly;
    case "camera":
      return Permission.camera;
    case "contacts":
      return Permission.contacts;
    case "criticalAlerts":
      return Permission.criticalAlerts;
    case "ignoreBatteryOptimizations":
      return Permission.ignoreBatteryOptimizations;
    case "location":
      return Permission.location;
    case "locationAlways":
      return Permission.locationAlways;
    case "locationWhenInUse":
      return Permission.locationWhenInUse;
    case "manageExternalStorage":
      return Permission.manageExternalStorage;
    case "mediaLibrary":
      return Permission.mediaLibrary;
    case "microphone":
      return Permission.microphone;
    case "nearbyWifiDevices":
      return Permission.nearbyWifiDevices;
    case "notification":
      return Permission.notification;
    case "phone":
      return Permission.phone;
    case "photos":
      return Permission.photos;
    case "photosAddOnly":
      return Permission.photosAddOnly;
    case "reminders":
      return Permission.reminders;
    case "requestInstallPackages":
      return Permission.requestInstallPackages;
    case "scheduleExactAlarm":
      return Permission.scheduleExactAlarm;
    case "sensors":
      return Permission.sensors;
    case "sensorsAlways":
      return Permission.sensorsAlways;
    case "sms":
      return Permission.sms;
    case "speech":
      return Permission.speech;
    case "storage":
      return Permission.storage;
    case "systemAlertWindow":
      return Permission.systemAlertWindow;
    case "unknown":
      return Permission.unknown;
    case "videos":
      return Permission.videos;
    default:
      return null;
  }
}

Future<String?> checkPermission(String permissionOf) async {
  bool isGranted = await parsePermissionInstance(permissionOf)!.isGranted;
  bool isDenied = await parsePermissionInstance(permissionOf)!.isDenied;
  bool isPermanentlyDenied =
      await parsePermissionInstance(permissionOf)!.isPermanentlyDenied;
  bool isLimited = await parsePermissionInstance(permissionOf)!.isLimited;
  bool isProvisional =
      await parsePermissionInstance(permissionOf)!.isProvisional;
  bool isRestricted = await parsePermissionInstance(permissionOf)!.isRestricted;

  return json.encode({
    "is_granted": isGranted,
    "is_denied": isDenied,
    "is_permanently_denied": isPermanentlyDenied,
    "is_limited": isLimited,
    "is_provisional": isProvisional,
    "is_restricted": isRestricted
  });
}

Future<String?> requestPermission(String permissionOf) async {
  Future<PermissionStatus> permissionStatus =
      parsePermissionInstance(permissionOf)!.request();
  return permissionStatus.then((value) async {
    return await checkPermission(permissionOf);
  });
}