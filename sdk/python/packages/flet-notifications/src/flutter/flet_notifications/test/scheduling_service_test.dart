import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:timezone/timezone.dart' as tz;

import 'fakes.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  late RecordingAndroid plugin;
  setUp(() => plugin = resetNotifications());

  test("periodic intervals select presets or custom durations", () async {
    final service = makeService();
    for (final (interval, expected) in <(Object, Object)>[
      ("HOURLY", fln.RepeatInterval.hourly),
      ({"minutes": 15}, const Duration(minutes: 15)),
    ]) {
      final result = await invoke(service, "periodically_show", {
        "id": 1,
        "title": "Reminder",
        "body": "Take a break",
        "payload": "break",
        "repeat_interval": interval,
      });
      expect(result, null);
      expect(plugin.periodicCalls.last, {
        'interval': expected,
        'title': 'Reminder',
        'body': 'Take a break',
        'payload': 'break',
        'scheduleMode': fln.AndroidScheduleMode.inexactAllowWhileIdle,
      });
    }
  });

  test("schedule retains its native arguments after validation", () async {
    final service = makeService();
    expect(
        await invoke(service, "schedule", {
          "id": 4,
          "title": "Reminder",
          "body": "Meeting",
          "payload": "meeting:4",
          "when": {
            "iso": "2099-06-01T14:00:00+02:00",
            "utc_offset_seconds": 7200,
            "timezone": "UTC"
          },
          "schedule_mode": "inexactAllowWhileIdle",
          "match_components": "dayOfWeekAndTime",
        }),
        null);
    final call = plugin.scheduledCalls.single;
    expect(call["id"], 4);
    expect(call["title"], "Reminder");
    expect(call["body"], "Meeting");
    expect(call["payload"], "meeting:4");
    expect((call["scheduledDate"] as tz.TZDateTime).toUtc(),
        DateTime.utc(2099, 6, 1, 12));
    expect(call["scheduleMode"], fln.AndroidScheduleMode.inexactAllowWhileIdle);
    expect(call["matchComponents"], fln.DateTimeComponents.dayOfWeekAndTime);
  });
}
