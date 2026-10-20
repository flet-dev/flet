import 'dart:convert';

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
  return raw.map((entry) {
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
      destructive: optionalBool(entry["destructive"]) ?? false,
      foreground: optionalBool(entry["foreground"]) ?? true,
      cancelNotification: optionalBool(entry["cancel_notification"]) ?? true,
      input: parseInput(entry["input"]),
    );
  }).toList();
}

/// Parses the optional inline-reply `input` of an action.
ParsedInput? parseInput(Object? raw) {
  if (raw == null) return null;
  if (raw is! Map) {
    throw const FormatException("input must be a map");
  }
  final choices = raw["choices"];
  final mimeTypes = raw["allowed_mime_types"];
  return ParsedInput(
    label: raw["label"] is String ? raw["label"] as String : "",
    choices: choices is List ? choices.cast<String>() : const [],
    allowFreeFormInput: optionalBool(raw["allow_free_form_input"]) ?? true,
    allowedMimeTypes:
        mimeTypes is List ? mimeTypes.cast<String>().toSet() : const {},
  );
}

bool? optionalBool(Object? value) {
  if (value == null) return null;
  if (value is bool) return value;
  throw const FormatException("expected a boolean");
}

/// A parsed Android icon/image source (exactly one set).
class ParsedIcon {
  const ParsedIcon({
    this.drawableResource,
    this.filePath,
    this.contentUri,
    this.flutterAsset,
    this.data,
  });

  final String? drawableResource;
  final String? filePath;
  final String? contentUri;
  final String? flutterAsset;
  final List<int>? data; // decoded from base64 on the wire
}

class ParsedPerson {
  const ParsedPerson({
    required this.name,
    this.key,
    this.bot = false,
    this.important = false,
    this.uri,
    this.icon,
  });

  final String name;
  final String? key;
  final bool bot;
  final bool important;
  final String? uri;
  final ParsedIcon? icon;
}

class ParsedMessage {
  const ParsedMessage({
    required this.text,
    required this.timestampIso,
    required this.person,
  });

  final String text;
  final String timestampIso;
  final ParsedPerson person;
}

/// A parsed style payload, plugin-agnostic; the service maps it onto
/// `styleInformation` value objects.
class ParsedStyle {
  const ParsedStyle({
    required this.type,
    this.bigText,
    this.contentTitle,
    this.summaryText,
    this.image,
    this.largeIcon,
    this.lines = const [],
    this.person,
    this.messages = const [],
    this.conversationTitle,
    this.groupConversation = false,
  });

  final String type;
  final String? bigText;
  final String? contentTitle;
  final String? summaryText;
  final ParsedIcon? image;
  final ParsedIcon? largeIcon;
  final List<String> lines;
  final ParsedPerson? person;
  final List<ParsedMessage> messages;
  final String? conversationTitle;
  final bool groupConversation;
}

/// Parses the optional ``style`` argument of a show/schedule invoke.
ParsedStyle? parseStyle(Object? raw) {
  if (raw == null) return null;
  if (raw is! Map) {
    throw const FormatException("style must be a map");
  }
  final type = raw["_type"];
  if (type is! String || type.isEmpty) {
    throw const FormatException("style type must be a non-empty string");
  }
  switch (type) {
    case "big_text":
      final bigText = raw["big_text"];
      if (bigText is! String || bigText.isEmpty) {
        throw const FormatException("big_text style requires big_text");
      }
      return ParsedStyle(
        type: type,
        bigText: bigText,
        contentTitle: raw["content_title"] as String?,
        summaryText: raw["summary_text"] as String?,
      );
    case "big_picture":
      final image = parseIcon(raw["image"]);
      if (image == null) {
        throw const FormatException("big_picture style requires an image");
      }
      return ParsedStyle(
        type: type,
        image: image,
        largeIcon: parseIcon(raw["large_icon"]),
        contentTitle: raw["content_title"] as String?,
        summaryText: raw["summary_text"] as String?,
      );
    case "inbox":
      final lines = raw["lines"];
      if (lines is! List || lines.isEmpty) {
        throw const FormatException("inbox style requires at least one line");
      }
      return ParsedStyle(
        type: type,
        lines: lines.map((e) => "$e").toList(),
        contentTitle: raw["content_title"] as String?,
        summaryText: raw["summary_text"] as String?,
      );
    case "messaging":
      final person = parsePerson(raw["person"]);
      if (person == null) {
        throw const FormatException("messaging style requires a person");
      }
      final messages = raw["messages"];
      return ParsedStyle(
        type: type,
        person: person,
        messages: messages is List
            ? messages.map(parseMessage).whereType<ParsedMessage>().toList()
            : const [],
        conversationTitle: raw["conversation_title"] as String?,
        groupConversation: optionalBool(raw["group_conversation"]) ?? false,
      );
    default:
      throw FormatException("unknown style type: $type");
  }
}

/// Parses an icon payload; enforces exactly one source.
ParsedIcon? parseIcon(Object? raw) {
  if (raw == null) return null;
  if (raw is! Map) {
    throw const FormatException("icon must be a map");
  }
  final drawableResource = raw["drawable_resource"] as String?;
  final filePath = raw["file_path"] as String?;
  final contentUri = raw["content_uri"] as String?;
  final flutterAsset = raw["flutter_asset"] as String?;
  final dataBase64 = raw["data_base64"] as String?;
  final sources = [
    drawableResource,
    filePath,
    contentUri,
    flutterAsset,
    dataBase64,
  ];
  if (sources.where((s) => s != null).length != 1) {
    throw const FormatException("icon requires exactly one source");
  }
  return ParsedIcon(
    drawableResource: drawableResource,
    filePath: filePath,
    contentUri: contentUri,
    flutterAsset: flutterAsset,
    data: dataBase64 == null ? null : base64Decode(dataBase64),
  );
}

ParsedPerson? parsePerson(Object? raw) {
  if (raw == null) return null;
  if (raw is! Map) {
    throw const FormatException("person must be a map");
  }
  final name = raw["name"];
  if (name is! String || name.isEmpty) {
    throw const FormatException("person name must be a non-empty string");
  }
  return ParsedPerson(
    name: name,
    key: raw["key"] as String?,
    bot: optionalBool(raw["bot"]) ?? false,
    important: optionalBool(raw["important"]) ?? false,
    uri: raw["uri"] as String?,
    icon: parseIcon(raw["icon"]),
  );
}

ParsedMessage? parseMessage(Object? raw) {
  if (raw is! Map) {
    throw const FormatException("message must be a map");
  }
  final text = raw["text"];
  final timestamp = raw["timestamp"];
  final person = parsePerson(raw["person"]);
  if (text is! String || text.isEmpty || timestamp is! String) {
    throw const FormatException("message requires text and timestamp");
  }
  if (person == null) {
    throw const FormatException("message requires a person");
  }
  return ParsedMessage(text: text, timestampIso: timestamp, person: person);
}
