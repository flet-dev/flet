import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import '../utils/actions.dart';

/// Launch arguments for a Windows notification or one of its buttons.
///
/// Windows hands the app a clicked element's launch arguments and nothing else:
/// the plugin reports a click on the notification's body as an action too, with
/// the arguments as its action id, and without the notification's id. Encoding
/// them lets [decodeWindowsLaunchArguments] tell the two apart and restore the
/// id and payload.
String windowsLaunchArguments({
  required int? notificationId,
  required String? payload,
  String? actionId,
}) =>
    jsonEncode({
      "notification": notificationId,
      if (actionId != null) "id": actionId,
      "payload": payload,
    });

/// Decodes [windowsLaunchArguments], or returns `null` for other strings.
({int? notificationId, String? actionId, String? payload})?
    decodeWindowsLaunchArguments(String? arguments) {
  if (arguments == null || !arguments.startsWith("{")) return null;
  try {
    final decoded = jsonDecode(arguments);
    if (decoded is! Map || !decoded.containsKey("notification")) return null;
    final (notificationId, actionId, payload) =
        (decoded["notification"], decoded["id"], decoded["payload"]);
    if (notificationId is! int? ||
        actionId is! String? ||
        payload is! String?) {
      return null;
    }
    return (
      notificationId: notificationId,
      actionId: actionId,
      payload: payload,
    );
  } on FormatException {
    return null;
  }
}

/// A Windows header with [title], under a fixed ID, so every notification with
/// a header shares one group in the notification center.
fln.WindowsHeader? parseWindowsHeader(String? title) {
  if (title == null || title.isEmpty) return null;
  return fln.WindowsHeader(id: "header", title: title, arguments: "");
}

fln.WindowsNotificationAudio? parseWindowsNotificationAudio(
  String? value, {
  bool loop = false,
  fln.WindowsNotificationAudio? defaultValue,
}) {
  if (value == null || value.isEmpty) return defaultValue;
  if (value.toLowerCase() == "silent") {
    return fln.WindowsNotificationAudio.silent();
  }
  final sound = parseEnum(fln.WindowsNotificationSound.values,
      value == "default" ? "defaultSound" : value);
  return sound == null
      ? defaultValue
      : fln.WindowsNotificationAudio.preset(sound: sound, shouldLoop: loop);
}

fln.WindowsNotificationDuration? parseWindowsNotificationDuration(String? value,
        [fln.WindowsNotificationDuration? defaultValue]) =>
    parseEnum(fln.WindowsNotificationDuration.values, value, defaultValue);

/// Converts a `WindowsProgress`, whose value counts up to its `max`, to the
/// plugin's progress bar, whose value is a fraction.
fln.WindowsProgressBar parseWindowsProgress(Map value) {
  final max = parseInt(value["max"], 100)!;
  final current = parseInt(value["value"], 0)!;
  return fln.WindowsProgressBar(
    id: "progress",
    status: value["status"] as String? ?? "",
    title: value["title"] as String?,
    label: value["label"] as String?,
    value: parseBool(value["indeterminate"], false)!
        ? null
        : max <= 0
            ? 0
            : (current / max).clamp(0.0, 1.0),
  );
}

fln.WindowsNotificationScenario? parseWindowsNotificationScenario(String? value,
        [fln.WindowsNotificationScenario? defaultValue]) =>
    parseEnum(fln.WindowsNotificationScenario.values, value, defaultValue);

/// Builds the Windows details of a notification from a `WindowsOptions` payload.
///
/// [notificationId] and [payload] go into the launch arguments of the buttons,
/// which Windows hands back on a click.
fln.WindowsNotificationDetails parseWindowsDetails({
  required List<ParsedAction> actions,
  Map<dynamic, dynamic>? options,
  int? notificationId,
  String? payload,
}) {
  final windowsOptions = options ?? const {};
  final windowsAudio = windowsOptions["sound"] as String?;
  final windowsProgress = windowsOptions["progress"] as Map?;
  final windowsActions = actions.map((a) {
    return fln.WindowsAction(
      content: a.title,
      arguments: windowsLaunchArguments(
        notificationId: notificationId,
        payload: payload,
        actionId: a.id,
      ),
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
          title: a.input!.label,
          placeHolderContent: a.input!.label,
        ),
      )
      .toList();

  return fln.WindowsNotificationDetails(
    actions: windowsActions,
    inputs: windowsInputs,
    header: parseWindowsHeader(windowsOptions["header"] as String?),
    audio: windowsAudio == null || windowsAudio.isEmpty
        ? null
        : parseWindowsNotificationAudio(
            windowsAudio,
            loop: parseBool(windowsOptions["loop_sound"], false)!,
            defaultValue: fln.WindowsNotificationAudio.preset(
                sound: fln.WindowsNotificationSound.defaultSound),
          ),
    duration:
        parseWindowsNotificationDuration(windowsOptions["duration"] as String?),
    scenario:
        parseWindowsNotificationScenario(windowsOptions["scenario"] as String?),
    timestamp: windowsOptions["timestamp"] as DateTime?,
    subtitle: windowsOptions["subtitle"] as String?,
    progressBars: [
      if (windowsProgress != null) parseWindowsProgress(windowsProgress),
    ],
    images: (windowsOptions["images"] as List?)
            ?.map((e) => fln.WindowsImage(Uri.parse("$e"), altText: ""))
            .toList() ??
        const [],
    bindings: (windowsOptions["bindings"] as Map?)?.map(
          (k, v) => MapEntry("$k", "$v"),
        ) ??
        const {},
  );
}
