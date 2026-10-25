import 'dart:convert';

import 'package:flet_notifications/src/platforms/windows.dart';
import 'package:flet_notifications/src/responses/responses.dart';
import 'package:flutter/foundation.dart';
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

  group("drainResponseQueue", () {
    test("returns events in key order and removes them", () async {
      final older = responseToEvent(_response(payload: "first"));
      final newer = responseToEvent(_response(payload: "second"));
      await prefs.setString(
          "flet_notifications_queue_200-2", jsonEncode(newer));
      await prefs.setString(
          "flet_notifications_queue_100-1", jsonEncode(older));
      await prefs.setString("unrelated_key", "keep me");

      expect(await drainResponseQueue(prefs), [older, newer]);
      expect(await drainResponseQueue(prefs), isEmpty);
      expect(await prefs.getKeys(), {"unrelated_key"});
    });

    test("unreadable entries are dropped, not fatal", () async {
      await prefs.setString("flet_notifications_queue_1-1", "not json");
      expect(await drainResponseQueue(prefs), isEmpty);
      // The bad entry is removed rather than left to wedge the queue.
      expect(await prefs.getKeys(), isEmpty);
    });

    test("background taps are queued for the main isolate", () async {
      final response = _response(payload: "background");
      notificationResponseBackground(response);
      await pumpEventQueue();
      expect(await drainResponseQueue(prefs), [responseToEvent(response)]);
    });
  });

  group("Windows responses", () {
    setUp(() => debugDefaultTargetPlatformOverride = TargetPlatform.windows);
    tearDown(() => debugDefaultTargetPlatformOverride = null);

    // The Windows plugin reports every click as an action whose actionId and
    // payload are the clicked element's launch arguments, with no id.
    fln.NotificationResponse windowsClick(String arguments,
            {Map<String, String> data = const {}}) =>
        fln.NotificationResponse(
          actionId: arguments,
          payload: arguments,
          notificationResponseType:
              fln.NotificationResponseType.selectedNotificationAction,
          data: data,
        );

    test("a click on the body is a tap with the notification's id", () {
      final event = responseToEvent(windowsClick(
          windowsLaunchArguments(notificationId: 7, payload: "probe")));
      expect(event["event"], "tap");
      expect(event["id"], 7);
      expect(event["payload"], "probe");
      expect(event.containsKey("action_id"), isFalse);
    });

    test("a button click is an action with the notification's id", () {
      final event = responseToEvent(windowsClick(
          windowsLaunchArguments(
              notificationId: 7, payload: "actions", actionId: "reply"),
          data: {"reply": "typed on windows"}));
      expect(event["event"], "action");
      expect(event["id"], 7);
      expect(event["action_id"], "reply");
      expect(event["payload"], "actions");
      expect(event["input"], "typed on windows"); // normalized from data
    });

    test("launch arguments without a payload yield no payload", () {
      final event = responseToEvent(windowsClick(
          windowsLaunchArguments(notificationId: 7, payload: null)));
      expect(event["event"], "tap");
      expect(event["payload"], isNull);
    });

    test("other platforms' JSON action ids are not taken for launch arguments",
        () {
      const response = fln.NotificationResponse(
        id: 3,
        actionId: '{"id": "x"}',
        notificationResponseType:
            fln.NotificationResponseType.selectedNotificationAction,
      );
      final event = responseToEvent(response);
      expect(event["event"], "action");
      expect(event["id"], 3);
      expect(event["action_id"], '{"id": "x"}');
    });
  });

  test("an action id shaped like Windows launch arguments is kept elsewhere",
      () {
    debugDefaultTargetPlatformOverride = TargetPlatform.android;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    const response = fln.NotificationResponse(
      id: 3,
      actionId: '{"notification": 9}',
      notificationResponseType:
          fln.NotificationResponseType.selectedNotificationAction,
    );
    final event = responseToEvent(response);
    expect(event["event"], "action");
    expect(event["id"], 3);
    expect(event["action_id"], '{"notification": 9}');
  });

  test("Windows launch arguments with wrongly typed fields are not decoded",
      () {
    expect(decodeWindowsLaunchArguments('{"notification": "reply"}'), isNull);
  });
}
