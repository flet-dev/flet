import 'package:flet/flet.dart';

/// Reads a calendar day (no time) from a control property.
///
/// Python may send a `date` (parsed as local midnight), a naive or aware
/// `datetime` (sent as a UTC instant), or a day picked earlier by these
/// controls, which is sent as midnight UTC (see [dayToPython]). UTC midnight
/// is read in UTC; anything else is read in local time.
DateTime? getDay(Control control, String propertyName) {
  final raw = control.get(propertyName);
  if (raw is! DateTime) return null;
  final isUtcMidnight =
      raw.isUtc &&
      raw.hour == 0 &&
      raw.minute == 0 &&
      raw.second == 0 &&
      raw.millisecond == 0 &&
      raw.microsecond == 0;
  final day = isUtcMidnight ? raw : raw.toLocal();
  return DateTime(day.year, day.month, day.day);
}

/// Converts a picked day to midnight UTC, so `value.date()` in Python gives
/// that day whatever the local time zone is.
DateTime? dayToPython(DateTime? day) =>
    day == null ? null : DateTime.utc(day.year, day.month, day.day);

/// The `min_date`/`max_date` limits of a picker control.
///
/// shadcn_ui has no min/max date: `fromMonth`/`toMonth` limit navigation and
/// [isSelectable] disables the days outside the range.
class DayBounds {
  final DateTime? min;
  final DateTime? max;

  DayBounds(Control control)
    : min = getDay(control, "min_date"),
      max = getDay(control, "max_date");

  DateTime? get fromMonth =>
      min == null ? null : DateTime(min!.year, min!.month);

  DateTime? get toMonth => max == null ? null : DateTime(max!.year, max!.month);

  bool Function(DateTime day)? get isSelectable => min == null && max == null
      ? null
      : (day) =>
            (min == null || !day.isBefore(min!)) &&
            (max == null || !day.isAfter(max!));
}
