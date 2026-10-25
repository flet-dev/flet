import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

/// Launch arguments for a Windows notification or one of its buttons.
///
/// Windows hands the app a clicked element's launch arguments and nothing else:
/// the plugin reports a click on the notification's body as an action too, with
/// the arguments as its action id, and without the notification's id. Encoding
/// them lets [decodeWindowsLaunchArguments] tell the two apart and restore the
/// id and payload.
String windowsLaunchArguments({
  required int? notificationId,
  required String? payload,
  String? actionId,
}) =>
    jsonEncode({
      "notification": notificationId,
      if (actionId != null) "id": actionId,
      "payload": payload,
    });

/// Decodes [windowsLaunchArguments], or returns `null` for other strings.
({int? notificationId, String? actionId, String? payload})?
    decodeWindowsLaunchArguments(String? arguments) {
  if (arguments == null || !arguments.startsWith("{")) return null;
  try {
    final decoded = jsonDecode(arguments);
    if (decoded is! Map || !decoded.containsKey("notification")) return null;
    final (notificationId, actionId, payload) =
        (decoded["notification"], decoded["id"], decoded["payload"]);
    if (notificationId is! int? ||
        actionId is! String? ||
        payload is! String?) {
      return null;
    }
    return (
      notificationId: notificationId,
      actionId: actionId,
      payload: payload,
    );
  } on FormatException {
    return null;
  }
}

/// A Windows header with [title], under a fixed ID, so every notification with
/// a header shares one group in the notification center.
fln.WindowsHeader? parseWindowsHeader(String? title) {
  if (title == null || title.isEmpty) return null;
  return fln.WindowsHeader(id: "header", title: title, arguments: "");
}

fln.WindowsNotificationAudio? parseWindowsNotificationAudio(
  String? value, {
  bool loop = false,
  fln.WindowsNotificationAudio? defaultValue,
}) {
  if (value == null || value.isEmpty) return defaultValue;
  if (value.toLowerCase() == "silent") {
    return fln.WindowsNotificationAudio.silent();
  }
  final sound = parseEnum(fln.WindowsNotificationSound.values,
      value == "default" ? "defaultSound" : value);
  return sound == null
      ? defaultValue
      : fln.WindowsNotificationAudio.preset(sound: sound, shouldLoop: loop);
}

fln.WindowsNotificationDuration? parseWindowsNotificationDuration(String? value,
        [fln.WindowsNotificationDuration? defaultValue]) =>
    parseEnum(fln.WindowsNotificationDuration.values, value, defaultValue);

/// Converts a `WindowsProgress`, whose value counts up to its `max`, to the
/// plugin's progress bar, whose value is a fraction.
fln.WindowsProgressBar parseWindowsProgress(Map value) {
  final max = parseInt(value["max"], 100)!;
  final current = parseInt(value["value"], 0)!;
  return fln.WindowsProgressBar(
    id: "progress",
    status: value["status"] as String? ?? "",
    title: value["title"] as String?,
    label: value["label"] as String?,
    value: parseBool(value["indeterminate"], false)!
        ? null
        : max <= 0
            ? 0
            : (current / max).clamp(0.0, 1.0),
  );
}

fln.WindowsNotificationScenario? parseWindowsNotificationScenario(String? value,
        [fln.WindowsNotificationScenario? defaultValue]) =>
    parseEnum(fln.WindowsNotificationScenario.values, value, defaultValue);
