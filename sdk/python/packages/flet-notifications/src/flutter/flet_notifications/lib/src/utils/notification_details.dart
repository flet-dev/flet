import 'dart:convert';
import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import '../parsers.dart';

const String _channelId = "flet_notifications";
const String _channelName = "Notifications";

/// Shared by Darwin notification details and the service's category registry.
const String darwinNotificationCategoryPrefix = "flet_notifications_actions_";

/// Raised for invalid per-platform option values (bad category, …) so the
/// invoke returns `invalid_option` rather than a generic `invalid_action`.
class InvalidNotificationOptionException implements Exception {
  InvalidNotificationOptionException(this.message);
  final String message;
}

/// Converts a wire payload into the upstream platform notification details.
///
/// The service supplies category registration so plugin state remains there. Keep
/// this callback at its existing position: conversion failures before and after
/// registration must retain the same side effects and invoke error behavior.
Future<fln.NotificationDetails> parseNotificationDetails({
  required int id,
  required List<ParsedAction> actions,
  ParsedStyle? style,
  Map? details,
  required Future<void> Function(int, List<ParsedAction>)
      registerDarwinCategories,
}) async {
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
                    label: a.input!.label.isEmpty ? null : a.input!.label,
                    choices: a.input!.choices,
                    allowFreeFormInput: a.input!.allowFreeFormInput,
                    allowedMimeTypes: a.input!.allowedMimeTypes,
                  ),
                ],
        ),
      )
      .toList();

  final darwinDetails = _mapDarwinDetails(
    id: id,
    actions: actions,
    options: _platformOptions(details, "iOS"),
  );

  if (actions.isNotEmpty) {
    await registerDarwinCategories(id, actions);
  }

  final payloadForWindows = (details ?? const {})["payload"] as String? ?? "";
  final windowsActions = actions.map((a) {
    return fln.WindowsAction(
      content: a.title,
      arguments: jsonEncode({"id": a.id, "payload": payloadForWindows}),
      inputId: a.input == null ? null : a.id,
      activationBehavior: fln.WindowsNotificationBehavior.dismiss,
    );
  }).toList();

  // Windows renders inline replies as separate input elements; Android and
  // Darwin put them on the action itself.
  final windowsInputs = actions
      .where((a) => a.input != null)
      .map(
        (a) => fln.WindowsTextInput(
          id: a.id,
          title: a.input!.label.isEmpty ? null : a.input!.label,
          placeHolderContent: a.input!.label.isEmpty ? null : a.input!.label,
        ),
      )
      .toList();

  // Rich details forwarded from the invoke payload (all optional).
  final d = details ?? const {};
  final androidOptions = _platformOptions(details, "android") ?? const {};
  final linuxOptions = _platformOptions(details, "linux") ?? const {};
  final webOptions = _platformOptions(details, "web") ?? const {};
  final windowsOptions = _platformOptions(details, "windows") ?? const {};
  final channelId =
      (d["channel_id"] as String?) ?? (androidOptions["channel_id"] as String?);
  final groupKey = d["group_key"] as String?;
  final groupAlert = _mapGroupAlertBehavior(
    d["group_alert_behavior"] as String?,
  );

  return fln.NotificationDetails(
    android: fln.AndroidNotificationDetails(
      channelId ?? _channelId,
      _channelName,
      channelDescription: androidOptions["channel_description"] as String?,
      icon: androidOptions["icon"] as String?,
      audioAttributesUsage: parseEnum(
        fln.AudioAttributesUsage.values,
        androidOptions["audio_attributes_usage"] as String?,
        fln.AudioAttributesUsage.notification,
      )!,
      additionalFlags: androidOptions["additional_flags"] == null
          ? null
          : Int32List.fromList([androidOptions["additional_flags"] as int]),
      actions: androidActions,
      styleInformation: _mapStyleInformation(style),
      importance:
          parseNotificationImportance(androidOptions["importance"] as String?),
      priority: _mapPriority(androidOptions["priority"] as String?),
      playSound: optionalBool(androidOptions["play_sound"]) ?? true,
      sound: _mapSound(androidOptions["sound"] as String?),
      enableVibration: optionalBool(androidOptions["enable_vibration"]) ?? true,
      vibrationPattern: parseNotificationVibrationPattern(
          androidOptions["vibration_pattern"]),
      groupKey: groupKey,
      setAsGroupSummary: optionalBool(d["set_as_group_summary"]) ?? false,
      groupAlertBehavior: groupAlert,
      autoCancel: optionalBool(androidOptions["auto_cancel"]) ?? true,
      ongoing: optionalBool(androidOptions["ongoing"]) ?? false,
      silent: optionalBool(androidOptions["silent"]) ?? false,
      color: parseColor((androidOptions["color"] as String?)?.trim(), null),
      colorized: optionalBool(androidOptions["colorized"]) ?? false,
      largeIcon: _mapLargeIcon(androidOptions["large_icon"] as String?),
      onlyAlertOnce: optionalBool(androidOptions["only_alert_once"]) ?? false,
      showWhen: optionalBool(androidOptions["show_when"]) ?? true,
      when: androidOptions["when"] as int?,
      usesChronometer:
          optionalBool(androidOptions["uses_chronometer"]) ?? false,
      chronometerCountDown:
          optionalBool(androidOptions["chronometer_count_down"]) ?? false,
      channelShowBadge:
          optionalBool(androidOptions["channel_show_badge"]) ?? true,
      channelBypassDnd:
          optionalBool(androidOptions["channel_bypass_dnd"]) ?? false,
      showProgress: optionalBool(d["show_progress"]) ?? false,
      maxProgress: (d["max_progress"] as int?) ?? 0,
      progress: (d["progress"] as int?) ?? 0,
      indeterminate: optionalBool(d["indeterminate"]) ?? false,
      enableLights: optionalBool(androidOptions["enable_lights"]) ?? false,
      ledColor:
          parseColor((androidOptions["led_color"] as String?)?.trim(), null),
      ledOnMs: androidOptions["led_on_ms"] as int?,
      ledOffMs: androidOptions["led_off_ms"] as int?,
      ticker: androidOptions["ticker"] as String?,
      visibility: _mapVisibility(androidOptions["visibility"] as String?),
      timeoutAfter: androidOptions["timeout_after"] as int?,
      category: _mapCategory(androidOptions["category"] as String?),
      fullScreenIntent:
          optionalBool(androidOptions["full_screen_intent"]) ?? false,
      shortcutId: androidOptions["shortcut_id"] as String?,
      subText: androidOptions["sub_text"] as String?,
      tag: androidOptions["tag"] as String?,
      number: androidOptions["number"] as int?,
    ),
    iOS: darwinDetails,
    macOS: _mapDarwinDetails(
      id: id,
      actions: actions,
      options: _platformOptions(details, "macOS"),
    ),
    linux: fln.LinuxNotificationDetails(
      defaultActionName: "Open",
      icon: _mapLinuxIcon(linuxOptions["icon"] as String?),
      sound: _mapLinuxSound(linuxOptions["sound"] as String?),
      category: _mapLinuxCategory(linuxOptions["category"] as String?),
      urgency: _mapLinuxUrgency(linuxOptions["urgency"] as String?),
      timeout: linuxOptions["timeout_ms"] == null
          ? const fln.LinuxNotificationTimeout.systemDefault()
          : fln.LinuxNotificationTimeout.fromDuration(
              Duration(milliseconds: linuxOptions["timeout_ms"] as int),
            ),
      resident: optionalBool(linuxOptions["resident"]) ?? false,
      transient: optionalBool(linuxOptions["transient"]) ?? false,
      suppressSound: optionalBool(linuxOptions["suppress_sound"]) ?? false,
      actionKeyAsIconName:
          optionalBool(linuxOptions["action_key_as_icon_name"]) ?? false,
    ),
    windows: fln.WindowsNotificationDetails(
      actions: windowsActions,
      inputs: windowsInputs,
      header: _mapWindowsHeader(windowsOptions["header"] as String?),
      audio: _mapWindowsAudio(windowsOptions["audio"] as String?),
      duration: _mapWindowsDuration(windowsOptions["duration"] as String?),
      scenario: _mapWindowsScenario(windowsOptions["scenario"] as String?),
      timestamp: windowsOptions["timestamp"] == null
          ? null
          : DateTime.fromMillisecondsSinceEpoch(
              windowsOptions["timestamp"] as int,
            ),
      subtitle: windowsOptions["subtitle"] as String?,
      images: (windowsOptions["images"] as List?)
              ?.map((e) => fln.WindowsImage(Uri.parse("$e"), altText: ""))
              .toList() ??
          const [],
      bindings: (windowsOptions["bindings"] as Map?)?.map(
            (k, v) => MapEntry("$k", "$v"),
          ) ??
          const {},
    ),
    web: fln.WebNotificationDetails(
      actions: actions
          .map((a) => fln.WebNotificationAction(action: a.id, title: a.title))
          .toList(),
      direction: parseEnum(
        fln.WebNotificationDirection.values,
        webOptions["direction"] as String?,
        fln.WebNotificationDirection.auto,
      )!,
      badgeUrl: webOptions["badge_url"] == null
          ? null
          : Uri.parse(webOptions["badge_url"] as String),
      iconUrl: webOptions["icon_url"] == null
          ? null
          : Uri.parse(webOptions["icon_url"] as String),
      imageUrl: webOptions["image_url"] == null
          ? null
          : Uri.parse(webOptions["image_url"] as String),
      lang: webOptions["lang"] as String?,
      requireInteraction:
          optionalBool(webOptions["require_interaction"]) ?? false,
      isSilent: optionalBool(webOptions["is_silent"]) ?? false,
      renotify: optionalBool(webOptions["renotify"]) ?? false,
      timestamp: webOptions["timestamp"] == null
          ? null
          : DateTime.fromMillisecondsSinceEpoch(webOptions["timestamp"] as int),
    ),
  );
}

