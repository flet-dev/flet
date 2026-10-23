import 'package:flet/flet.dart' show parseBool, parseList;
import 'package:flutter/foundation.dart' show setEquals;
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
    this.cancelNotification = true,
    this.input,
  });

  final String id;
  final String title;
  final bool destructive;
  final bool foreground;
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

/// Compares the native category definitions, including action order and options.
bool areDarwinCategoriesEqual(
  fln.DarwinNotificationCategory? registered,
  fln.DarwinNotificationCategory category,
) {
  if (registered == null ||
      registered.identifier != category.identifier ||
      !setEquals(registered.options, category.options) ||
      registered.actions.length != category.actions.length) {
    return false;
  }
  for (var i = 0; i < category.actions.length; i++) {
    final a = registered.actions[i];
    final b = category.actions[i];
    if ((a.type, a.identifier, a.title, a.buttonTitle, a.placeholder) !=
            (b.type, b.identifier, b.title, b.buttonTitle, b.placeholder) ||
        !setEquals(a.options, b.options)) {
      return false;
    }
  }
  return true;
}
