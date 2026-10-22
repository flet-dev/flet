import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import 'errors.dart';

/// Channel used when a notification names none.
const String defaultChannelId = "flet_notifications";

/// Name given to channels created from a bare ID.
const String defaultChannelName = "Notifications";

/// Parses a `NotificationChannel` payload, or a bare channel ID, into a native
/// channel.
///
/// Missing fields take the Python `NotificationChannel` defaults, which Flet
/// omits from the wire. `null` resolves to the extension's default channel.
fln.AndroidNotificationChannel parseNotificationChannel(Object? value) {
  if (value == null || value is String) {
    final id = value as String?;
    return fln.AndroidNotificationChannel(
      id == null || id.isEmpty ? defaultChannelId : id,
      defaultChannelName,
    );
  }
  if (value is! Map) {
    throw const NotificationException.invalidChannel(
      "channel must be a NotificationChannel or an ID",
    );
  }
  final id = value["id"];
  final name = value["name"];
  if (id is! String || id.isEmpty || name is! String || name.isEmpty) {
    throw const NotificationException.invalidChannel(
        "id and name are required");
  }
  return fln.AndroidNotificationChannel(
    id,
    name,
    description: value["description"] as String?,
    groupId: value["group_id"] as String?,
    importance: parseNotificationImportance(
        value["importance"] as String?, fln.Importance.defaultImportance)!,
    bypassDnd: parseBool(value["bypass_dnd"], false)!,
    playSound: parseBool(value["play_sound"], true)!,
    sound: parseAndroidNotificationSound(value["sound"] as String?),
    enableVibration: parseBool(value["enable_vibration"], true)!,
    vibrationPattern:
        parseNotificationVibrationPattern(value["vibration_pattern"]),
    showBadge: parseBool(value["show_badge"], true)!,
    enableLights: parseBool(value["enable_lights"], false)!,
    ledColor: parseColor((value["led_color"] as String?)?.trim(), null),
    audioAttributesUsage: parseEnum(
      fln.AudioAttributesUsage.values,
      value["audio_attributes_usage"] as String?,
      fln.AudioAttributesUsage.notification,
    )!,
  );
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
  throw NotificationException.invalidOption(
    "unknown Linux notification category: $value",
  );
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
  String? value,
) {
  if (value == null) return null;
  final category = parseEnum(fln.AndroidNotificationCategory.values, value);
  if (category != null) return category;
  throw NotificationException.invalidOption(
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

fln.AndroidServiceForegroundType? parseForegroundServiceType(
  String? value, [
  fln.AndroidServiceForegroundType? defaultValue,
]) =>
    parseEnum(
      fln.AndroidServiceForegroundType.values,
      value == null ? null : "foregroundServiceType$value",
      defaultValue,
    );

/// An absent or empty list lets Android use the manifest's service types.
/// Invalid entries are rejected rather than silently changing the service type.
Set<fln.AndroidServiceForegroundType>? parseForegroundServiceTypes(
  Object? values,
) {
  if (values == null) return null;
  if (values is! List) {
    throw const NotificationException.invalidOption(
      "foreground_service_types must be a list",
    );
  }
  if (values.isEmpty) return null;
  return parseList(values, (value) {
    final type = value is String ? parseForegroundServiceType(value) : null;
    if (type == null) {
      throw NotificationException.invalidOption(
        "unknown foreground_service_types entry: $value",
      );
    }
    return type;
  })!
      .toSet();
}
