import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

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
  return null;
}

fln.LinuxNotificationUrgency? parseLinuxNotificationUrgency(String? value,
        [fln.LinuxNotificationUrgency? defaultValue]) =>
    parseEnum(fln.LinuxNotificationUrgency.values, value, defaultValue);
