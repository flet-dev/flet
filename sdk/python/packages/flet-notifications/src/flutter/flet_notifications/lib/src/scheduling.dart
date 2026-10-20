import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;
import 'package:timezone/timezone.dart' as tz;

/// Resolves the target location: an explicit IANA zone name when given,
/// otherwise ``tz.local`` (set from the device timezone at init).
tz.Location resolveLocation(String? timeZone) {
  if (timeZone != null && timeZone.isNotEmpty) {
    return tz.getLocation(timeZone);
  }
  return tz.local;
}

/// Parses the `when` payload of a `schedule` invoke into a [tz.TZDateTime].
///
/// - ``delay_seconds`` → now + delay in the target zone (from ``timedelta``)
/// - ``iso`` with an offset → the exact instant, rendered in the target zone
/// - ``iso`` without an offset → wall-clock time in the target zone
tz.TZDateTime parseWhen(Map<dynamic, dynamic> args, tz.Location fallback) {
  final when = args["when"];
  if (when is! Map) {
    throw const FormatException("when must be a map");
  }
  final timeZone = when["time_zone"] as String?;
  final location = (timeZone != null && timeZone.isNotEmpty)
      ? resolveLocation(timeZone)
      : fallback;

  final delay = when["delay_seconds"];
  if (delay != null) {
    final seconds = (delay as num).toInt();
    return tz.TZDateTime.now(location).add(Duration(seconds: seconds));
  }

  final iso = when["iso"] as String?;
  if (iso == null) {
    throw const FormatException("when must carry delay_seconds or iso");
  }
  final parsed = DateTime.parse(iso);
  final offsetSeconds = when["utc_offset_seconds"] as num?;
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
}

fln.AndroidScheduleMode parseScheduleMode(String? value) {
  switch (value) {
    case "alarmClock":
      return fln.AndroidScheduleMode.alarmClock;
    case "exact":
      return fln.AndroidScheduleMode.exact;
    case "inexact":
      return fln.AndroidScheduleMode.inexact;
    case "inexactAllowWhileIdle":
      return fln.AndroidScheduleMode.inexactAllowWhileIdle;
    default:
      return fln.AndroidScheduleMode.exactAllowWhileIdle;
  }
}

fln.DateTimeComponents? parseMatchComponents(String? value) {
  switch (value) {
    case "time":
      return fln.DateTimeComponents.time;
    case "dayOfWeekAndTime":
      return fln.DateTimeComponents.dayOfWeekAndTime;
    case "dayOfMonthAndTime":
      return fln.DateTimeComponents.dayOfMonthAndTime;
    case "dateAndTime":
      return fln.DateTimeComponents.dateAndTime;
    default:
      return null;
  }
}

fln.RepeatInterval parseRepeatInterval(String? value) {
  switch (value) {
    case "everyMinute":
      return fln.RepeatInterval.everyMinute;
    case "hourly":
      return fln.RepeatInterval.hourly;
    case "weekly":
      return fln.RepeatInterval.weekly;
    default:
      return fln.RepeatInterval.daily;
  }
}
