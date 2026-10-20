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
/// The service owns category registration and supplies it as a callback. Category
/// registration completes before the remaining platform details are constructed.
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

  final darwinDetails = parseDarwinDetails(
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
  final windowsAudio = windowsOptions["audio"] as String?;
  final additionalFlags = parseInt(androidOptions["additional_flags"]);
  final linuxTimeout = parseDuration(linuxOptions["timeout"]);
  final windowsTimestamp = parseInt(windowsOptions["timestamp"]);
  final webTimestamp = parseInt(webOptions["timestamp"]);
  final channelId =
      (d["channel_id"] as String?) ?? (androidOptions["channel_id"] as String?);
  final groupKey = d["group_key"] as String?;
  final groupAlert = parseGroupAlertBehavior(
    d["group_alert_behavior"] as String?,
    fln.GroupAlertBehavior.all,
  )!;

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
      additionalFlags: additionalFlags == null
          ? null
          : Int32List.fromList([additionalFlags]),
      actions: androidActions,
      styleInformation: parseStyleInformation(style),
      importance: parseNotificationImportance(
          androidOptions["importance"] as String?,
          fln.Importance.defaultImportance)!,
      priority: parsePriority(
          androidOptions["priority"] as String?, fln.Priority.defaultPriority)!,
      playSound: parseBool(androidOptions["play_sound"], true)!,
      sound: parseSound(androidOptions["sound"] as String?),
      enableVibration: parseBool(androidOptions["enable_vibration"], true)!,
      vibrationPattern: parseNotificationVibrationPattern(
          androidOptions["vibration_pattern"]),
      groupKey: groupKey,
      setAsGroupSummary: parseBool(d["set_as_group_summary"], false)!,
      groupAlertBehavior: groupAlert,
      autoCancel: parseBool(androidOptions["auto_cancel"], true)!,
      ongoing: parseBool(androidOptions["ongoing"], false)!,
      silent: parseBool(androidOptions["silent"], false)!,
      color: parseColor((androidOptions["color"] as String?)?.trim(), null),
      colorized: parseBool(androidOptions["colorized"], false)!,
      largeIcon: parseLargeIcon(androidOptions["large_icon"] as String?),
      onlyAlertOnce: parseBool(androidOptions["only_alert_once"], false)!,
      showWhen: parseBool(androidOptions["show_when"], true)!,
      when: parseInt(androidOptions["when"]),
      usesChronometer: parseBool(androidOptions["uses_chronometer"], false)!,
      chronometerCountDown:
          parseBool(androidOptions["chronometer_count_down"], false)!,
      channelShowBadge: parseBool(androidOptions["channel_show_badge"], true)!,
      channelBypassDnd: parseBool(androidOptions["channel_bypass_dnd"], false)!,
      showProgress: parseBool(d["show_progress"], false)!,
      maxProgress: parseInt(d["max_progress"], 0)!,
      progress: parseInt(d["progress"], 0)!,
      indeterminate: parseBool(d["indeterminate"], false)!,
      enableLights: parseBool(androidOptions["enable_lights"], false)!,
      ledColor:
          parseColor((androidOptions["led_color"] as String?)?.trim(), null),
      ledOnMs: parseDuration(androidOptions["led_on_duration"])?.inMilliseconds,
      ledOffMs: parseDuration(androidOptions["led_off_duration"])?.inMilliseconds,
      ticker: androidOptions["ticker"] as String?,
      visibility: parseVisibility(androidOptions["visibility"] as String?),
      timeoutAfter:
          parseDuration(androidOptions["timeout_after"])?.inMilliseconds,
      category: parseCategory(androidOptions["category"] as String?),
      fullScreenIntent: parseBool(androidOptions["full_screen_intent"], false)!,
      shortcutId: androidOptions["shortcut_id"] as String?,
      subText: androidOptions["sub_text"] as String?,
      tag: androidOptions["tag"] as String?,
      number: parseInt(androidOptions["number"]),
    ),
    iOS: darwinDetails,
    macOS: parseDarwinDetails(
      id: id,
      actions: actions,
      options: _platformOptions(details, "macOS"),
    ),
    linux: fln.LinuxNotificationDetails(
      defaultActionName: "Open",
      icon: parseLinuxIcon(linuxOptions["icon"] as String?),
      sound: parseLinuxSound(linuxOptions["sound"] as String?),
      category: parseLinuxCategory(linuxOptions["category"] as String?),
      urgency: parseLinuxUrgency(linuxOptions["urgency"] as String?,
          fln.LinuxNotificationUrgency.normal)!,
      timeout: linuxTimeout == null
          ? const fln.LinuxNotificationTimeout.systemDefault()
          : fln.LinuxNotificationTimeout.fromDuration(linuxTimeout),
      resident: parseBool(linuxOptions["resident"], false)!,
      transient: parseBool(linuxOptions["transient"], false)!,
      suppressSound: parseBool(linuxOptions["suppress_sound"], false)!,
      actionKeyAsIconName:
          parseBool(linuxOptions["action_key_as_icon_name"], false)!,
    ),
    windows: fln.WindowsNotificationDetails(
      actions: windowsActions,
      inputs: windowsInputs,
      header: parseWindowsHeader(windowsOptions["header"] as String?),
      audio: windowsAudio == null || windowsAudio.isEmpty
          ? null
          : parseWindowsAudio(
              windowsAudio,
              fln.WindowsNotificationAudio.preset(
                  sound: fln.WindowsNotificationSound.defaultSound),
            ),
      duration: parseWindowsDuration(windowsOptions["duration"] as String?),
      scenario: parseWindowsScenario(windowsOptions["scenario"] as String?),
      timestamp: windowsTimestamp == null
          ? null
          : DateTime.fromMillisecondsSinceEpoch(windowsTimestamp),
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
      requireInteraction: parseBool(webOptions["require_interaction"], false)!,
      isSilent: parseBool(webOptions["is_silent"], false)!,
      renotify: parseBool(webOptions["renotify"], false)!,
      timestamp: webTimestamp == null
          ? null
          : DateTime.fromMillisecondsSinceEpoch(webTimestamp),
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

fln.AndroidNotificationSound? parseSound(String? sound) {
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

fln.DarwinNotificationDetails parseDarwinDetails({
  required int id,
  required List<ParsedAction> actions,
  Map<dynamic, dynamic>? options,
}) {
  final o = options ?? const {};
  return fln.DarwinNotificationDetails(
    categoryIdentifier:
        actions.isEmpty ? null : "$darwinNotificationCategoryPrefix$id",
    presentAlert: parseBool(o["present_alert"]),
    presentBadge: parseBool(o["present_badge"]),
    presentSound: parseBool(o["present_sound"]),
    presentBanner: parseBool(o["present_banner"]),
    presentList: parseBool(o["present_list"]),
    sound: o["sound"] as String?,
    badgeNumber: parseInt(o["badge_number"]),
    subtitle: o["subtitle"] as String?,
    threadIdentifier: o["thread_identifier"] as String?,
    interruptionLevel:
        parseInterruptionLevel(o["interruption_level"] as String?),
    criticalSoundVolume: parseDouble(o["critical_sound_volume"]),
    attachments: (o["attachments"] as List?)
            ?.map((e) => fln.DarwinNotificationAttachment("$e"))
            .toList() ??
        const [],
  );
}

fln.Priority? parsePriority(String? value, [fln.Priority? defaultValue]) =>
    parseEnum(fln.Priority.values, value, defaultValue);

fln.NotificationVisibility? parseVisibility(String? value,
        [fln.NotificationVisibility? defaultValue]) =>
    parseEnum(fln.NotificationVisibility.values, value, defaultValue);

fln.InterruptionLevel? parseInterruptionLevel(String? value,
        [fln.InterruptionLevel? defaultValue]) =>
    parseEnum(fln.InterruptionLevel.values, value, defaultValue);

fln.LinuxNotificationIcon? parseLinuxIcon(String? name) {
  if (name == null || name.isEmpty) return null;
  if (name.startsWith("/") || name.startsWith("file://")) {
    return fln.FilePathLinuxIcon(name);
  }
  return fln.ThemeLinuxIcon(name);
}

fln.LinuxNotificationSound? parseLinuxSound(String? name) {
  if (name == null || name.isEmpty) return null;
  return fln.ThemeLinuxSound(name);
}

fln.LinuxNotificationCategory? parseLinuxCategory(String? value) {
  if (value == null) return null;
  for (final category in fln.LinuxNotificationCategory.values) {
    if (category.name == value) return category;
  }
  throw FormatException("unknown Linux notification category: $value");
}

fln.LinuxNotificationUrgency? parseLinuxUrgency(String? value,
        [fln.LinuxNotificationUrgency? defaultValue]) =>
    parseEnum(fln.LinuxNotificationUrgency.values, value, defaultValue);

fln.WindowsHeader? parseWindowsHeader(String? title) {
  if (title == null || title.isEmpty) return null;
  return fln.WindowsHeader(id: "header", title: title, arguments: "");
}

fln.WindowsNotificationAudio? parseWindowsAudio(String? value,
    [fln.WindowsNotificationAudio? defaultValue]) {
  if (value == null || value.isEmpty) return defaultValue;
  if (value == "silent") return fln.WindowsNotificationAudio.silent();
  const presets = {
    "default": fln.WindowsNotificationSound.defaultSound,
    "im": fln.WindowsNotificationSound.im,
    "mail": fln.WindowsNotificationSound.mail,
    "reminder": fln.WindowsNotificationSound.reminder,
    "sms": fln.WindowsNotificationSound.sms,
  };
  final sound = presets[value];
  return sound == null
      ? defaultValue
      : fln.WindowsNotificationAudio.preset(sound: sound);
}

fln.WindowsNotificationDuration? parseWindowsDuration(String? value,
        [fln.WindowsNotificationDuration? defaultValue]) =>
    parseEnum(fln.WindowsNotificationDuration.values, value, defaultValue);

fln.WindowsNotificationScenario? parseWindowsScenario(String? value,
        [fln.WindowsNotificationScenario? defaultValue]) =>
    parseEnum(fln.WindowsNotificationScenario.values, value, defaultValue);

/// Converts a parsed style onto the Android `styleInformation` object.
///
/// Styles are an Android concept in the plugin; iOS/macOS render titles,
/// attachments and interruptions through their own details fields.
fln.StyleInformation? parseStyleInformation(ParsedStyle? style) {
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
        parseBitmap(style.image!)!,
        largeIcon: parseBitmap(style.largeIcon),
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
        parsePerson(style.person!),
        conversationTitle: style.conversationTitle,
        groupConversation: style.groupConversation,
        messages: style.messages
            .map(
              (m) => fln.Message(
                m.text,
                DateTime.parse(m.timestampIso),
                parsePerson(m.person),
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
fln.AndroidBitmap<Object>? parseBitmap(ParsedIcon? icon) {
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
fln.AndroidIcon<Object>? parseIcon(ParsedIcon? icon) {
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

fln.Person parsePerson(ParsedPerson person) {
  return fln.Person(
    name: person.name,
    key: person.key,
    bot: person.bot,
    important: person.important,
    uri: person.uri,
    icon: parseIcon(person.icon),
  );
}

fln.GroupAlertBehavior? parseGroupAlertBehavior(String? value,
        [fln.GroupAlertBehavior? defaultValue]) =>
    parseEnum(fln.GroupAlertBehavior.values, value, defaultValue);

fln.AndroidNotificationCategory? parseCategory(String? value) {
  if (value == null) return null;
  final category = parseEnum(fln.AndroidNotificationCategory.values, value);
  if (category != null) return category;
  throw InvalidNotificationOptionException(
    "unknown notification category: $value",
  );
}

/// Converts importance for both notifications and explicitly created channels.
fln.Importance? parseNotificationImportance(String? value,
        [fln.Importance? defaultValue]) =>
    parseEnum(fln.Importance.values, value, defaultValue);

/// Converts the vibration pattern shared by notifications and channels.
Int64List? parseNotificationVibrationPattern(Object? value) {
  final pattern = parseList(value, (item) => parseInt(item)!);
  return pattern == null ? null : Int64List.fromList(pattern);
}
