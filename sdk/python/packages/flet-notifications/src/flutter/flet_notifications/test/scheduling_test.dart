import 'package:flet_notifications/src/utils/scheduling.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

void main() {
  setUpAll(() => tz.initializeTimeZones());

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
    for (final microseconds in [90000000, 1500001, 500000, 1, 0, -1]) {
      final delay = Duration(microseconds: microseconds);
      final before = tz.TZDateTime.now(location);
      final date = parseWhen({
        "when": {"delay_ms": microseconds, "timezone": "Africa/Lagos"},
      }, tz.UTC);
      final after = tz.TZDateTime.now(location);
      expect(date.location.name, "Africa/Lagos");
      expect(date.isBefore(before.add(delay)), isFalse,
          reason: "$microseconds");
      expect(date.isAfter(after.add(delay)), isFalse, reason: "$microseconds");
    }
  });
}