/// Extracts one platform's options dict from the ``options`` payload.
Map<dynamic, dynamic>? _platformOptions(Map? details, String platform) {
  final options = details?["options"];
  if (options is! Map) return null;
  final platformOptions = options[platform];
  return platformOptions is Map ? platformOptions : null;
}

fln.AndroidNotificationSound? _mapSound(String? sound) {
  if (sound == null || sound.isEmpty) return null;
  if (sound.startsWith("content://") || sound.startsWith("file://")) {
    return fln.UriAndroidNotificationSound(sound);
  }
  return fln.RawResourceAndroidNotificationSound(sound);
}

/// Notification large icons accept bitmaps (drawable, file path or bytes).
fln.AndroidBitmap<Object>? _mapLargeIcon(String? source) {
  if (source == null || source.isEmpty) return null;
  if (source.startsWith("/") || source.contains("\\")) {
    return fln.FilePathAndroidBitmap(source);
  }
  return fln.DrawableResourceAndroidBitmap(source);
}

fln.DarwinNotificationDetails _mapDarwinDetails({
  required int id,
  required List<ParsedAction> actions,
  Map<dynamic, dynamic>? options,
}) {
  final o = options ?? const {};
  return fln.DarwinNotificationDetails(
    categoryIdentifier:
        actions.isEmpty ? null : "$darwinNotificationCategoryPrefix$id",
    presentAlert: optionalBool(o["present_alert"]),
    presentBadge: optionalBool(o["present_badge"]),
    presentSound: optionalBool(o["present_sound"]),
    presentBanner: optionalBool(o["present_banner"]),
    presentList: optionalBool(o["present_list"]),
    sound: o["sound"] as String?,
    badgeNumber: o["badge_number"] as int?,
    subtitle: o["subtitle"] as String?,
    threadIdentifier: o["thread_identifier"] as String?,
    interruptionLevel: _mapInterruptionLevel(
      o["interruption_level"] as String?,
    ),
    criticalSoundVolume: (o["critical_sound_volume"] as num?)?.toDouble(),
    attachments: (o["attachments"] as List?)
            ?.map((e) => fln.DarwinNotificationAttachment("$e"))
            .toList() ??
        const [],
  );
}

