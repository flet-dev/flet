import 'dart:convert';
import 'dart:typed_data';

import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import 'actions.dart';
import 'errors.dart';
import 'parsers.dart';
import 'styles.dart';

/// Shared by Darwin notification details and the service's category registry.
const String darwinNotificationCategoryPrefix = "flet_notifications_actions_";

/// Converts a wire payload into the upstream platform notification details.
fln.NotificationDetails parseNotificationDetails({
  required int id,
  required List<ParsedAction> actions,
  Map? details,
}) {
  try {
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
    final androidOptions = _platformOptions(details, "android") ?? const {};
    final linuxOptions = _platformOptions(details, "linux") ?? const {};
    final webOptions = _platformOptions(details, "web") ?? const {};
    final windowsOptions = _platformOptions(details, "windows") ?? const {};
    final windowsAudio = windowsOptions["audio"] as String?;
    final additionalFlags = parseInt(androidOptions["additional_flags"]);
    final linuxTimeout = parseDuration(linuxOptions["timeout"]);
    final progress = androidOptions["progress"] as Map?;
    final group = androidOptions["group"] as Map?;
    final channel = parseNotificationChannel(androidOptions["channel"]);

    return fln.NotificationDetails(
      android: fln.AndroidNotificationDetails(
        channel.id,
        channel.name,
        channelDescription: channel.description,
        icon: androidOptions["icon"] as String?,
        audioAttributesUsage: channel.audioAttributesUsage,
        additionalFlags: additionalFlags == null
            ? null
            : Int32List.fromList([additionalFlags]),
        actions: androidActions,
        styleInformation: parseStyle(androidOptions["style"]),
        importance: channel.importance,
        priority: parsePriority(androidOptions["priority"] as String?,
            fln.Priority.defaultPriority)!,
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
        when:
            (androidOptions["timestamp"] as DateTime?)?.millisecondsSinceEpoch,
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
        ledOnMs:
            parseDuration(androidOptions["led_on_duration"])?.inMilliseconds,
        ledOffMs:
            parseDuration(androidOptions["led_off_duration"])?.inMilliseconds,
        ticker: androidOptions["ticker"] as String?,
        visibility: parseNotificationVisibility(
            androidOptions["visibility"] as String?),
        timeoutAfter:
            parseDuration(androidOptions["timeout_after"])?.inMilliseconds,
        category: parseAndroidNotificationCategory(
            androidOptions["category"] as String?),
        fullScreenIntent:
            parseBool(androidOptions["full_screen_intent"], false)!,
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
        icon: parseLinuxNotificationIcon(linuxOptions["icon"] as String?),
        sound: parseLinuxNotificationSound(linuxOptions["sound"] as String?),
        category:
            parseLinuxNotificationCategory(linuxOptions["category"] as String?),
        urgency: parseLinuxNotificationUrgency(
            linuxOptions["urgency"] as String?,
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
            : parseWindowsNotificationAudio(
                windowsAudio,
                fln.WindowsNotificationAudio.preset(
                    sound: fln.WindowsNotificationSound.defaultSound),
              ),
        duration: parseWindowsNotificationDuration(
            windowsOptions["duration"] as String?),
        scenario: parseWindowsNotificationScenario(
            windowsOptions["scenario"] as String?),
        timestamp: windowsOptions["timestamp"] as DateTime?,
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
            parseBool(webOptions["require_interaction"], false)!,
        isSilent: parseBool(webOptions["is_silent"], false)!,
        renotify: parseBool(webOptions["renotify"], false)!,
        timestamp: webOptions["timestamp"] as DateTime?,
      ),
    );
  } on FormatException catch (e) {
    throw NotificationException.invalidOption(e.message);
  } on TypeError catch (e) {
    throw NotificationException.invalidOption(
      "invalid notification option: $e",
    );
  }
}

/// Extracts one platform's options dict from the `options` payload.
Map<dynamic, dynamic>? _platformOptions(Map? details, String platform) {
  final options = details?["options"];
  if (options is! Map) return null;
  final platformOptions = options[platform];
  return platformOptions is Map ? platformOptions : null;
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
