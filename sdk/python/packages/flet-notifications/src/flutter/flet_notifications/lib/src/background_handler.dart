/// Background tap handling.
///
/// When the app process is not running and the user taps a notification (or
/// presses an action button), Android/iOS run this top-level handler in a
/// background isolate managed by the plugin. The response is persisted to
/// shared preferences under a unique queue key and replayed — in order — the
/// next time the service initializes.
///
/// Unique keys per tap avoid read-modify-write races between the background
/// isolate and the main isolate. [SharedPreferencesAsync] stores them without
/// the `flutter.` prefix of the legacy API, so `ft.SharedPreferences` neither
/// lists nor clears them, and reads them from the platform without caching.
library;

import 'dart:convert';
import 'dart:ui' show DartPluginRegistrant;

import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:shared_preferences/shared_preferences.dart';

const String _queuePrefix = "flet_notifications_queue_";

/// Serializes a notification response into the payload of the Python event it
/// becomes.
///
/// `event` names the service event to emit (`tap`, `action` or `dismiss`); it
/// routes queued responses and is not sent to Python. Only action responses carry
/// `action_id` and `input`, matching `NotificationActionEvent`.
Map<String, Object?> responseToEvent(NotificationResponse response) {
  final isAction = response.notificationResponseType ==
      NotificationResponseType.selectedNotificationAction;
  final isDismissed = response.notificationResponseType ==
      NotificationResponseType.notificationDismissed;
  String? nonEmpty(String? value) =>
      value == null || value.isEmpty ? null : value;
  var actionId = isAction ? nonEmpty(response.actionId) : null;
  var payload = nonEmpty(response.payload);
  // Windows returns the launch string (our JSON envelope) as both actionId
  // and payload, and typed text in `data` (input always null there).
  // Unwrap both so every platform yields the same event shape.
  if (actionId != null) {
    try {
      final decoded = jsonDecode(actionId);
      if (decoded is Map && decoded["id"] is String) {
        // Windows returns the launch string as both actionId and payload;
        // the envelope carries the real button id and payload.
        actionId = decoded["id"] as String;
        payload = nonEmpty(decoded["payload"] as String?);
      }
    } on FormatException {
      // Not our envelope: Android/Darwin/plain action ids pass through.
    }
  }
  final input = nonEmpty(response.input) ??
      (response.data.length == 1
          ? nonEmpty(response.data.values.first.toString())
          : null);
  return <String, Object?>{
    "event": isDismissed
        ? "dismiss"
        : isAction
            ? "action"
            : "tap",
    "id": response.id,
    "payload": payload,
    if (isAction) "action_id": actionId,
    if (isAction) "input": input,
    // Windows text/selection inputs arrive here (input is always null there).
    "data": response.data,
  };
}

/// Entry point invoked by the OS in a background isolate.
///
/// Must stay top-level and `@pragma('vm:entry-point')` annotated so the tree
/// shaker keeps it. Background isolates do not register Dart plugin
/// implementations by themselves, and [SharedPreferencesAsync] needs them.
@pragma('vm:entry-point')
void notificationTapBackground(NotificationResponse response) {
  DartPluginRegistrant.ensureInitialized();
  final stamp = DateTime.now().microsecondsSinceEpoch;
  final key = "$_queuePrefix$stamp-${identityHashCode(response)}";
  SharedPreferencesAsync()
      .setString(key, jsonEncode(responseToEvent(response)));
}

/// Reads and removes all queued taps, oldest key first.
Future<List<Map<String, Object?>>> drainTapQueue(
  SharedPreferencesAsync prefs,
) async {
  final keys = (await prefs.getKeys())
      .where((k) => k.startsWith(_queuePrefix))
      .toList()
    ..sort();
  final out = <Map<String, Object?>>[];
  for (final key in keys) {
    final raw = await prefs.getString(key);
    if (raw != null) {
      try {
        final decoded = jsonDecode(raw);
        if (decoded is Map) {
          out.add(decoded.cast<String, Object?>());
        }
      } on FormatException {
        // Drop unreadable entries — the queue must not wedge on bad data.
      }
    }
    await prefs.remove(key);
  }
  return out;
}
