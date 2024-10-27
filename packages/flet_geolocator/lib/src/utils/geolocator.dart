import 'dart:convert';

import 'package:collection/collection.dart';
import 'package:flet/flet.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:geolocator/geolocator.dart';

LocationAccuracy? parseLocationAccuracy(String? accuracy,
    [LocationAccuracy? defaultValue]) {
  switch (accuracy?.toLowerCase()) {
    case "best":
      return LocationAccuracy.best;
    case "bestfornavigation":
      return LocationAccuracy.bestForNavigation;
    case "high":
      return LocationAccuracy.high;
    case "medium":
      return LocationAccuracy.medium;
    case "low":
      return LocationAccuracy.low;
    case "lowest":
      return LocationAccuracy.lowest;
    case "reduced":
      return LocationAccuracy.reduced;
    default:
      return defaultValue;
  }
}

String? positionToJson(Position? position) {
  if (position == null) {
    return null;
  }
  String positionAsJson = json.encode({
    "latitude": position.latitude,
    "longitude": position.longitude,
    "accuracy": position.accuracy,
    "altitude": position.altitude,
    "speed": position.speed,
    "speed_accuracy": position.speedAccuracy,
    "heading": position.heading,
    "heading_accuracy": position.headingAccuracy,
    "timestamp": position.timestamp.toIso8601String(),
    "floor": position.floor,
    "is_mocked": position.isMocked,
  });
  return positionAsJson;
}

ActivityType? parseActivityType(String? value, [ActivityType? defValue]) {
  if (value == null) {
    return defValue;
  }
  return ActivityType.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defValue;
}

LocationSettings? parseLocationSettings(
    Control control, String propName, ThemeData? theme,
    [LocationSettings? defValue]) {
  var v = control.attrString(propName, null);
  if (v == null) {
    return defValue;
  }

  final j1 = json.decode(v);
  return locationSettingsFromJson(j1, theme);
}

LocationSettings? locationSettingsFromJson(dynamic j, ThemeData? theme) {
  var distanceFilter = parseInt(j["distance_filter"], 0)!;
  var accuracy = parseLocationAccuracy(j["accuracy"], LocationAccuracy.best)!;
  var timeLimit = durationFromJSON(j["time_limit"]);
  if (defaultTargetPlatform == TargetPlatform.android) {
    return AndroidSettings(
        accuracy: accuracy,
        distanceFilter: distanceFilter,
        timeLimit: timeLimit,
        forceLocationManager: parseBool(j["force_location_manager"], false)!,
        intervalDuration: durationFromJSON(j["interval_duration"]),
        useMSLAltitude: parseBool(j["use_msl_altitude"], false)!,
        // Needs this or when app goes in background, background service stops working
        foregroundNotificationConfig: (j["foreground_notification_text"] !=
                    null ||
                j["foreground_notification_title"] != null)
            ? ForegroundNotificationConfig(
                notificationText:
                    j["foreground_notification_text"] ?? "Location Updates",
                notificationTitle: j["foreground_notification_title"] ??
                    "Running in Background",
                enableWakeLock: parseBool(
                    j["foreground_notification_enable_wake_lock"], false)!,
                enableWifiLock: parseBool(
                    j["foreground_notification_enable_wifi_lock"], false)!,
                color: parseColor(theme, j["foreground_notification_color"]),
                notificationChannelName:
                    j["foreground_notification_channel_name"] ??
                        'Background Location',
                setOngoing:
                    parseBool(j["foreground_notification_set_ongoing"], true)!)
            : null);
  } else if (defaultTargetPlatform == TargetPlatform.iOS ||
      defaultTargetPlatform == TargetPlatform.macOS) {
    return AppleSettings(
      accuracy: accuracy,
      distanceFilter: distanceFilter,
      timeLimit: timeLimit,
      activityType: parseActivityType(j["activity_type"], ActivityType.other)!,
      pauseLocationUpdatesAutomatically:
          parseBool(j["pause_location_updates_automatically"], false)!,
      showBackgroundLocationIndicator:
          parseBool(j["show_background_location_indicator"], false)!,
      allowBackgroundLocationUpdates:
          parseBool(j["allow_background_location_updates"], true)!,
    );
  } else if (kIsWeb) {
    return WebSettings(
      accuracy: accuracy,
      distanceFilter: distanceFilter,
      timeLimit: timeLimit,
      maximumAge: durationFromJSON(j["maximum_age"], Duration.zero)!,
    );
  } else {
    return LocationSettings(
        accuracy: accuracy,
        distanceFilter: distanceFilter,
        timeLimit: timeLimit);
  }
}
