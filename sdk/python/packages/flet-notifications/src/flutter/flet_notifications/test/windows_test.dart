import 'package:flet_notifications/src/platforms/windows.dart';
import 'package:flet_notifications/src/utils/actions.dart';
import 'package:flet_notifications/src/utils/details.dart'
    as notification_details;
import 'package:flutter/foundation.dart'
    show debugDefaultTargetPlatformOverride, TargetPlatform;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';

import 'fakes.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUp(resetNotifications);

  test("Windows sounds are selected by name and can loop", () {
    fln.WindowsNotificationAudio? audio(Map<String, Object?> windows) =>
        notification_details
            .parseNotificationDetails(
              actions: const [],
              details: {
                "options": {"windows": windows},
              },
            )
            .windows!
            .audio;

    expect(audio({"sound": "default"})!.source,
        fln.WindowsNotificationSound.defaultSound.name);
    expect(audio({"sound": "alarm3"})!.shouldLoop, isFalse);
    final looping = audio({"sound": "call10", "loop_sound": true})!;
    expect(looping.source, fln.WindowsNotificationSound.call10.name);
    expect(looping.shouldLoop, isTrue);
    expect(audio({"sound": "silent"})!.isSilent, isTrue);
    expect(audio({"sound": "unknown"})!.source,
        fln.WindowsNotificationSound.defaultSound.name);
    expect(audio({}), isNull);
  });

  test("Windows progress counts up to its max", () {
    double? value(Map<String, Object?> progress) =>
        parseWindowsProgress({"status": "Downloading", ...progress}).value;
    expect(value({"value": 30}), 0.3);
    expect(value({"value": 3, "max": 10}), 0.3);
    expect(value({"value": 30, "indeterminate": true}), isNull);
  });

  test("Windows buttons carry launch arguments and link their reply inputs",
      () {
    final windows = notification_details.parseNotificationDetails(
      actions: parseActions([
        {"id": "open", "title": "Open"},
        {
          "id": "reply",
          "title": "Reply",
          "input": {"label": "Message"}
        },
      ]),
      details: {"id": 7, "payload": "chat"},
    ).windows!;
    expect(
        windows.actions.map((a) => decodeWindowsLaunchArguments(a.arguments)), [
      (notificationId: 7, actionId: "open", payload: "chat"),
      (notificationId: 7, actionId: "reply", payload: "chat"),
    ]);
    expect(windows.actions.map((a) => a.inputId), [null, "reply"]);
    expect(
        windows.inputs.map((i) => (i as fln.WindowsTextInput).id), ["reply"]);
  });

  test("Windows progress updates in place and reports dismissed notifications",
      () async {
    debugDefaultTargetPlatformOverride = TargetPlatform.windows;
    addTearDown(() => debugDefaultTargetPlatformOverride = null);
    final windows = FakeWindowsPlugin();
    fln.FlutterLocalNotificationsPlatform.instance = windows;
    final service = makeService();

    expect(
        await invoke(service, "update_windows_progress", {
          "id": 5,
          "progress": {
            "status": "Downloading",
            "value": 3,
            "max": 10,
            "label": "3/10",
          },
        }),
        true);
    final (id, bar) = windows.updates.single;
    expect(id, 5);
    expect(bar.id, "progress");
    expect(bar.value, 0.3);
    expect(bar.label, "3/10");

    expect(
        await invoke(service, "update_windows_progress", {
          "id": 5,
          "progress": {"status": "Downloading", "indeterminate": true},
        }),
        true);
    expect(windows.updates.last.$2.value, isNull);
    expect(windows.updates.last.$2.label, isNull);

    const progress = {
      "id": 5,
      "progress": {"status": "Downloading"},
    };
    windows.updateResult = fln.NotificationUpdateResult.notFound;
    expect(await invoke(service, "update_windows_progress", progress), false);
    windows.updateResult = fln.NotificationUpdateResult.error;
    expect(await invoke(service, "update_windows_progress", progress),
        startsWith("operation_failed: "));
  });
}
