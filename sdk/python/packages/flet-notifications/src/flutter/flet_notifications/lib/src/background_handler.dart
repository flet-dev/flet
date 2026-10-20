/// Background tap handling.
///
/// When the app process is not running and the user taps a notification (or
/// presses an action button), Android/iOS run this top-level handler in a
/// background isolate managed by the plugin. The response is persisted to
/// shared preferences under a unique queue key and replayed — in order — the
/// next time the service initializes.
///
/// Unique keys per tap avoid read-modify-write races between the background
/// isolate and the main isolate.
library;

import 'dart:convert';

import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:shared_preferences/shared_preferences.dart';

const String _queuePrefix = "flet_notifications_queue_";

/// Serializes a notification response into the event payload shape the
/// Python `NotificationEvent` dataclass expects.
Map<String, Object?> responseToEvent(NotificationResponse response) {
  final isAction = response.notificationResponseType ==
      NotificationResponseType.selectedNotificationAction;
  final isDismissed = response.notificationResponseType ==
      NotificationResponseType.notificationDismissed;
  var input = response.input;
  var actionId = isDismissed
      ? ""
      : isAction
          ? (response.actionId ?? "")
          : "";
  var payload = response.payload ?? "";
  // Windows returns the launch string (our JSON envelope) as both actionId
  // and payload, and typed text in `data` (input always null there).
  // Unwrap both so every platform yields the same event shape.
  if (isAction && actionId.isNotEmpty) {
    try {
      final decoded = jsonDecode(actionId);
      if (decoded is Map && decoded["id"] is String) {
        // Windows returns the launch string as both actionId and payload;
        // the envelope carries the real button id and payload.
        actionId = decoded["id"] as String;
        if (decoded["payload"] is String) {
          payload = decoded["payload"] as String;
        }
      }
    } on FormatException {
      // Not our envelope: Android/Darwin/plain action ids pass through.
    }
  }
  final normalizedInput = (input != null && input.isNotEmpty)
      ? input
      : (response.data.length == 1
          ? response.data.values.first.toString()
          : "");
  return <String, Object?>{
    "id": response.id ?? -1,
    "action_id": actionId,
    "payload": payload,
    "input": normalizedInput,
    "response_type": isDismissed
        ? "dismissed"
        : isAction
            ? "action"
            : "tap",
    // Windows text/selection inputs arrive here (input is always null there).
    "data": response.data,
  };
}

/// Entry point invoked by the OS in a background isolate.
///
/// Must stay top-level and `@pragma('vm:entry-point')` annotated so the tree
/// shaker keeps it.
@pragma('vm:entry-point')
void notificationTapBackground(NotificationResponse response) {
  SharedPreferences.getInstance().then((prefs) {
    final stamp = DateTime.now().microsecondsSinceEpoch;
    final key = "$_queuePrefix$stamp-${identityHashCode(response)}";
    prefs.setString(key, jsonEncode(responseToEvent(response)));
  });
}

/// Reads and removes all queued taps, oldest key first.
Future<List<Map<String, Object?>>> drainTapQueue(
  SharedPreferences prefs,
) async {
  // Another isolate may have written entries since this instance was cached.
  await prefs.reload();
  final keys = prefs.getKeys().where((k) => k.startsWith(_queuePrefix)).toList()
    ..sort();
  final out = <Map<String, Object?>>[];
  for (final key in keys) {
    final raw = prefs.getString(key);
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