fln.Priority _mapPriority(String? value) {
  switch (value) {
    case "min":
      return fln.Priority.min;
    case "low":
      return fln.Priority.low;
    case "high":
      return fln.Priority.high;
    case "max":
      return fln.Priority.max;
    default:
      return fln.Priority.defaultPriority;
  }
}

fln.NotificationVisibility? _mapVisibility(String? value) {
  switch (value) {
    case "public":
      return fln.NotificationVisibility.public;
    case "private":
      return fln.NotificationVisibility.private;
    case "secret":
      return fln.NotificationVisibility.secret;
    default:
      return null;
  }
}

fln.InterruptionLevel? _mapInterruptionLevel(String? value) {
  switch (value) {
    case "passive":
      return fln.InterruptionLevel.passive;
    case "active":
      return fln.InterruptionLevel.active;
    case "timeSensitive":
      return fln.InterruptionLevel.timeSensitive;
    case "critical":
      return fln.InterruptionLevel.critical;
    default:
      return null;
  }
}

fln.LinuxNotificationIcon? _mapLinuxIcon(String? name) {
  if (name == null || name.isEmpty) return null;
  if (name.startsWith("/") || name.startsWith("file://")) {
    return fln.FilePathLinuxIcon(name);
  }
  return fln.ThemeLinuxIcon(name);
}

