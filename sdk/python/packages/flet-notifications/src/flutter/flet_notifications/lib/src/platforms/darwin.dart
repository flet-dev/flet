import 'dart:convert';

import 'package:flet/flet.dart';
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import '../utils/actions.dart';

/// Builds the iOS or macOS details of a notification from a `DarwinOptions` payload.
fln.DarwinNotificationDetails parseDarwinDetails({
  required List<ParsedAction> actions,
  Map<dynamic, dynamic>? options,
}) {
  final o = options ?? const {};
  return fln.DarwinNotificationDetails(
    categoryIdentifier: actions.isEmpty
        ? null
        : darwinCategoryIdentifier(darwinActionSpecs(actions)),
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

fln.InterruptionLevel? parseInterruptionLevel(String? value,
        [fln.InterruptionLevel? defaultValue]) =>
    parseEnum(fln.InterruptionLevel.values, value, defaultValue);

/// Prefix of the Apple category identifiers this extension registers.
const String darwinCategoryPrefix = "flet_notifications_actions_";

/// Defaults of the fields describing an action in [darwinActionSpecs], used for
/// fields added after an entry was stored. New fields go at the end, with the
/// default that matches how actions behaved before.
const List<Object?> _darwinActionSpecDefaults = [
  null, // id
  null, // title
  false, // destructive
  true, // foreground
  false, // has input
  null, // input label
  false, // authentication required
];

/// Completes a stored [darwinActionSpecs] entry with the defaults of fields
/// added since, or returns `null` when it doesn't describe an action.
List<Object?>? completeDarwinActionSpec(List<Object?> spec) {
  if (spec.length < 2 ||
      spec.length > _darwinActionSpecDefaults.length ||
      spec[0] is! String ||
      spec[1] is! String) {
    return null;
  }
  return [...spec, ..._darwinActionSpecDefaults.skip(spec.length)];
}

/// The fields of each action that define its Apple category, in a form that can
/// be stored and compared.
List<List<Object?>> darwinActionSpecs(List<ParsedAction> actions) => [
      for (final a in actions)
        [
          a.id,
          a.title,
          a.destructive,
          a.foreground,
          a.input != null,
          a.input?.label,
          a.authenticationRequired,
        ],
    ];

/// Identifier of the Apple category for actions described by [specs].
///
/// It is derived from the actions, so notifications with the same buttons share
/// a category, and it stays the same across app launches.
String darwinCategoryIdentifier(List<List<Object?>> specs) {
  // 32-bit FNV-1a, which unlike `hashCode` is stable across runs.
  var hash = 0x811c9dc5;
  for (final unit in utf8.encode(jsonEncode(specs))) {
    hash = ((hash ^ unit) * 0x01000193) & 0xffffffff;
  }
  return "$darwinCategoryPrefix${hash.toRadixString(16).padLeft(8, "0")}";
}

/// Builds the Apple category [identifier] for actions described by [specs].
///
/// The identifier is the one notifications were delivered with, which for
/// categories stored before fields were added differs from
/// [darwinCategoryIdentifier] of their completed specs.
fln.DarwinNotificationCategory darwinCategory(
    String identifier, List<List<Object?>> specs) {
  return fln.DarwinNotificationCategory(
    identifier,
    actions: [
      for (final [
            id,
            title,
            destructive,
            foreground,
            hasInput,
            label,
            authenticationRequired,
          ] in specs)
        _darwinAction(
          id as String,
          title as String,
          {
            if (destructive == true)
              fln.DarwinNotificationActionOption.destructive,
            if (foreground == true)
              fln.DarwinNotificationActionOption.foreground,
            if (authenticationRequired == true)
              fln.DarwinNotificationActionOption.authenticationRequired,
          },
          hasInput == true,
          label as String?,
        ),
    ],
  );
}

fln.DarwinNotificationAction _darwinAction(
  String id,
  String title,
  Set<fln.DarwinNotificationActionOption> options,
  bool hasInput,
  String? label,
) {
  if (!hasInput) {
    return fln.DarwinNotificationAction.plain(id, title, options: options);
  }
  return fln.DarwinNotificationAction.text(
    id,
    title,
    buttonTitle: label ?? title,
    placeholder: label,
    options: options,
  );
}
