import 'package:flet/flet.dart' show parseBool, parseList;

class ParsedInput {
  const ParsedInput({
    this.label = "",
    this.choices = const [],
    this.allowFreeFormInput = true,
    this.allowedMimeTypes = const {},
  });

  final String label;
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
/// Throws [FormatException] with a human-readable message on bad input; the
/// service converts it into an `error:invalid_action:...` invoke result.
List<ParsedAction> parseActions(Object? raw) {
  if (raw == null) return const [];
  if (raw is! List) {
    throw const FormatException("actions must be a list");
  }
  return parseList(raw, parseAction)!;
}

/// Parses one notification action.
ParsedAction parseAction(Object? entry) {
  if (entry is! Map) {
    throw const FormatException("each action must be a map");
  }
  final id = entry["id"];
  final title = entry["title"];
  if (id is! String || id.isEmpty) {
    throw const FormatException("action id must be a non-empty string");
  }
  if (title is! String || title.isEmpty) {
    throw const FormatException("action title must be a non-empty string");
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
    throw const FormatException("input must be a map");
  }
  final choices = raw["choices"];
  final mimeTypes = raw["allowed_mime_types"];
  if (choices != null &&
      (choices is! List || choices.any((v) => v is! String))) {
    throw const FormatException("input choices must be a list of strings");
  }
  if (mimeTypes != null &&
      (mimeTypes is! List || mimeTypes.any((v) => v is! String))) {
    throw const FormatException(
        "input allowed_mime_types must be a list of strings");
  }
  return ParsedInput(
    label: raw["label"] is String ? raw["label"] as String : "",
    choices: choices is List ? List<String>.from(choices) : const [],
    allowFreeFormInput: parseBool(raw["allow_free_form_input"], true)!,
    allowedMimeTypes:
        mimeTypes is List ? Set<String>.from(mimeTypes) : const {},
  );
}
