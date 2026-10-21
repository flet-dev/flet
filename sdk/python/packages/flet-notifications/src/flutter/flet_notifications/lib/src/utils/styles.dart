import 'dart:convert';
import 'dart:typed_data';

import 'package:flet/flet.dart' show parseBool;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

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

/// Parses the optional `style` argument of a show/schedule invoke.
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
        messages:
            messages is List ? messages.map(parseMessage).toList() : const [],
        conversationTitle: raw["conversation_title"] as String?,
        groupConversation: parseBool(raw["group_conversation"], false)!,
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
    bot: parseBool(raw["bot"], false)!,
    important: parseBool(raw["important"], false)!,
    uri: raw["uri"] as String?,
    icon: parseIcon(raw["icon"]),
  );
}

ParsedMessage parseMessage(Object? raw) {
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
        parseAndroidBitmap(style.image!)!,
        largeIcon: parseAndroidBitmap(style.largeIcon),
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
        parseAndroidPerson(style.person!),
        conversationTitle: style.conversationTitle,
        groupConversation: style.groupConversation,
        messages: style.messages
            .map(
              (m) => fln.Message(
                m.text,
                DateTime.parse(m.timestampIso),
                parseAndroidPerson(m.person),
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
fln.AndroidBitmap<Object>? parseAndroidBitmap(ParsedIcon? icon) {
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
fln.AndroidIcon<Object>? parseAndroidIcon(ParsedIcon? icon) {
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

fln.Person parseAndroidPerson(ParsedPerson person) {
  return fln.Person(
    name: person.name,
    key: person.key,
    bot: person.bot,
    important: person.important,
    uri: person.uri,
    icon: parseAndroidIcon(person.icon),
  );
}
