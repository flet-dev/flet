import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import '../utils/actions.dart';

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

/// Builds the Linux details of a notification from a `LinuxOptions` payload.
fln.LinuxNotificationDetails parseLinuxDetails({
  required List<ParsedAction> actions,
  Map<dynamic, dynamic>? options,
}) {
  final linuxOptions = options ?? const {};
  final linuxTimeout = parseDuration(linuxOptions["timeout"]);
  return fln.LinuxNotificationDetails(
    defaultActionName: "Open",
    icon: parseLinuxNotificationIcon(linuxOptions["icon"] as String?),
    sound: parseLinuxNotificationSound(linuxOptions["sound"] as String?),
    category:
        parseLinuxNotificationCategory(linuxOptions["category"] as String?),
    urgency: parseLinuxNotificationUrgency(linuxOptions["urgency"] as String?,
        fln.LinuxNotificationUrgency.normal)!,
    timeout: linuxTimeout == null
        ? const fln.LinuxNotificationTimeout.systemDefault()
        : fln.LinuxNotificationTimeout.fromDuration(linuxTimeout),
    resident: parseBool(linuxOptions["resident"], false)!,
    transient: parseBool(linuxOptions["transient"], false)!,
    suppressSound: parseBool(linuxOptions["silent"], false)!,
    actions: actions
        .map((a) => fln.LinuxNotificationAction(key: a.id, label: a.title))
        .toList(),
    actionKeyAsIconName:
        parseBool(linuxOptions["action_key_as_icon_name"], false)!,
  );
}
