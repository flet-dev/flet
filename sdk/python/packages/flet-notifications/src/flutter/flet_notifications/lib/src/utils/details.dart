import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import '../platforms/android.dart';
import '../platforms/darwin.dart';
import '../platforms/linux.dart';
import '../platforms/web.dart';
import '../platforms/windows.dart';
import 'actions.dart';
import 'errors.dart';

/// Converts a wire payload into the upstream platform notification details.
fln.NotificationDetails parseNotificationDetails({
  required List<ParsedAction> actions,
  Map? details,
}) {
  try {
    return fln.NotificationDetails(
      android: parseAndroidDetails(
        actions: actions,
        options: _platformOptions(details, "android"),
      ),
      iOS: parseDarwinDetails(
        actions: actions,
        options: _platformOptions(details, "ios"),
      ),
      macOS: parseDarwinDetails(
        actions: actions,
        options: _platformOptions(details, "macos"),
      ),
      linux: parseLinuxDetails(_platformOptions(details, "linux")),
      windows: parseWindowsDetails(
        actions: actions,
        options: _platformOptions(details, "windows"),
        notificationId: parseInt(details?["id"]),
        payload: details?["payload"] as String?,
      ),
      web: parseWebDetails(
        actions: actions,
        options: _platformOptions(details, "web"),
      ),
    );
  } on FormatException catch (e) {
    throw NotificationException.invalidArgument(e.message);
  } on TypeError catch (e) {
    throw NotificationException.invalidArgument(
      "invalid notification option: $e",
    );
  }
}

/// Extracts one platform's options dict from the `options` payload.
Map<dynamic, dynamic>? _platformOptions(Map? details, String platform) {
  final options = details?["options"];
  if (options is! Map) return null;
  final platformOptions = options[platform];
  return platformOptions is Map ? platformOptions : null;
}