fln.LinuxNotificationSound? _mapLinuxSound(String? name) {
  if (name == null || name.isEmpty) return null;
  return fln.ThemeLinuxSound(name);
}

fln.LinuxNotificationCategory? _mapLinuxCategory(String? value) {
  if (value == null) return null;
  for (final category in fln.LinuxNotificationCategory.values) {
    if (category.name == value) return category;
  }
  throw FormatException("unknown Linux notification category: $value");
}

fln.LinuxNotificationUrgency? _mapLinuxUrgency(String? value) {
  switch (value) {
    case "low":
      return fln.LinuxNotificationUrgency.low;
    case "critical":
      return fln.LinuxNotificationUrgency.critical;
    default:
      return fln.LinuxNotificationUrgency.normal;
  }
}

fln.WindowsHeader? _mapWindowsHeader(String? title) {
  if (title == null || title.isEmpty) return null;
  return fln.WindowsHeader(id: "header", title: title, arguments: "");
}

fln.WindowsNotificationAudio? _mapWindowsAudio(String? value) {
  if (value == null || value.isEmpty) return null;
  if (value == "silent") return fln.WindowsNotificationAudio.silent();
  const presets = {
    "default": fln.WindowsNotificationSound.defaultSound,
    "im": fln.WindowsNotificationSound.im,
    "mail": fln.WindowsNotificationSound.mail,
    "reminder": fln.WindowsNotificationSound.reminder,
    "sms": fln.WindowsNotificationSound.sms,
  };
  return fln.WindowsNotificationAudio.preset(
    sound: presets[value] ?? fln.WindowsNotificationSound.defaultSound,
  );
}

fln.WindowsNotificationDuration? _mapWindowsDuration(String? value) {
  switch (value) {
    case "long":
      return fln.WindowsNotificationDuration.long;
    case "short":
      return fln.WindowsNotificationDuration.short;
    default:
      return null;
  }
}

fln.WindowsNotificationScenario? _mapWindowsScenario(String? value) {
  switch (value) {
    case "reminder":
      return fln.WindowsNotificationScenario.reminder;
    case "alarm":
      return fln.WindowsNotificationScenario.alarm;
    case "incomingCall":
      return fln.WindowsNotificationScenario.incomingCall;
    case "urgent":
      return fln.WindowsNotificationScenario.urgent;
    default:
      return null;
  }
}

/// Maps a parsed style onto the Android `styleInformation` object.
///
/// Styles are an Android concept in the plugin; iOS/macOS render titles,
/// attachments and interruptions through their own details fields.
fln.StyleInformation? _mapStyleInformation(ParsedStyle? style) {
  if (style == null) return null;
  switch (style.type) {
    case "big_text":
      return fln.BigTextStyleInformation(
        style.bigText!,
        contentTitle: style.contentTitle,
        summaryText: style.summaryText,
      );
    case "big_picture":
      return fln.BigPictureStyleInformation(
        _mapBitmap(style.image!)!,
        largeIcon: _mapBitmap(style.largeIcon),
        contentTitle: style.contentTitle,
        summaryText: style.summaryText,
      );
    case "inbox":
      return fln.InboxStyleInformation(
        style.lines,
        contentTitle: style.contentTitle,
        summaryText: style.summaryText,
      );
    case "messaging":
      return fln.MessagingStyleInformation(
        _mapPerson(style.person!),
        conversationTitle: style.conversationTitle,
        groupConversation: style.groupConversation,
        messages: style.messages
            .map(
              (m) => fln.Message(
                m.text,
                DateTime.parse(m.timestampIso),
                _mapPerson(m.person),
              ),
            )
            .toList(),
      );
    default:
      throw FormatException("unknown style type: ${style.type}");
  }
}

