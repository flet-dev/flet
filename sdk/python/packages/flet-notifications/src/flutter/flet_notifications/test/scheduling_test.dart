import 'package:flet_notifications/src/utils/scheduling.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:timezone/data/latest_all.dart' as tz;
import 'package:timezone/timezone.dart' as tz;

void main() {
  setUpAll(() => tz.initializeTimeZones());

  test("naive wall clock in the target zone", () {
    final date = parseWhen({
      "when": {"iso": "2030-01-15T09:30:00", "time_zone": "Africa/Lagos"},
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
      "when": {"iso": "2030-03-01T08:00:00", "time_zone": null},
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
        "time_zone": "UTC",
      },
    }, tz.local);
    expect(date.hour, 11);
    expect(date.minute, 0);
    expect(date.location.name, "UTC");
  });

  test("delay from now lands in the future", () {
    final date = parseWhen({
      "when": {"delay_seconds": "90", "time_zone": "UTC"},
    }, tz.UTC);
    expect(
      date.difference(tz.TZDateTime.now(tz.UTC)).inSeconds,
      inInclusiveRange(85, 90),
    );
  });
}
