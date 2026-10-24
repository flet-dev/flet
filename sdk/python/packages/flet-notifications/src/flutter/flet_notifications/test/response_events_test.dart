import 'dart:convert';

import 'package:flet_notifications/src/background_handler.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shared_preferences_platform_interface/in_memory_shared_preferences_async.dart';
import 'package:shared_preferences_platform_interface/shared_preferences_async_platform_interface.dart';

fln.NotificationResponse _response({
  int? id = 7,
  String? actionId,
  String? input,
  String? payload,
  fln.NotificationResponseType type =
      fln.NotificationResponseType.selectedNotification,
}) {
  return fln.NotificationResponse(
    id: id,
    actionId: actionId,
    input: input,
    payload: payload,
    notificationResponseType: type,
  );
}

void main() {
  late SharedPreferencesAsync prefs;

  setUp(() {
    SharedPreferencesAsyncPlatform.instance =
        InMemorySharedPreferencesAsync.empty();
    prefs = SharedPreferencesAsync();
  });

  group("responseToEvent", () {
    test("action with inline reply", () {
      final event = responseToEvent(
        _response(
          actionId: "reply",
          input: "my answer",
          payload: "hello",
          type: fln.NotificationResponseType.selectedNotificationAction,
        ),
      );
      expect(event["action_id"], "reply");
      expect(event["input"], "my answer");
      expect(event["event"], "action");
    });

    test("absent values are null, not placeholders", () {
      final event = responseToEvent(_response(id: null, payload: ""));
      expect(event["event"], "tap");
      expect(event["id"], isNull);
      expect(event["payload"], isNull);
      // Only action responses carry action fields.
      expect(event.containsKey("action_id"), isFalse);
      expect(event.containsKey("input"), isFalse);
    });
  });

  group("drainTapQueue", () {
    test("returns events in key order and removes them", () async {
      final older = responseToEvent(_response(payload: "first"));
      final newer = responseToEvent(_response(payload: "second"));
      await prefs.setString(
          "flet_notifications_queue_200-2", jsonEncode(newer));
      await prefs.setString(
          "flet_notifications_queue_100-1", jsonEncode(older));
      await prefs.setString("unrelated_key", "keep me");

      expect(await drainTapQueue(prefs), [older, newer]);
      expect(await drainTapQueue(prefs), isEmpty);
      expect(await prefs.getKeys(), {"unrelated_key"});
    });

    test("unreadable entries are dropped, not fatal", () async {
      await prefs.setString("flet_notifications_queue_1-1", "not json");
      expect(await drainTapQueue(prefs), isEmpty);
      // The bad entry is removed rather than left to wedge the queue.
      expect(await prefs.getKeys(), isEmpty);
    });

    test("background taps are queued for the main isolate", () async {
      final response = _response(payload: "background");
      notificationTapBackground(response);
      await pumpEventQueue();
      expect(await drainTapQueue(prefs), [responseToEvent(response)]);
    });
  });

  group("Windows response normalization", () {
    test("actionId envelope is unwrapped to the button id", () {
      // The Windows plugin returns the launch string as both actionId and
      // payload; our Dart envelope carries id + payload as JSON.
      const response = fln.NotificationResponse(
        id: 7,
        actionId: '{"id": "reply", "payload": "actions"}',
        input: null,
        payload: '{"id": "reply", "payload": "actions"}',
        notificationResponseType:
            fln.NotificationResponseType.selectedNotificationAction,
        data: {"reply": "typed on windows"},
      );
      final event = responseToEvent(response);
      expect(event["action_id"], "reply");
      expect(event["payload"], "actions");
      expect(event["input"], "typed on windows"); // normalized from data
      expect(event["event"], "action");
    });

    test("an envelope without a payload yields no payload", () {
      const envelope = '{"id": "open", "payload": null}';
      const response = fln.NotificationResponse(
        id: 7,
        actionId: envelope,
        payload: envelope,
        notificationResponseType:
            fln.NotificationResponseType.selectedNotificationAction,
      );
      final event = responseToEvent(response);
      expect(event["action_id"], "open");
      expect(event["payload"], isNull);
    });
  });
}
