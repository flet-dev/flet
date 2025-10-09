import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:geolocator/geolocator.dart';

LocationAccuracy? parseLocationAccuracy(String? value,
    [LocationAccuracy? defaultValue]) {
  if (value == null) return defaultValue;
  return LocationAccuracy.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

extension PositionExtension on Position {
  Map<String, dynamic> toMap() => {
        "latitude": latitude,
        "longitude": longitude,
        "speed": speed,
        "altitude": altitude,
        "timestamp": timestamp,
        "accuracy": accuracy,
        "altitude_accuracy": altitudeAccuracy,
        "heading": heading,
        "heading_accuracy": headingAccuracy,
        "speed_accuracy": speedAccuracy,
        "floor": floor,
        "mocked": isMocked,
      };
}

ActivityType? parseActivityType(String? value, [ActivityType? defaultValue]) {
  if (value == null) return defaultValue;
  return ActivityType.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

LocationSettings? parseLocationSettings(dynamic value,
    [LocationSettings? defaultValue]) {
  if (value == null) return defaultValue;

  var distanceFilter = parseInt(value["distance_filter"], 0)!;
  var accuracy =
      parseLocationAccuracy(value["accuracy"], LocationAccuracy.best)!;
  var timeLimit = parseDuration(value["time_limit"]);
  if (kIsWeb) {
    return WebSettings(
      accuracy: accuracy,
      distanceFilter: distanceFilter,
      timeLimit: timeLimit,
      maximumAge: parseDuration(value["maximum_age"], Duration.zero)!,
    );
  } else if (isAndroidMobile()) {
    return AndroidSettings(
        accuracy: accuracy,
        distanceFilter: distanceFilter,
        timeLimit: timeLimit,
        intervalDuration: parseDuration(
            value["interval_duration"], const Duration(milliseconds: 5000))!,
        useMSLAltitude: parseBool(value["use_msl_altitude"], false)!,
        // Needed to prevet background to stop working when app goes in background
        foregroundNotificationConfig: (value["foreground_notification_text"] !=
                    null ||
                value["foreground_notification_title"] != null)
            ? ForegroundNotificationConfig(
                notificationText:
                    value["foreground_notification_text"] ?? "Location Updates",
                notificationTitle: value["foreground_notification_title"] ??
                    "Running in Background",
                enableWakeLock: parseBool(
                    value["foreground_notification_enable_wake_lock"], false)!,
                enableWifiLock: parseBool(
                    value["foreground_notification_enable_wifi_lock"], false)!,
                // color:
                //   parseColor(value["foreground_notification_color"], theme),
                notificationChannelName:
                    value["foreground_notification_channel_name"] ??
                        'Background Location',
                setOngoing: parseBool(
                    value["foreground_notification_set_ongoing"], true)!)
            : null);
  } else if (isApplePlatform()) {
    return AppleSettings(
      accuracy: accuracy,
      distanceFilter: distanceFilter,
      timeLimit: timeLimit,
      activityType:
          parseActivityType(value["activity_type"], ActivityType.other)!,
      pauseLocationUpdatesAutomatically:
          parseBool(value["pause_location_updates_automatically"], false)!,
      showBackgroundLocationIndicator:
          parseBool(value["show_background_location_indicator"], false)!,
      allowBackgroundLocationUpdates:
          parseBool(value["allow_background_location_updates"], true)!,
    );
  } else {
    return LocationSettings(
        accuracy: accuracy,
        distanceFilter: distanceFilter,
        timeLimit: timeLimit);
  }
}
