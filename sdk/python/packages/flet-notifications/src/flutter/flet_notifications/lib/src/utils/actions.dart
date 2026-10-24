import 'dart:convert';

import 'package:flet/flet.dart' show parseBool, parseList;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import 'errors.dart';

class ParsedInput {
  const ParsedInput({
    this.label,
    this.choices = const [],
    this.allowFreeFormInput = true,
    this.allowedMimeTypes = const {},
  });

  final String? label;
  final List<String> choices;
  final bool allowFreeFormInput;
  final Set<String> allowedMimeTypes;
}

class ParsedAction {
  const ParsedAction({
    required this.id,
    required this.title,
    this.destructive = false,
    this.foreground = true,
    this.authenticationRequired = false,
    this.cancelNotification = true,
    this.input,
  });

  final String id;
  final String title;
  final bool destructive;
  final bool foreground;
  final bool authenticationRequired;
  final bool cancelNotification;
  final ParsedInput? input;
}

/// Parses the `actions` argument (a list of dicts sent from Python) into
/// [ParsedAction]s.
///
/// Throws [NotificationException] with `invalid_argument` for malformed actions.
List<ParsedAction> parseActions(Object? raw) {
  if (raw == null) return const [];
  if (raw is! List) {
    throw const NotificationException.invalidArgument(
      "actions must be a list",
    );
  }
  return parseList(raw, parseAction)!;
}

/// Parses one notification action.
ParsedAction parseAction(Object? entry) {
  if (entry is! Map) {
    throw const NotificationException.invalidArgument(
      "each action must be a map",
    );
  }
  final id = entry["id"];
  final title = entry["title"];
  if (id is! String || id.isEmpty) {
    throw const NotificationException.invalidArgument(
      "action id must be a non-empty string",
    );
  }
  if (title is! String || title.isEmpty) {
    throw const NotificationException.invalidArgument(
      "action title must be a non-empty string",
    );
  }
  return ParsedAction(
    id: id,
    title: title,
    destructive: parseBool(entry["destructive"], false)!,
    foreground: parseBool(entry["foreground"], true)!,
    authenticationRequired: parseBool(entry["require_authentication"], false)!,
    cancelNotification: parseBool(entry["cancel_notification"], true)!,
    input: parseActionInput(entry["input"]),
  );
}

/// Parses the optional inline-reply `input` of an action.
ParsedInput? parseActionInput(Object? raw) {
  if (raw == null) return null;
  if (raw is! Map) {
    throw const NotificationException.invalidArgument("input must be a map");
  }
  final choices = raw["choices"];
  final mimeTypes = raw["allowed_mime_types"];
  if (choices != null &&
      (choices is! List || choices.any((v) => v is! String))) {
    throw const NotificationException.invalidArgument(
      "input choices must be a list of strings",
    );
  }
  if (mimeTypes != null &&
      (mimeTypes is! List || mimeTypes.any((v) => v is! String))) {
    throw const NotificationException.invalidArgument(
      "input allowed_mime_types must be a list of strings",
    );
  }
  return ParsedInput(
    label: raw["label"] is String && (raw["label"] as String).isNotEmpty
        ? raw["label"] as String
        : null,
    choices: choices is List ? List<String>.from(choices) : const [],
    allowFreeFormInput: parseBool(raw["allow_free_form_input"], true)!,
    allowedMimeTypes:
        mimeTypes is List ? Set<String>.from(mimeTypes) : const {},
  );
}

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
