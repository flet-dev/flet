/// Queued notification responses.
///
/// Android and iOS deliver responses to actions that do not bring the app to the
/// foreground, and on iOS taps on a terminated app, to this top-level handler in
/// a background isolate managed by the plugin, whether or not the app is
/// running. Responses that arrive while no service runs are queued the same
/// way. Each is persisted to shared preferences under a unique queue key, and
/// the service replays the queue, in order, when it initializes and whenever a
/// new entry is signaled.
///
/// Unique keys per response avoid read-modify-write races between the background
/// isolate and the main isolate. [SharedPreferencesAsync] stores them without
/// the `flutter.` prefix of the legacy API, so `ft.SharedPreferences` neither
/// lists nor clears them, and reads them from the platform without caching.
library;

import 'dart:convert';
import 'dart:ui' show DartPluginRegistrant;

import 'package:flet/flet.dart' show isWindowsDesktop;
import 'package:flutter_local_notifications/flutter_local_notifications.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../platforms/windows.dart';
import 'response_queue_signal.dart';

const String _queuePrefix = "flet_notifications_queue_";

/// Serializes a notification response into the payload of the Python event it
/// becomes.
///
/// `event` names the service event to emit (`tap` or `action`); it
/// routes queued responses and is not sent to Python. Only action responses carry
/// `action_id` and `input`, matching `NotificationActionEvent`.
Map<String, Object?> responseToEvent(NotificationResponse response) {
  var isAction = response.notificationResponseType ==
      NotificationResponseType.selectedNotificationAction;
  String? nonEmpty(String? value) =>
      value == null || value.isEmpty ? null : value;
  var id = response.id;
  var actionId = isAction ? nonEmpty(response.actionId) : null;
  var payload = nonEmpty(response.payload);
  // Windows reports every click as an action whose id is the clicked element's
  // launch arguments, and typed text in `data` (input is always null there).
  // Elsewhere, an action id is the app's own and kept as it is.
  final launch = isWindowsDesktop()
      ? decodeWindowsLaunchArguments(response.actionId)
      : null;
  if (launch != null) {
    id = launch.notificationId ?? id;
    actionId = nonEmpty(launch.actionId);
    payload = nonEmpty(launch.payload);
    isAction = actionId != null;
  }
  final input = nonEmpty(response.input) ??
      (response.data.length == 1
          ? nonEmpty(response.data.values.first.toString())
          : null);
  return <String, Object?>{
    "event": isAction ? "action" : "tap",
    "id": id,
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
Future<void> notificationResponseBackground(
    NotificationResponse response) async {
  DartPluginRegistrant.ensureInitialized();
  await queueResponse(response);
}

/// Persists [response] for the service to replay, and signals it.
Future<void> queueResponse(NotificationResponse response) async {
  final stamp = DateTime.now().microsecondsSinceEpoch;
  final key = "$_queuePrefix$stamp-${identityHashCode(response)}";
  await SharedPreferencesAsync()
      .setString(key, jsonEncode(responseToEvent(response)));
  signalResponseQueued();
}

/// Reads and removes all queued responses, oldest key first.
Future<List<Map<String, Object?>>> drainResponseQueue(
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
