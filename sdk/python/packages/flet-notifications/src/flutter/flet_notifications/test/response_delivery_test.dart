import 'dart:convert';

import 'package:flet_notifications/src/responses/responses.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'fakes.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late RecordingAndroid plugin;
  setUp(() => plugin = resetNotifications());

  test("launch replay is once per process and allows identical later taps",
      () async {
    plugin.launchDetails = const fln.NotificationAppLaunchDetails(
      true,
      notificationResponse: fln.NotificationResponse(
        id: 7,
        actionId: "reply",
        input: "Hello",
        payload: "conversation:7",
        notificationResponseType:
            fln.NotificationResponseType.selectedNotificationAction,
      ),
    );
    final firstControl = RecordingControl();
    final firstService = makeService(control: firstControl);
    expect(
        await Future.wait([
          reinitializeService(firstService),
          reinitializeService(firstService),
        ]),
        [null, null]);
    expect(await reinitializeService(firstService), null);
    expect(firstControl.events, hasLength(1));
    expect(firstControl.events.single["name"], "action");

    // A new user interaction with identical content is still delivered live.
    plugin.onResponse!(plugin.launchDetails!.notificationResponse!);
    expect(firstControl.events, hasLength(2));
    expect(firstControl.events.last, firstControl.events.first);

    // A later service, such as after a session restart, doesn't replay it.
    final nextControl = RecordingControl();
    final nextService = makeService(control: nextControl);
    expect(await reinitializeService(nextService), null);
    expect(nextControl.events, isEmpty);
  });

  test("a launch response also delivered live during startup is emitted once",
      () async {
    const response = fln.NotificationResponse(
      id: 50,
      payload: "cold launch",
      notificationResponseType:
          fln.NotificationResponseType.selectedNotification,
    );
    plugin.launchDetails = const fln.NotificationAppLaunchDetails(
      true,
      notificationResponse: response,
    );
    // Android delivers the launching tap live before launch details are read.
    plugin.onLaunchDetailsQuery = () => plugin.onResponse!(response);
    final control = RecordingControl();
    final service = makeService(control: control);
    expect(await reinitializeService(service), null);
    expect(control.events, hasLength(1));
    expect(control.events.single["name"], "tap");

    // A later tap with identical content is a new interaction and is delivered.
    plugin.onLaunchDetailsQuery = null;
    plugin.onResponse!(response);
    expect(control.events, hasLength(2));
  });

  test("responses reach the live service through an earlier one's callback",
      () async {
    const response = fln.NotificationResponse(
      id: 60,
      payload: "after restart",
      notificationResponseType:
          fln.NotificationResponseType.selectedNotification,
    );
    final firstControl = RecordingControl();
    final first = makeService(control: firstControl);
    expect(await reinitializeService(first), null);
    // Windows and Linux keep the first initialization's callback.
    final firstCallback = plugin.onResponse!;
    first.dispose();

    final nextControl = RecordingControl();
    final next = makeService(control: nextControl);
    expect(await reinitializeService(next), null);
    firstCallback(response);
    expect(firstControl.events, isEmpty);
    expect(nextControl.events.single["data"], containsPair("id", 60));
    // The event kind routes the response and is not sent to Python.
    expect(nextControl.events.single["data"], isNot(contains("event")));
  });

  test("a response without a live service is replayed by the next one",
      () async {
    const response = fln.NotificationResponse(
      id: 61,
      payload: "between sessions",
      notificationResponseType:
          fln.NotificationResponseType.selectedNotification,
    );
    final first = makeService(control: RecordingControl());
    expect(await reinitializeService(first), null);
    final callback = plugin.onResponse!;
    first.dispose();
    callback(response);
    await pumpEventQueue();

    final nextControl = RecordingControl();
    expect(await reinitializeService(makeService(control: nextControl)), null);
    expect(nextControl.events.single["data"], containsPair("id", 61));
  });

  test("a service disposed while initializing leaves the queue to the next one",
      () async {
    final prefs = SharedPreferencesAsync();
    await prefs.setString("flet_notifications_queue_1-1",
        jsonEncode({"event": "tap", "id": 62, "payload": null, "data": {}}));
    final firstControl = RecordingControl();
    final first = makeService(control: firstControl);
    final initializing = reinitializeService(first);
    first.dispose();
    await initializing;
    expect(firstControl.events, isEmpty);

    final nextControl = RecordingControl();
    expect(await reinitializeService(makeService(control: nextControl)), null);
    expect(nextControl.events.single["data"], containsPair("id", 62));
  });

  test("reinitialization does not replay an already delivered live tap",
      () async {
    final control = RecordingControl();
    final service = makeService(control: control);
    expect(await reinitializeService(service), null);
    expect(control.events, isEmpty);

    const response = fln.NotificationResponse(
      id: 7,
      payload: "opened while running",
      notificationResponseType:
          fln.NotificationResponseType.selectedNotification,
    );
    plugin.onResponse!(response);
    // Android's current activity intent now exposes this same live response.
    plugin.launchDetails = const fln.NotificationAppLaunchDetails(
      true,
      notificationResponse: response,
    );
    expect(await reinitializeService(service), null);
    expect(control.events, hasLength(1));
  });

  test("background responses are delivered while the service runs", () async {
    final control = RecordingControl();
    final service = makeService(control: control);
    expect(await reinitializeService(service), null);

    fln.NotificationResponse archive(int id) => fln.NotificationResponse(
          id: id,
          actionId: "archive",
          notificationResponseType:
              fln.NotificationResponseType.selectedNotificationAction,
        );
    // Responses arriving during a replay are delivered by a further pass.
    await Future.wait([
      notificationResponseBackground(archive(1)),
      notificationResponseBackground(archive(2)),
    ]);
    await pumpEventQueue();
    expect(control.events.map((e) => e["name"]), ["action", "action"]);
    expect(control.events.map((e) => (e["data"] as Map)["id"]), [1, 2]);
    expect(await SharedPreferencesAsync().getKeys(), isEmpty);

    // A disposed service leaves responses queued for the next one.
    service.dispose();
    await notificationResponseBackground(archive(3));
    await pumpEventQueue();
    expect(control.events, hasLength(2));
    expect(await SharedPreferencesAsync().getKeys(), hasLength(1));
  });
}
