import 'dart:convert';

import 'package:flet_notifications/src/background_handler.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:shared_preferences_platform_interface/shared_preferences_platform_interface.dart';

/// In-memory store so the tap queue can be tested without platform channels.
class _FakeStore extends SharedPreferencesStorePlatform {
  final Map<String, Object> values = {};

  @override
  Future<bool> remove(String key) async {
    values.remove(key);
    return true;
  }

  @override
  Future<bool> setValue(String valueType, String key, Object value) async {
    values[key] = value;
    return true;
  }

  @override
  Future<bool> clear() async {
    values.clear();
    return true;
  }

  @override
  Future<Map<String, Object>> getAll() async {
    return {
      for (final entry in values.entries) entry.key: entry.value,
    };
  }
}

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
  late _FakeStore store;

  setUp(() {
    store = _FakeStore();
    SharedPreferencesStorePlatform.instance = store;
    SharedPreferences.resetStatic();
  });

  group("responseToEvent", () {
    test("plain tap", () {
      final event = responseToEvent(_response(payload: "hello"));
      expect(event["id"], 7);
      expect(event["action_id"], "");
      expect(event["payload"], "hello");
      expect(event["input"], "");
      expect(event["response_type"], "tap");
    });

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
      expect(event["response_type"], "action");
    });

    test("dismissed", () {
      final event = responseToEvent(
        _response(
          type: fln.NotificationResponseType.notificationDismissed,
        ),
      );
      expect(event["action_id"], "");
      expect(event["response_type"], "dismissed");
    });

    test("null payload and input become empty strings", () {
      final event = responseToEvent(_response());
      expect(event["payload"], "");
      expect(event["input"], "");
    });
  });

  group("drainTapQueue", () {
    test("returns events in key order and removes them", () async {
      final older = responseToEvent(_response(payload: "first"));
      final newer = responseToEvent(_response(payload: "second"));
      // The store contract returns keys with the legacy "flutter." prefix
      // (the real method-channel store does the same).
      store.setValue(
        "String",
        "flutter.flet_notifications_queue_100-1",
        jsonEncode(older),
      );
      store.setValue(
        "String",
        "flutter.flet_notifications_queue_200-2",
        jsonEncode(newer),
      );
      store.setValue("String", "flutter.unrelated_key", "keep me");

      // Populate the store first: the SharedPreferences instance snapshots
      // its keys at construction.
      final prefs = await SharedPreferences.getInstance();
      final drained = await drainTapQueue(prefs);
      expect(drained, hasLength(2));
      expect(drained.first["payload"], "first");
      expect(drained.last["payload"], "second");
      expect(
        prefs.getKeys().where(
          (k) => k.startsWith("flet_notifications_queue_"),
        ),
        isEmpty,
      );
      expect(prefs.getString("unrelated_key"), "keep me");
    });

    test("empty queue yields empty list", () async {
      final prefs = await SharedPreferences.getInstance();
      expect(await drainTapQueue(prefs), isEmpty);
    });

    test("unreadable entries are dropped, not fatal", () async {
      store.setValue(
        "String",
        "flutter.flet_notifications_queue_1-1",
        "not json",
      );
      final prefs = await SharedPreferences.getInstance();
      final drained = await drainTapQueue(prefs);
      expect(drained, isEmpty);
      // The bad entry is removed rather than left to wedge the queue.
      expect(prefs.getKeys(), isNot(contains("flet_notifications_queue_1-1")));
    });
  });

  group("launch fingerprint dedupe", () {
    test("emits once per unique payload", () async {
      final prefs = await SharedPreferences.getInstance();
      final event = responseToEvent(_response(payload: "hello"));
      expect(await shouldEmitLaunch(prefs, event), isTrue);
      expect(await shouldEmitLaunch(prefs, event), isFalse);
      final other = responseToEvent(_response(payload: "changed"));
      expect(await shouldEmitLaunch(prefs, other), isTrue);
    });
  });

  // ── Windows normalization ─────────────────────────────────────────────

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
    expect(event["response_type"], "action");
  });

  test("plain Android/Darwin action ids pass through untouched", () {
    const response = fln.NotificationResponse(
      id: 8,
      actionId: "reply",
      input: "typed text",
      payload: "actions",
      notificationResponseType:
          fln.NotificationResponseType.selectedNotificationAction,
    );
    final event = responseToEvent(response);
    expect(event["action_id"], "reply");
    expect(event["input"], "typed text");
    expect(event["payload"], "actions");
  });

  test("Windows tap with no data keeps an empty input", () {
    const response = fln.NotificationResponse(
      id: 9,
      actionId: '',
      input: null,
      payload: '',
      notificationResponseType:
          fln.NotificationResponseType.selectedNotification,
    );
    final event = responseToEvent(response);
    expect(event["response_type"], "tap");
    expect(event["input"], "");
  });
});
}
