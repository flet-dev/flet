import 'dart:convert';

import 'package:flet/flet.dart' show parseBool, parseList;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import 'errors.dart';

/// Parses the optional Android style directly into its native representation.
fln.StyleInformation? parseStyle(Object? value) {
  if (value == null) return null;
  try {
    if (value is! Map) {
      throw const FormatException("style must be a map");
    }
    switch (value["_type"]) {
      case "big_text":
        final text = value["big_text"];
        if (text is! String || text.isEmpty) {
          throw const FormatException("big_text style requires big_text");
        }
        return fln.BigTextStyleInformation(
          text,
          contentTitle: value["content_title"] as String?,
          summaryText: value["summary_text"] as String?,
        );
      case "big_picture":
        final image = parseAndroidBitmap(value["image"]);
        if (image == null) {
          throw const FormatException("big_picture style requires an image");
        }
        return fln.BigPictureStyleInformation(
          image,
          largeIcon: parseAndroidBitmap(value["large_icon"]),
          contentTitle: value["content_title"] as String?,
          summaryText: value["summary_text"] as String?,
        );
      case "inbox":
        final lines = value["lines"];
        if (lines is! List || lines.isEmpty || lines.any((v) => v is! String)) {
          throw const FormatException(
              "inbox style requires a non-empty list of strings");
        }
        return fln.InboxStyleInformation(
          List<String>.from(lines),
          contentTitle: value["content_title"] as String?,
          summaryText: value["summary_text"] as String?,
        );
      case "messaging":
        final person = parseAndroidPerson(value["person"]);
        if (person == null) {
          throw const FormatException("messaging style requires a person");
        }
        final messages = value["messages"];
        if (messages != null && messages is! List) {
          throw const FormatException("messages must be a list");
        }
        return fln.MessagingStyleInformation(
          person,
          messages: parseList(messages, parseMessage) ?? const [],
          conversationTitle: value["conversation_title"] as String?,
          groupConversation: parseBool(value["group_conversation"], false)!,
        );
      default:
        throw FormatException("unknown style type: ${value["_type"]}");
    }
  } on FormatException catch (e) {
    throw NotificationException.invalidStyle(e.message);
  } on TypeError catch (e) {
    throw NotificationException.invalidStyle("invalid style field: $e");
  }
}

/// Validates the shared icon payload before selecting a native representation.
({String source, String value})? parseIconSource(Object? value) {
  if (value == null) return null;
  if (value is! Map) {
    throw const FormatException("icon must be a map");
  }
  const sources = [
    "drawable_resource",
    "file_path",
    "content_uri",
    "flutter_asset",
    "data_base64",
  ];
  final selected = sources.where((key) => value[key] != null).toList();
  if (selected.length != 1) {
    throw const FormatException("icon requires exactly one source");
  }
  final source = selected.single;
  final data = value[source];
  if (data is! String) {
    throw FormatException("icon $source must be a string");
  }
  return (source: source, value: data);
}

/// Big-picture bitmaps support drawable resources, files and base64 bytes.
fln.AndroidBitmap<Object>? parseAndroidBitmap(Object? value) {
  final icon = parseIconSource(value);
  if (icon == null) return null;
  switch (icon.source) {
    case "drawable_resource":
      return fln.DrawableResourceAndroidBitmap(icon.value);
    case "file_path":
      return fln.FilePathAndroidBitmap(icon.value);
    case "data_base64":
      return fln.ByteArrayAndroidBitmap(base64Decode(icon.value));
    default:
      throw const FormatException(
          "big-picture images support drawable, file path and byte sources");
  }
}

/// Person icons additionally support content URIs and Flutter assets.
fln.AndroidIcon<Object>? parseAndroidIcon(Object? value) {
  final icon = parseIconSource(value);
  if (icon == null) return null;
  switch (icon.source) {
    case "drawable_resource":
      return fln.DrawableResourceAndroidIcon(icon.value);
    case "file_path":
      return fln.BitmapFilePathAndroidIcon(icon.value);
    case "content_uri":
      return fln.ContentUriAndroidIcon(icon.value);
    case "flutter_asset":
      return fln.FlutterBitmapAssetAndroidIcon(icon.value);
    case "data_base64":
      return fln.ByteArrayAndroidIcon(base64Decode(icon.value));
    default:
      throw const FormatException("unknown icon source");
  }
}

fln.Person? parseAndroidPerson(Object? value) {
  if (value == null) return null;
  if (value is! Map) {
    throw const FormatException("person must be a map");
  }
  final name = value["name"];
  if (name is! String || name.isEmpty) {
    throw const FormatException("person name must be a non-empty string");
  }
  return fln.Person(
    name: name,
    key: value["key"] as String?,
    bot: parseBool(value["bot"], false)!,
    important: parseBool(value["important"], false)!,
    uri: value["uri"] as String?,
    icon: parseAndroidIcon(value["icon"]),
  );
}

fln.Message parseMessage(Object? value) {
  if (value is! Map) {
    throw const FormatException("message must be a map");
  }
  final text = value["text"];
  final timestamp = value["timestamp"];
  if (text is! String || text.isEmpty || timestamp is! DateTime) {
    throw const FormatException("message requires text and timestamp");
  }
  final person = parseAndroidPerson(value["person"]);
  if (person == null) {
    throw const FormatException("message requires a person");
  }
  return fln.Message(text, timestamp, person);
}
