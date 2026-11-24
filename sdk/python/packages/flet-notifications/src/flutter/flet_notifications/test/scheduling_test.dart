import 'package:flet_notifications/src/utils/scheduling.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:flutter_test/flutter_test.dart';
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

import 'fakes.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  setUpAll(() => tz.initializeTimeZones());

  group("parseWhen", () {
    test("naive wall clock in the target zone", () {
      final date = parseWhen({
        "when": {"iso": "2030-01-15T09:30:00", "timezone": "Africa/Lagos"},
      }, tz.UTC);
      expect(date.location.name, "Africa/Lagos");
      expect(date.year, 2030);
      expect(date.month, 1);
      expect(date.day, 15);
      expect(date.hour, 9);
      expect(date.minute, 30);
    });

    test("naive without a zone uses the fallback location", () {
      tz.setLocalLocation(tz.getLocation("Europe/Berlin"));
      addTearDown(() => tz.setLocalLocation(tz.getLocation("UTC")));
      final date = parseWhen({
        "when": {"iso": "2030-03-01T08:00:00", "timezone": null},
      }, tz.local);
      expect(date.location.name, "Europe/Berlin");
      expect(date.hour, 8);
    });

    test("aware datetime preserves the instant", () {
      // 12:00+01:00 must stay 11:00 UTC in the target zone.
      final date = parseWhen({
        "when": {
          "iso": "2030-06-01T12:00:00+01:00",
          "utc_offset_seconds": "3600",
          "timezone": "UTC",
        },
      }, tz.local);
      expect(date.hour, 11);
      expect(date.minute, 0);
      expect(date.location.name, "UTC");
    });

    test("relative delays retain fractional seconds in the target zone", () {
      final location = tz.getLocation("Africa/Lagos");
      // Delays as Python's `ft.Duration` encodes them: unit maps without zero units.
      for (final (microseconds, wire) in <(int, Map<String, int>)>[
        (90000000, {"seconds": 30, "minutes": 1}),
        (1500001, {"microseconds": 1, "milliseconds": 500, "seconds": 1}),
      ]) {
        final delay = Duration(microseconds: microseconds);
        final before = tz.TZDateTime.now(location);
        final date = parseWhen({
          "when": {"delay": wire, "timezone": "Africa/Lagos"},
        }, tz.UTC);
        final after = tz.TZDateTime.now(location);
        expect(date.location.name, "Africa/Lagos");
        expect(date.isBefore(before.add(delay)), isFalse,
            reason: "$microseconds");
        expect(date.isAfter(after.add(delay)), isFalse,
            reason: "$microseconds");
      }
    });
  });

  group("scheduling methods", () {
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
      expect(
          call["scheduleMode"], fln.AndroidScheduleMode.inexactAllowWhileIdle);
      expect(call["matchComponents"], fln.DateTimeComponents.dayOfWeekAndTime);
    });
  });
}
