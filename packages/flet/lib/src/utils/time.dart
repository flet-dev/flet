import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'numbers.dart';

enum DurationUnit { microseconds, milliseconds, seconds, minutes, hours, days }

/// Parses a dynamic [value] into a [Duration] object.
///
/// Supported input types:
/// - `null`: Returns [defaultValue].
/// - `num` (int or double): Interpreted as a single time unit specified by [treatNumAs].
/// - `Map`: Must contain one or more of the following keys with numeric values:
///   `days`, `hours`, `minutes`, `seconds`, `milliseconds`, `microseconds`.
///
/// Parameters:
/// - [value]: The input to parse. Can be `null`, `num`, or `Map<String, dynamic>`.
/// - [defaultValue]: The value to return if [value] is `null`.
/// - [treatNumAs]: Specifies the unit of time for numeric input. Defaults to `DurationUnit.milliseconds`.
///
/// Returns:
/// A [Duration] constructed from the parsed input, or [defaultValue] if input is `null`.
Duration? parseDuration(dynamic value,
    [Duration? defaultValue,
    DurationUnit treatNumAs = DurationUnit.milliseconds]) {
  if (value == null) return defaultValue;
  if (value is num) {
    final v = parseInt(value, 0)!;
    return Duration(
      microseconds: treatNumAs == DurationUnit.microseconds ? v : 0,
      milliseconds: treatNumAs == DurationUnit.milliseconds ? v : 0,
      seconds: treatNumAs == DurationUnit.seconds ? v : 0,
      minutes: treatNumAs == DurationUnit.minutes ? v : 0,
      hours: treatNumAs == DurationUnit.hours ? v : 0,
      days: treatNumAs == DurationUnit.days ? v : 0,
    );
  }
  return Duration(
      days: parseInt(value["days"], 0)!,
      hours: parseInt(value["hours"], 0)!,
      minutes: parseInt(value["minutes"], 0)!,
      seconds: parseInt(value["seconds"], 0)!,
      milliseconds: parseInt(value["milliseconds"], 0)!,
      microseconds: parseInt(value["microseconds"], 0)!);
}

TimePickerEntryMode? parseTimePickerEntryMode(String? value,
    [TimePickerEntryMode? defaultValue]) {
  if (value == null) return defaultValue;
  return TimePickerEntryMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

CupertinoDatePickerMode? parseCupertinoDatePickerMode(String? value,
    [CupertinoDatePickerMode? defaultValue]) {
  if (value == null) return defaultValue;
  return CupertinoDatePickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

CupertinoTimerPickerMode? parseCupertinoTimerPickerMode(String? value,
    [CupertinoTimerPickerMode? defaultValue]) {
  if (value == null) return defaultValue;
  return CupertinoTimerPickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

DatePickerDateOrder? parseDatePickerDateOrder(String? value,
    [DatePickerDateOrder? defaultValue]) {
  if (value == null) return defaultValue;
  return DatePickerDateOrder.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

DatePickerEntryMode? parseDatePickerEntryMode(String? value,
    [DatePickerEntryMode? defaultValue]) {
  if (value == null) return defaultValue;
  return DatePickerEntryMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

DatePickerMode? parseDatePickerMode(String? value,
    [DatePickerMode? defaultValue]) {
  if (value == null) return defaultValue;
  return DatePickerMode.values.firstWhereOrNull(
          (e) => e.name.toLowerCase() == value.toLowerCase()) ??
      defaultValue;
}

extension TimeParsers on Control {
  /// Retrieves and parses a duration value from the control's properties.
  ///
  /// Parameters:
  /// - [propertyName]: The name of the property to retrieve the value from.
  /// - [defaultValue]: The value to return if the property is not set or is `null`.
  /// - [treatNumAs]: Specifies the unit of time for numeric input. Defaults to `DurationUnit.milliseconds`.
  ///
  ///
  /// Returns:
  /// A [Duration] based on the property's value, or [defaultValue] if the value is `null`.
  Duration? getDuration(String propertyName,
      [Duration? defaultValue,
      DurationUnit treatNumAs = DurationUnit.milliseconds]) {
    return parseDuration(get(propertyName), defaultValue, treatNumAs);
  }

  DatePickerDateOrder? getDatePickerDateOrder(String propertyName,
      [DatePickerDateOrder? defaultValue]) {
    return parseDatePickerDateOrder(get(propertyName), defaultValue);
  }

  TimePickerEntryMode? getTimePickerEntryMode(String propertyName,
      [TimePickerEntryMode? defaultValue]) {
    return parseTimePickerEntryMode(get(propertyName), defaultValue);
  }

  CupertinoDatePickerMode? getCupertinoDatePickerMode(String propertyName,
      [CupertinoDatePickerMode? defaultValue]) {
    return parseCupertinoDatePickerMode(get(propertyName), defaultValue);
  }

  CupertinoTimerPickerMode? getCupertinoTimerPickerMode(String propertyName,
      [CupertinoTimerPickerMode? defaultValue]) {
    return parseCupertinoTimerPickerMode(get(propertyName), defaultValue);
  }

  DatePickerMode? getDatePickerMode(String propertyName,
      [DatePickerMode? defaultValue]) {
    return parseDatePickerMode(get(propertyName), defaultValue);
  }

  DatePickerEntryMode? getDatePickerEntryMode(String propertyName,
      [DatePickerEntryMode? defaultValue]) {
    return parseDatePickerEntryMode(get(propertyName), defaultValue);
  }

  DateTime? getDateTime(String propertyName, [DateTime? defaultValue]) {
    final value = get<DateTime>(propertyName, defaultValue); // UTC time
    return value?.toLocal();
  }

  TimeOfDay? getTimeOfDay(String propertyName, [TimeOfDay? defaultValue]) {
    return get<TimeOfDay>(propertyName, defaultValue);
  }
}