/// Maps an icon onto a style image. FLN's big-picture bitmaps support
/// drawable, file-path and byte sources only.
fln.AndroidBitmap<Object>? _mapBitmap(ParsedIcon? icon) {
  if (icon == null) return null;
  final drawable = icon.drawableResource;
  if (drawable != null) return fln.DrawableResourceAndroidBitmap(drawable);
  final path = icon.filePath;
  if (path != null) return fln.FilePathAndroidBitmap(path);
  final data = icon.data;
  if (data != null) return fln.ByteArrayAndroidBitmap(Uint8List.fromList(data));
  throw const FormatException(
    "big-picture images support drawable, file path and byte sources",
  );
}

/// Maps an icon onto an Android notification icon (all five sources).
fln.AndroidIcon<Object>? _mapIcon(ParsedIcon? icon) {
  if (icon == null) return null;
  final drawable = icon.drawableResource;
  if (drawable != null) return fln.DrawableResourceAndroidIcon(drawable);
  final path = icon.filePath;
  if (path != null) return fln.BitmapFilePathAndroidIcon(path);
  final uri = icon.contentUri;
  if (uri != null) return fln.ContentUriAndroidIcon(uri);
  final asset = icon.flutterAsset;
  if (asset != null) return fln.FlutterBitmapAssetAndroidIcon(asset);
  final data = icon.data;
  if (data != null) return fln.ByteArrayAndroidIcon(Uint8List.fromList(data));
  throw const FormatException("icon has no source");
}

fln.Person _mapPerson(ParsedPerson person) {
  return fln.Person(
    name: person.name,
    key: person.key,
    bot: person.bot,
    important: person.important,
    uri: person.uri,
    icon: _mapIcon(person.icon),
  );
}

fln.GroupAlertBehavior _mapGroupAlertBehavior(String? value) {
  switch (value) {
    case "summary":
      return fln.GroupAlertBehavior.summary;
    case "children":
      return fln.GroupAlertBehavior.children;
    default:
      return fln.GroupAlertBehavior.all;
  }
}

fln.AndroidNotificationCategory? _mapCategory(String? value) {
  if (value == null) return null;
  switch (value) {
    case "alarm":
      return fln.AndroidNotificationCategory.alarm;
    case "call":
      return fln.AndroidNotificationCategory.call;
    case "email":
      return fln.AndroidNotificationCategory.email;
    case "error":
      return fln.AndroidNotificationCategory.error;
    case "event":
      return fln.AndroidNotificationCategory.event;
    case "locationSharing":
      return fln.AndroidNotificationCategory.locationSharing;
    case "message":
      return fln.AndroidNotificationCategory.message;
    case "missedCall":
      return fln.AndroidNotificationCategory.missedCall;
    case "navigation":
      return fln.AndroidNotificationCategory.navigation;
    case "progress":
      return fln.AndroidNotificationCategory.progress;
    case "promo":
      return fln.AndroidNotificationCategory.promo;
    case "recommendation":
      return fln.AndroidNotificationCategory.recommendation;
    case "reminder":
      return fln.AndroidNotificationCategory.reminder;
    case "service":
      return fln.AndroidNotificationCategory.service;
    case "social":
      return fln.AndroidNotificationCategory.social;
    case "status":
      return fln.AndroidNotificationCategory.status;
    case "stopwatch":
      return fln.AndroidNotificationCategory.stopwatch;
    case "system":
      return fln.AndroidNotificationCategory.system;
    case "transport":
      return fln.AndroidNotificationCategory.transport;
    case "workout":
      return fln.AndroidNotificationCategory.workout;
    default:
      throw InvalidNotificationOptionException(
        "unknown notification category: $value",
      );
  }
}

/// Converts importance for both notifications and explicitly created channels.
fln.Importance parseNotificationImportance(String? value) {
  switch (value) {
    case "unspecified":
      return fln.Importance.unspecified;
    case "min":
      return fln.Importance.min;
    case "none":
      return fln.Importance.none;
    case "low":
      return fln.Importance.low;
    case "high":
      return fln.Importance.high;
    case "max":
      return fln.Importance.max;
    default:
      return fln.Importance.defaultImportance;
  }
}

/// Converts the vibration pattern shared by notifications and channels.
Int64List? parseNotificationVibrationPattern(Object? value) {
  if (value is! List) return null;
  return Int64List.fromList(value.map((e) => e as int).toList());
}
