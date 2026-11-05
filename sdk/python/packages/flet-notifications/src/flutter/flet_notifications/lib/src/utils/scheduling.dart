import 'package:flet/flet.dart' show parseDuration, parseEnum, parseInt;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:timezone/timezone.dart' as tz;

import 'errors.dart';

/// Resolves the target location: an explicit IANA zone name when given,
/// otherwise `tz.local` (set from the device timezone at init).
tz.Location resolveLocation(String? timezone) {
  if (timezone != null && timezone.isNotEmpty) {
    return tz.getLocation(timezone);
  }
  return tz.local;
}

/// Parses the `when` payload of a `schedule` invoke into a [tz.TZDateTime].
///
/// - `delay` → now + delay in the target zone (from `timedelta`)
/// - `iso` with an offset → the exact instant, rendered in the target zone
/// - `iso` without an offset → wall-clock time in the target zone
tz.TZDateTime parseWhen(Map<dynamic, dynamic> args, tz.Location fallback) {
  try {
    final when = args["when"];
    if (when is! Map) {
      throw const FormatException("when must be a map");
    }
    final timezone = when["timezone"] as String?;
    final location = (timezone != null && timezone.isNotEmpty)
        ? resolveLocation(timezone)
        : fallback;

    final delay = when["delay"];
    if (delay != null) {
      if (delay is! Map) {
        throw const FormatException("delay must be a duration");
      }
      return tz.TZDateTime.now(location).add(parseDuration(delay)!);
    }

    final iso = when["iso"] as String?;
    if (iso == null) {
      throw const FormatException("when must carry delay or iso");
    }
    final parsed = DateTime.parse(iso);
    final offsetSeconds = parseInt(when["utc_offset_seconds"]);
    if (offsetSeconds != null) {
      // Aware datetime: preserve the instant, render in the target zone.
      return tz.TZDateTime.from(parsed.toUtc(), location);
    }
    // Naive datetime: wall-clock time in the target zone.
    return tz.TZDateTime(
      location,
      parsed.year,
      parsed.month,
      parsed.day,
      parsed.hour,
      parsed.minute,
      parsed.second,
      parsed.millisecond,
      parsed.microsecond,
    );
  } on FormatException catch (e) {
    throw NotificationException.invalidArgument(e.message);
  } on TypeError catch (e) {
    throw NotificationException.invalidArgument(
      "invalid schedule field: $e",
    );
  } on tz.LocationNotFoundException catch (e) {
    throw NotificationException.invalidArgument(e.toString());
  }
}

fln.DateTimeComponents? parseDateTimeComponents(String? value,
        [fln.DateTimeComponents? defaultValue]) =>
    parseEnum(fln.DateTimeComponents.values, value, defaultValue);

fln.RepeatInterval? parseRepeatInterval(String? value,
        [fln.RepeatInterval? defaultValue]) =>
    parseEnum(fln.RepeatInterval.values, value, defaultValue);
