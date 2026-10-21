import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

/// Raised for invalid per-platform option values (bad category, …) so the
/// invoke returns `invalid_option` rather than a generic `invalid_action`.
class InvalidNotificationOptionException implements Exception {
  InvalidNotificationOptionException(this.message);
  final String message;
}

fln.AndroidNotificationSound? parseAndroidNotificationSound(String? sound) {
  if (sound == null || sound.isEmpty) return null;
  if (sound.startsWith("content://") || sound.startsWith("file://")) {
    return fln.UriAndroidNotificationSound(sound);
  }
  return fln.RawResourceAndroidNotificationSound(sound);
}

/// Notification large icons accept bitmaps (drawable, file path or bytes).
fln.AndroidBitmap<Object>? parseLargeIcon(String? source) {
  if (source == null || source.isEmpty) return null;
  if (source.startsWith("/") || source.contains("\\")) {
    return fln.FilePathAndroidBitmap(source);
  }
  return fln.DrawableResourceAndroidBitmap(source);
}

fln.Priority? parsePriority(String? value, [fln.Priority? defaultValue]) =>
    parseEnum(fln.Priority.values, value, defaultValue);

fln.NotificationVisibility? parseNotificationVisibility(String? value,
        [fln.NotificationVisibility? defaultValue]) =>
    parseEnum(fln.NotificationVisibility.values, value, defaultValue);

fln.InterruptionLevel? parseInterruptionLevel(String? value,
        [fln.InterruptionLevel? defaultValue]) =>
    parseEnum(fln.InterruptionLevel.values, value, defaultValue);

fln.LinuxNotificationIcon? parseLinuxNotificationIcon(String? name) {
  if (name == null || name.isEmpty) return null;
  if (name.startsWith("/") || name.startsWith("file://")) {
    return fln.FilePathLinuxIcon(name);
  }
  return fln.ThemeLinuxIcon(name);
}

fln.LinuxNotificationSound? parseLinuxNotificationSound(String? name) {
  if (name == null || name.isEmpty) return null;
  return fln.ThemeLinuxSound(name);
}

fln.LinuxNotificationCategory? parseLinuxNotificationCategory(String? value) {
  if (value == null) return null;
  for (final category in fln.LinuxNotificationCategory.values) {
    if (category.name.toLowerCase() == value.toLowerCase()) return category;
  }
  throw FormatException("unknown Linux notification category: $value");
}

fln.LinuxNotificationUrgency? parseLinuxNotificationUrgency(String? value,
        [fln.LinuxNotificationUrgency? defaultValue]) =>
    parseEnum(fln.LinuxNotificationUrgency.values, value, defaultValue);

fln.WindowsHeader? parseWindowsHeader(String? title) {
  if (title == null || title.isEmpty) return null;
  return fln.WindowsHeader(id: "header", title: title, arguments: "");
}

fln.WindowsNotificationAudio? parseWindowsNotificationAudio(String? value,
    [fln.WindowsNotificationAudio? defaultValue]) {
  if (value == null || value.isEmpty) return defaultValue;
  if (value.toLowerCase() == "silent") {
    return fln.WindowsNotificationAudio.silent();
  }
  const presets = {
    "default": fln.WindowsNotificationSound.defaultSound,
    "im": fln.WindowsNotificationSound.im,
    "mail": fln.WindowsNotificationSound.mail,
    "reminder": fln.WindowsNotificationSound.reminder,
    "sms": fln.WindowsNotificationSound.sms,
  };
  final sound = presets[value.toLowerCase()];
  return sound == null
      ? defaultValue
      : fln.WindowsNotificationAudio.preset(sound: sound);
}

fln.WindowsNotificationDuration? parseWindowsNotificationDuration(String? value,
        [fln.WindowsNotificationDuration? defaultValue]) =>
    parseEnum(fln.WindowsNotificationDuration.values, value, defaultValue);

fln.WindowsNotificationScenario? parseWindowsNotificationScenario(String? value,
        [fln.WindowsNotificationScenario? defaultValue]) =>
    parseEnum(fln.WindowsNotificationScenario.values, value, defaultValue);

fln.GroupAlertBehavior? parseGroupAlertBehavior(String? value,
        [fln.GroupAlertBehavior? defaultValue]) =>
    parseEnum(fln.GroupAlertBehavior.values, value, defaultValue);

fln.AndroidNotificationCategory? parseAndroidNotificationCategory(
    String? value) {
  if (value == null) return null;
  final category = parseEnum(fln.AndroidNotificationCategory.values, value);
  if (category != null) return category;
  throw InvalidNotificationOptionException(
    "unknown notification category: $value",
  );
}

fln.Importance? parseNotificationImportance(String? value,
        [fln.Importance? defaultValue]) =>
    parseEnum(fln.Importance.values, value, defaultValue);

/// Converts the vibration pattern shared by notifications and channels.
Int64List? parseNotificationVibrationPattern(Object? value) {
  final pattern = parseList(value, (item) => parseInt(item)!);
  return pattern == null ? null : Int64List.fromList(pattern);
}

fln.AndroidScheduleMode? parseAndroidScheduleMode(String? value,
        [fln.AndroidScheduleMode? defaultValue]) =>
    parseEnum(fln.AndroidScheduleMode.values, value, defaultValue);

fln.DateTimeComponents? parseDateTimeComponents(String? value,
        [fln.DateTimeComponents? defaultValue]) =>
    parseEnum(fln.DateTimeComponents.values, value, defaultValue);

fln.RepeatInterval? parseRepeatInterval(String? value,
        [fln.RepeatInterval? defaultValue]) =>
    parseEnum(fln.RepeatInterval.values, value, defaultValue);

fln.AndroidServiceStartType? parseServiceStartType(String? value,
        [fln.AndroidServiceStartType? defaultValue]) =>
    parseEnum(fln.AndroidServiceStartType.values, value, defaultValue);

fln.AndroidServiceForegroundType? parseForegroundServiceType(String? value,
        [fln.AndroidServiceForegroundType? defaultValue]) =>
    parseEnum(fln.AndroidServiceForegroundType.values,
        value == null ? null : "foregroundServiceType$value", defaultValue);

/// An absent or empty list lets Android use the manifest's service types.
/// Invalid entries are rejected rather than silently changing the service type.
Set<fln.AndroidServiceForegroundType>? parseForegroundServiceTypes(
    Object? values) {
  if (values == null) return null;
  if (values is! List) {
    throw InvalidNotificationOptionException(
        "foreground_service_types must be a list");
  }
  if (values.isEmpty) return null;
  return parseList(values, (value) {
    final type = value is String ? parseForegroundServiceType(value) : null;
    if (type == null) {
      throw InvalidNotificationOptionException(
          "unknown foreground_service_types entry: $value");
    }
    return type;
  })!
      .toSet();
}
