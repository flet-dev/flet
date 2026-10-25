import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import '../utils/actions.dart';
import '../utils/errors.dart';
import 'android_styles.dart';

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
    throw const NotificationException.invalidArgument(
      "channel must be a NotificationChannel or an ID",
    );
  }
  final id = value["id"];
  final name = value["name"];
  if (id is! String || id.isEmpty || name is! String || name.isEmpty) {
    throw const NotificationException.invalidArgument(
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

fln.Priority? parsePriority(String? value, [fln.Priority? defaultValue]) =>
    parseEnum(fln.Priority.values,
        value == "default" ? "defaultPriority" : value, defaultValue);

fln.NotificationVisibility? parseNotificationVisibility(String? value,
        [fln.NotificationVisibility? defaultValue]) =>
    parseEnum(fln.NotificationVisibility.values, value, defaultValue);

fln.GroupAlertBehavior? parseGroupAlertBehavior(String? value,
        [fln.GroupAlertBehavior? defaultValue]) =>
    parseEnum(fln.GroupAlertBehavior.values, value, defaultValue);

fln.AndroidNotificationCategory? parseAndroidNotificationCategory(
        String? value) =>
    parseEnum(fln.AndroidNotificationCategory.values, value);

fln.Importance? parseNotificationImportance(String? value,
        [fln.Importance? defaultValue]) =>
    parseEnum(fln.Importance.values,
        value == "default" ? "defaultImportance" : value, defaultValue);

/// The `AndroidImportance` value of [importance], as [parseNotificationImportance]
/// parses it.
String notificationImportanceName(fln.Importance importance) =>
    importance == fln.Importance.defaultImportance
        ? "default"
        : importance.name;

/// Converts the vibration pattern shared by notifications and channels.
Int64List? parseNotificationVibrationPattern(Object? value) {
  final pattern = parseList(value, (item) => parseInt(item)!);
  return pattern == null ? null : Int64List.fromList(pattern);
}

fln.AndroidScheduleMode? parseAndroidScheduleMode(String? value,
        [fln.AndroidScheduleMode? defaultValue]) =>
    parseEnum(fln.AndroidScheduleMode.values, value, defaultValue);

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
    throw const NotificationException.invalidArgument(
      "foreground_service_types must be a list",
    );
  }
  if (values.isEmpty) return null;
  return parseList(values, (value) {
    final type = value is String ? parseForegroundServiceType(value) : null;
    if (type == null) {
      throw NotificationException.invalidArgument(
        "unknown foreground_service_types entry: $value",
      );
    }
    return type;
  })!
      .toSet();
}

/// Builds the Android details of a notification from an `AndroidOptions` payload.
fln.AndroidNotificationDetails parseAndroidDetails({
  required List<ParsedAction> actions,
  Map<dynamic, dynamic>? options,
}) {
  final androidOptions = options ?? const {};
  final androidActions = actions
      .map(
        (a) => fln.AndroidNotificationAction(
          a.id,
          a.title,
          showsUserInterface: a.foreground,
          cancelNotification: a.cancelNotification,
          allowGeneratedReplies: a.input != null,
          inputs: a.input == null
              ? const []
              : [
                  fln.AndroidNotificationActionInput(
                    label: a.input!.label,
                    choices: a.input!.choices,
                    allowFreeFormInput: a.input!.allowFreeFormInput,
                    allowedMimeTypes: a.input!.allowedMimeTypes,
                  ),
                ],
        ),
      )
      .toList();
  final additionalFlags = parseInt(androidOptions["additional_flags"]);
  final progress = androidOptions["progress"] as Map?;
  final group = androidOptions["group"] as Map?;
  final channel = parseNotificationChannel(androidOptions["channel"]);
  return fln.AndroidNotificationDetails(
    channel.id,
    channel.name,
    channelDescription: channel.description,
    icon: androidOptions["icon"] as String?,
    audioAttributesUsage: channel.audioAttributesUsage,
    additionalFlags:
        additionalFlags == null ? null : Int32List.fromList([additionalFlags]),
    actions: androidActions,
    styleInformation: parseStyle(androidOptions["style"]),
    importance: channel.importance,
    priority: parsePriority(
        androidOptions["priority"] as String?, fln.Priority.defaultPriority)!,
    playSound: channel.playSound,
    sound: channel.sound,
    enableVibration: channel.enableVibration,
    vibrationPattern: channel.vibrationPattern,
    groupKey: group?["key"] as String?,
    setAsGroupSummary: parseBool(group?["summary"], false)!,
    groupAlertBehavior: parseGroupAlertBehavior(
      group?["alert_behavior"] as String?,
      fln.GroupAlertBehavior.all,
    )!,
    autoCancel: parseBool(androidOptions["auto_cancel"], true)!,
    ongoing: parseBool(androidOptions["ongoing"], false)!,
    silent: parseBool(androidOptions["silent"], false)!,
    color: parseColor((androidOptions["color"] as String?)?.trim(), null),
    colorized: parseBool(androidOptions["colorized"], false)!,
    largeIcon: parseAndroidBitmap(androidOptions["large_icon"]),
    onlyAlertOnce: parseBool(androidOptions["only_alert_once"], false)!,
    showWhen: parseBool(androidOptions["show_timestamp"], true)!,
    when: (androidOptions["timestamp"] as DateTime?)?.millisecondsSinceEpoch,
    usesChronometer: parseBool(androidOptions["uses_chronometer"], false)!,
    chronometerCountDown:
        parseBool(androidOptions["chronometer_count_down"], false)!,
    channelShowBadge: channel.showBadge,
    channelBypassDnd: channel.bypassDnd,
    showProgress: progress != null,
    maxProgress: parseInt(progress?["max"], 100)!,
    progress: parseInt(progress?["value"], 0)!,
    indeterminate: parseBool(progress?["indeterminate"], false)!,
    enableLights: channel.enableLights,
    ledColor: channel.ledColor,
    ledOnMs: parseDuration(androidOptions["led_on_duration"])?.inMilliseconds,
    ledOffMs: parseDuration(androidOptions["led_off_duration"])?.inMilliseconds,
    ticker: androidOptions["ticker"] as String?,
    visibility:
        parseNotificationVisibility(androidOptions["visibility"] as String?),
    timeoutAfter:
        parseDuration(androidOptions["timeout_after"])?.inMilliseconds,
    category:
        parseAndroidNotificationCategory(androidOptions["category"] as String?),
    fullScreenIntent: parseBool(androidOptions["full_screen_intent"], false)!,
    shortcutId: androidOptions["shortcut_id"] as String?,
    subText: androidOptions["sub_text"] as String?,
    tag: androidOptions["tag"] as String?,
    number: parseInt(androidOptions["badge_number"]),
  );
}
