import 'dart:typed_data';

import 'package:flet/flet.dart' show parseBool, parseList;
import 'package:flutter_local_notifications/flutter_local_notifications.dart'
    as fln;

import '../utils/errors.dart';

/// Parses the optional Android style directly into its native representation.
fln.StyleInformation? parseStyle(Object? value) {
  if (value == null) return null;
  try {
    if (value is! Map) {
      throw const FormatException("style must be a map");
    }
    switch (value["_type"]) {
      case "big_text":
        final text = value["text"];
        if (text is! String || text.isEmpty) {
          throw const FormatException("big_text style requires text");
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
    throw NotificationException.invalidArgument(e.message);
  } on TypeError catch (e) {
    throw NotificationException.invalidArgument("invalid style field: $e");
  }
}

/// Reads the discriminator and value of an `AndroidIcon` payload.
({String type, Object? value})? _parseIconSource(Object? value) {
  if (value == null) return null;
  if (value is! Map) {
    throw const FormatException("icon must be a map");
  }
  final type = value["_type"];
  return switch (type) {
    "drawable" => (type: type as String, value: value["name"]),
    "file" => (type: type as String, value: value["path"]),
    "bytes" => (type: type as String, value: value["data"]),
    "content_uri" => (type: type as String, value: value["uri"]),
    _ => throw FormatException("unknown icon type: $type"),
  };
}

/// Notification images accept drawable, file and byte sources.
fln.AndroidBitmap<Object>? parseAndroidBitmap(Object? value) {
  final icon = _parseIconSource(value);
  if (icon == null) return null;
  switch (icon) {
    case (type: "drawable", value: final String name):
      return fln.DrawableResourceAndroidBitmap(name);
    case (type: "file", value: final String path):
      return fln.FilePathAndroidBitmap(path);
    case (type: "bytes", value: final Uint8List data):
      return fln.ByteArrayAndroidBitmap(data);
    case (type: "content_uri", value: _):
      throw const FormatException(
          "notification images support drawable, file and byte sources");
    default:
      throw FormatException("invalid ${icon.type} icon");
  }
}

/// Person icons additionally support content URIs.
fln.AndroidIcon<Object>? parseAndroidIcon(Object? value) {
  final icon = _parseIconSource(value);
  if (icon == null) return null;
  switch (icon) {
    case (type: "drawable", value: final String name):
      return fln.DrawableResourceAndroidIcon(name);
    case (type: "file", value: final String path):
      return fln.BitmapFilePathAndroidIcon(path);
    case (type: "bytes", value: final Uint8List data):
      return fln.ByteArrayAndroidIcon(data);
    case (type: "content_uri", value: final String uri):
      return fln.ContentUriAndroidIcon(uri);
    default:
      throw FormatException("invalid ${icon.type} icon");
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
