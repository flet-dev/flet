import 'package:collection/collection.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../models/control.dart';
import 'numbers.dart';

Duration? parseDuration(dynamic value, [Duration? defaultValue]) {
  if (value == null) return defaultValue;
  if (value is int || value is double) {
    return Duration(milliseconds: parseInt(value, 0)!);
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
  Duration? getDuration(String propertyName, [Duration? defaultValue]) {
    return parseDuration(get(propertyName), defaultValue);
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
    return get<DateTime>(propertyName, defaultValue);
  }

  TimeOfDay? getTimeOfDay(String propertyName, [TimeOfDay? defaultValue]) {
    return get<TimeOfDay>(propertyName, defaultValue);
  }
}
